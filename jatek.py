#!/usr/bin/env python3
import sys
import random
import os
from random import random
from typing import List, Dict, Optional

# Card types cycle (for strengths/weaknesses): levego <-> fold <-> viz <-> tuz <-> levego
TYPE_ORDER = ['levego', 'fold', 'viz', 'tuz']

def type_multiplier(attacker: str, defender: str) -> float:
    if attacker == defender:
        return 1.0
    try:

        ai = TYPE_ORDER.index(attacker)
        di = TYPE_ORDER.index(defender)
    except ValueError:
        return 1.0
    if (ai+di!=3) and (ai!=di):
        return 2.0
    if (ai+di==3):
        return 0.5
    return 1.0

class Card:
    def __init__(self, name: str, damage: int, hp: int, ctype: str, is_leader=False):
        self.name = name
        self.base_damage = int(damage)
        self.base_hp = int(hp)
        self.type = ctype
        self.is_leader = is_leader
        # current 'base' stats in player's collection (can be increased by rewards)
        self.col_damage = int(damage)
        self.col_hp = int(hp)

    def copy_for_battle(self):
        # returns a fresh mutable battle instance with hp and damage
        return BattleCard(self.name, self.col_damage, self.col_hp, self.type)

    def serialize_world(self) -> str:
        return f"kartya;{self.name};{self.base_damage};{self.base_hp};{self.type}"

    def serialize_collection(self) -> str:
        return f"gyujtemeny;{self.name};{self.col_damage};{self.col_hp};{self.type}"

class Leader(Card):
    def __init__(self, name: str, source: Card, boost: str):
        # boost: 'sebzes' or 'eletero'
        damage = source.base_damage
        hp = source.base_hp
        if boost == 'sebzes':
            damage = damage * 2
        elif boost == 'eletero':
            hp = hp * 2
        super().__init__(name, damage, hp, source.type, is_leader=True)
        # leaders have base_damage and base_hp as modified values
        self.col_damage = damage
        self.col_hp = hp

class Dungeon:
    def __init__(self, dtype: str, name: str, simple_cards: List[str], leader_name: Optional[str], reward: Optional[str]):
        self.type = dtype  # egyszeru, kis, nagy
        self.name = name
        self.simple_cards = simple_cards[:]  # names in order
        self.leader_name = leader_name
        self.reward = reward  # 'sebzes' or 'eletero' or 'uj kartya' ba

    def serialize(self) -> str:
        if self.type == 'egyszeru':
            return f"kazamata;egyszeru;{self.name};{self.simple_cards[0]};{self.reward}"
        elif self.type == 'kis':
            return f"kazamata;kis;{self.name};{','.join(self.simple_cards)};{self.leader_name};{self.reward}"
        else:
            return f"kazamata;nagy;{self.name};{','.join(self.simple_cards)};{self.leader_name}"

class BattleCard:
    def __init__(self, name: str, damage: int, hp: int, ctype: str):
        self.name = name
        self.damage = int(damage)
        self.hp = int(hp)
        self.type = ctype

    def is_alive(self):
        return self.hp > 0

class Player:
    def __init__(self):
        self.collection: Dict[str, Card] = {}  # name -> Card
        self.deck_order: List[str] = []  # names in deck order

    def add_to_collection(self, card: Card):
        if card.name not in self.collection:
            # store a copy with initial col stats based on card
            c = Card(card.name, card.base_damage, card.base_hp, card.type, is_leader=card.is_leader)
            c.col_damage = card.base_damage
            c.col_hp = card.base_hp
            self.collection[card.name] = c

    def update_card_stats(self, name: str, delta_damage: int = 0, delta_hp: int = 0):
        if name in self.collection:
            self.collection[name].col_damage += delta_damage
            self.collection[name].col_hp += delta_hp

    def serialize(self) -> List[str]:
        lines = []
        for c in self.collection.values():
            lines.append(c.serialize_collection())
        for dn in self.deck_order:
            lines.append(f"pakli;{dn}")
        return lines

    def build_deck(self, names: List[str]):
        # deck must be formed from collection, max half of collection (ceil)
        sz = max(1, (len(self.collection)+1)//2)
        # Use provided order but only take up to sz
        deck = []
        for n in names:
            if n in self.collection and n not in deck:
                deck.append(n)
            if len(deck) >= sz:
                break
        self.deck_order = deck

class Game:
    def __init__(self):
        self.world_cards: Dict[str, Card] = {}
        self.leaders: Dict[str, Leader] = {}
        self.dungeons: Dict[str, Dungeon] = {}
        self.player = Player()

    def add_world_card(self, name, damage, hp, ctype):
        c = Card(name, int(damage), int(hp), ctype)
        self.world_cards[name] = c

    def add_leader(self, name, source_name, boost):
        if source_name not in self.world_cards:
            # ignore invalid
            return
        src = self.world_cards[source_name]
        l = Leader(name, src, boost)
        self.leaders[name] = l

    def add_dungeon(self, dtype, name, simple_list, leader_name, reward):
        self.dungeons[name] = Dungeon(dtype, name, simple_list, leader_name, reward)

    def import_player_card(self, name):
        # can be from world simple cards or leader cards
        if name in self.world_cards:
            self.player.add_to_collection(self.world_cards[name])
        elif name in self.leaders:
            self.player.add_to_collection(self.leaders[name])
        else:
            # ignore
            pass

    def export_world(self) -> List[str]:
        lines = []
        # simple cards in insertion order: we don't have insertion order guaranteed in dict prior to py3.7 but assume
        for c in self.world_cards.values():
            lines.append(c.serialize_world())
        for l in self.leaders.values():
            lines.append(f"vezer;{l.name};{l.col_damage};{l.col_hp};{l.type}")
        for d in self.dungeons.values():
            lines.append(d.serialize())
        return lines

    def export_player(self) -> List[str]:
        return self.player.serialize()

    def run_battle(self, dungeon_name: str, test = True) -> List[str]:
        # returns log lines
        nehezseg=0
        if not test:
            nehezseg=int(input("nehezsegi szint (1-10) "))
        if dungeon_name not in self.dungeons:
            if test:
                return [f"error;nem_letezik_kazamata;{dungeon_name}"]
            else:
                print('Nem létezik ilyen kazamata')
                return []
        d = self.dungeons[dungeon_name]
        # create enemy sequence
        enemy_cards: List[BattleCard] = []
        for name in d.simple_cards:
            if name in self.world_cards:
                enemy_cards.append(self.world_cards[name].copy_for_battle())
            elif name in self.leaders:
                enemy_cards.append(self.leaders[name].copy_for_battle())
            else:
                # skip missing
                pass
        if d.leader_name:
            if d.leader_name in self.leaders:
                enemy_cards.append(self.leaders[d.leader_name].copy_for_battle())
            elif d.leader_name in self.world_cards:
                enemy_cards.append(self.world_cards[d.leader_name].copy_for_battle())
        # player's deck battle copies
        player_deck: List[BattleCard] = []
        for nm in self.player.deck_order:
            if nm in self.player.collection:
                player_deck.append(self.player.collection[nm].copy_for_battle())
        # Reset HPs to collection base
        # Battle proceeds: first kazamata plays its first card, then player plays
        logs: List[str] = []
        logs.append(f"harc kezdodik;{dungeon_name}")
        logs.append("")
        if not test:
            print("⚔️ A harc elkezdődött!")
        # initial play actions (kijatszik) for both sides when their card enters play
        # --- 5. Első kör kijátszásai
        round_no = 1
        if not test:
            print(f"{round_no}.kör")
        enemy_next_kijatsz=False
        if enemy_cards:
            e = enemy_cards[0]
            line = f"{round_no}.kor;kazamata;kijatszik;{e.name};{e.damage};{e.hp};{e.type}"
            logs.append(line)
            if not test:
                print(f"👹 A kazamata kijátszotta: {e.name} | sebzés: {e.damage}, életerő: {e.hp}, típus: {e.type}")
        if player_deck:
            p = player_deck[0]
            line = f"{round_no}.kor;jatekos;kijatszik;{p.name};{p.damage};{p.hp};{p.type}"
            logs.append(line)
            if not test:
                print(f"🧙‍♂️ A játékos kijátszotta: {p.name} | sebzés: {p.damage}, életerő: {p.hp}, típus: {p.type}")

        # --- 6. Harc ciklus
        enemy_index = 0
        player_index = 0

        # segédfüggvény: él-e még valaki?
        def alive(cards):
            return any(c.hp > 0 for c in cards)

        while alive(enemy_cards) and alive(player_deck):
            attacker_e = enemy_cards[enemy_index]
            defender_p = player_deck[player_index]
            round_no+=1
            logs.append("")
            if not test:
                print(f"{round_no}.kör")
            # --- Kazamata támad ---
            if not enemy_next_kijatsz:
                if attacker_e.hp > 0:
                    mult = type_multiplier(attacker_e.type, defender_p.type)
                    dmg = round(attacker_e.damage * mult *(1+random()*float(nehezseg/10)))
                    defender_p.hp -= dmg
                    if defender_p.hp < 0:
                        defender_p.hp = 0
                    line = f"{round_no}.kor;kazamata;tamad;{attacker_e.name};{dmg};{defender_p.name};{defender_p.hp}"
                    logs.append(line)
                    if not test:
                        print(f"👹 A kazamata támad: {attacker_e.name} → {defender_p.name} | sebzés: {dmg}, {defender_p.name} maradék életerő: {defender_p.hp}")
            else:
                # új ellenség kijátszása
                new_enemy = enemy_cards[enemy_index]
                enemy_next_kijatsz = False
                line = f"{round_no}.kor;kazamata;kijatszik;{new_enemy.name};{new_enemy.damage};{new_enemy.hp};{new_enemy.type}"
                logs.append(line)
                if not test:
                    print(f"👹 A kazamata új kártyát hoz játékba: {new_enemy.name} | sebzés: {new_enemy.damage}, életerő: {new_enemy.hp}, típus: {new_enemy.type}")
            # --- Ha a játékos kártyája meghalt ---
            if defender_p.hp <= 0:
                player_index += 1
                if player_index >= len(player_deck):
                    logs.append("jatekos vesztett")
                    if not test:
                        print("💀 A játékos vesztett.")
                    return logs
                # új kártya kijátszása
                new_card = player_deck[player_index]
                line = f"{round_no}.kor;jatekos;kijatszik;{new_card.name};{new_card.damage};{new_card.hp};{new_card.type}"
                logs.append(line)
                if not test:
                    print(f"🧙‍♂️ A játékos új kártyát játszik ki: {new_card.name} | sebzés: {new_card.damage}, életerő: {new_card.hp}, típus: {new_card.type}")
                continue  # a következő kör jön

            # --- Játékos támad ---
            attacker_p = player_deck[player_index]
            defender_e = enemy_cards[enemy_index]
            mult2 = type_multiplier(attacker_p.type, defender_e.type)
            dmg2 = round(attacker_p.damage * mult2*(1-random()*nehezseg/20))
            defender_e.hp -= dmg2
            if defender_e.hp < 0:
                defender_e.hp = 0
            line = f"{round_no}.kor;jatekos;tamad;{attacker_p.name};{dmg2};{defender_e.name};{defender_e.hp}"

            logs.append(line)
            if not test:
                print(f"🗡️ A játékos támad: {attacker_p.name} → {defender_e.name} | sebzés: {dmg2}, {defender_e.name} maradék életerő: {defender_e.hp}")
            # --- Ha az ellenség meghalt ---
            if defender_e.hp <= 0:
                enemy_index += 1
                enemy_next_kijatsz=True
                if enemy_index >= len(enemy_cards):
                    logs.append("")
                    if d.type=='nagy':
                        all_cards = list(self.world_cards.keys()) + list(self.leaders.keys())

                        # Megkeressük az első olyan kártyát ami még nincs meg
                        uj = None
                        for card in all_cards:
                            if card not in self.player.collection:
                                uj = card
                                break

                        if uj is not None:
                            self.player.collection[uj] = self.world_cards.get(uj, self.leaders.get(uj))
                            re = f"{uj}"
                    else:
                        re=f'{d.reward};{player_deck[player_index].name}'
                    logs.append(f"jatekos nyert;{re}")
                    if d.reward=="eletero":
                        if self.player.collection[player_deck[player_index].name].col_hp<100:
                            self.player.collection[player_deck[player_index].name].col_hp+=2
                        if not test:
                            print(f"🏆A játékos nyert! A nyeremény {player_deck[player_index].name} +2 életerő ")
                    elif d.reward=="sebzes":
                        if self.player.collection[player_deck[player_index].name].col_damage<100:
                            self.player.collection[player_deck[player_index].name].col_damage+=1
                        if not test:
                            print(f"🏆A játékos nyert! A nyeremény {player_deck[player_index].name} +1 sebzés")
                    else:
                        if not test:
                            print(f"🏆A játékos nyert! A nyeremény egy új kártya a gyűjteménybe: {uj}")
                    return logs



        # Ha ide jut, valami hiba
        if not alive(player_deck):
            logs.append("jatekos vesztett")
        elif not alive(enemy_cards):
            logs.append("jatekos nyert")
        else:
            logs.append("error;ismeretlen_allapot")

        return logs


def process_test_folder(folder: str):
    game = Game()
    inpath = os.path.join(folder, 'in.txt')
    if not os.path.exists(inpath):
        print(f"in.txt not found in {folder}")
        return
    with open(inpath, 'r', encoding='utf-8') as f:
        lines = [ln.strip() for ln in f.readlines()]
    # allow empty lines
    for raw in lines:
        if not raw:
            continue
        parts = raw.split(';')
        cmd = parts[0].strip()
        if cmd == 'uj kartya':
            # uj kartya;Name;damage;hp;type
            _, name, dmg, hp, ctype = parts
            game.add_world_card(name.strip(), int(dmg), int(hp), ctype.strip())
        elif cmd == 'uj vezer':
            # uj vezer;Name;Source;sebzes/eletero
            _, name, source, boost = parts
            game.add_leader(name.strip(), source.strip(), boost.strip())
        elif cmd == 'uj kazamata':
            # uj kazamata;type;Name;simple_list(;leader;reward?)
            # parse variable args
            # parts: 0 cmd,1 type,2 name,3 simple(s), maybe 4 leader, maybe 5 reward
            dtype = parts[1].strip()
            name = parts[2].strip()
            simple = []
            leader_name = None
            reward = None
            if dtype == 'egyszeru':
                simple = [parts[3].strip()]
                reward = parts[4].strip() if len(parts) > 4 else None
            elif dtype == 'kis':
                simple = [s.strip() for s in parts[3].split(',') if s.strip()]
                leader_name = parts[4].strip() if len(parts) > 4 else None
                reward = parts[5].strip() if len(parts) > 5 else None
            elif dtype == 'nagy':
                simple = [s.strip() for s in parts[3].split(',') if s.strip()]
                leader_name = parts[4].strip() if len(parts) > 4 else None
                reward = 'uj_kartya'
            game.add_dungeon(dtype, name, simple, leader_name, reward)
        elif cmd == 'uj jatekos':
            # initialize player - already exists
            game.player = Player()
        elif cmd == 'felvetel gyujtemenybe':
            # felvetel gyujtemenybe;Name
            _, name = parts
            game.import_player_card(name.strip())
        elif cmd == 'uj pakli':
            # uj pakli;Name1,Name2 or ;Name1,Name2 as parts[1]
            # sometimes format in example is 'uj pakli;Corky,Kira'
            if len(parts) >= 2:
                names = [s.strip() for s in parts[1].split(',') if s.strip()]
                game.player.build_deck(names)
        elif cmd == 'harc':
            # harc;DungeonName;out.filename
            _, dname, outfn = parts[:3]
            logs = game.run_battle(dname.strip())
            outpath = os.path.join(folder, outfn.strip())
            with open(outpath, 'w', encoding='utf-8') as outf:
                for ln in logs:
                    outf.write(ln + '\n')
        elif cmd == 'export vilag':
            _, outfn = parts
            lines_out = game.export_world()
            outpath = os.path.join(folder, outfn.strip())
            with open(outpath, 'w', encoding='utf-8') as outf:
                for ln in lines_out:
                    outf.write(ln + '\n')
        elif cmd == 'export jatekos':
            _, outfn = parts
            lines_out = game.export_player()
            outpath = os.path.join(folder, outfn.strip())
            with open(outpath, 'w', encoding='utf-8') as outf:
                for ln in lines_out:
                    outf.write(ln + '\n')
        else:
            # unknown command - ignore or print
            # Allow other commands in inputs
            pass
    print("Teszt futtatás befejezve.")


def run_ui():

    game = Game()
    # Base game mode

    # Initialize game

    game.add_world_card('Arin', 2, 5, 'fold')
    game.add_world_card('Liora', 2, 4, 'levego')
    game.add_world_card('Nerun', 3, 3, 'tuz')
    game.add_world_card('Selia', 2, 6, 'viz')
    game.add_world_card('Torak', 3, 4, 'fold')
    game.add_world_card('Emera', 2, 5, 'levego')
    game.add_world_card('Vorn', 2, 7, 'viz')
    game.add_world_card('Kael', 3, 5, 'tuz')
    game.add_world_card('Myra', 2, 6, 'fold')
    game.add_world_card('Thalen', 3, 5, 'levego')
    game.add_world_card('Isara', 2, 6, 'viz')

    game.add_leader('Lord Torak', 'Torak', 'sebzes') #if False else None
    game.add_leader('Priestess Selia', 'Selia', 'eletero') #if False else None

    game.add_dungeon('egyszeru', 'Barlangi portya', ['Nerun'], None, 'sebzes')
    game.add_dungeon('kis', 'Ősi Szentély', ['Arin', 'Emera', 'Selia'], 'Lord Torak', 'eletero')
    game.add_dungeon('nagy', 'A mélység királynője', ['Liora', 'Arin', 'Selia', 'Nerun', 'Torak'], 'Priestess Sella', None)

    for n in ['Arin', 'Liora', 'Selia', 'Nerun', 'Torak', 'Emera', 'Kael', 'Myra', 'Thalen', 'Isara']:
      game.import_player_card(n)

    print("🔥 Damareen – a gyűjtögetős fantasy kártyajáték, ahol stratégia, szerencse és képzelet fonódik össze. \n"
          "🪙 A selyemutak játszóasztalaitól a modern digitális arénákig ez a műfaj mindig is a hősök és történetek kovácsa volt. \n"
          "⚔️ Most rajtad a sor, hogy saját paklid lapjaira írd a történelmet: hősöket teremts, kazamatákon küzdj végig, "
          "és szörnyek vezéreivel mérkőzz meg. \n"
          "🕳️ Vajon a gondosan kidolgozott stratégiád diadalt arat, vagy a kazamaták mélye örökre elnyel? \n"
          "📜 Készítsd elő a paklidat, mert a kártyák sorsot hordoznak!")

    for m in [game.world_cards, game.leaders,game.dungeons, game.player.collection]:
        s = ''
        if m == game.world_cards:
            print('Ezek a világkártyák:')
            for n in m:
                s += n + '\n' + str(game.world_cards[n].col_damage) + '/' +str(game.world_cards[n].col_hp) + '\n'+ game.world_cards[n].type + '\n'
            s = s[:-1]
            print(s)
        elif m == game.leaders:
            print('Ezek a vezérkártyák:')
            for n in m:
                s += n + '\n' + str(game.leaders[n].col_damage) + '/' +str(game.leaders[n].col_hp) + '\n'+ game.leaders[n].type + '\n'
            s = s[:-1]
            print(s)
        elif m == game.dungeons:
            print('Ezek a kazamaták:')
            for n in m:
                s += n + ', '
            s = s[:-2]
            print(s)
        else:
            print('Ez a játékos gyűjteménye:')
            for n in m:
                s += n + ', '
            s = s[:-2]
            print(s)
        s = ''

    while True:
        print('A kalandod következő lépésének választásához írd be a válasznak a számát.')
        print('1. Harc \n2. Új pakli készítése \n3. Kilépés')
        inp = input('> ').strip()
        if inp in ('kilep', 'exit', 'quit', '3'):
            break
        elif inp in ('harc', '1'):
            if not game.player.deck_order:
                print('Először paklira lesz szükséged, kérlek készíts egyet.')
            else:
                print('Választható kazamaták:')

                i = 1
                if len(game.player.collection) == len(game.world_cards) + len(game.leaders) :
                    nagy = False
                else:
                    nagy = True
                for n in game.dungeons:
                    if not (nagy) and i == 3:
                        break
                    print(i, n)
                    if game.dungeons[n].reward == None:
                        s = 'új kártya'
                    else:
                        s = game.dungeons[n].reward
                        if s == 'sebzes':
                            s = 'sebzés'
                        else:
                            s = 'életerő'
                    print('Nyeremény:',s)
                    for m in game.dungeons[n].simple_cards:
                        print(m + '\n' + str(game.world_cards[m].col_damage) + '/' +str(game.world_cards[m].col_hp) + '\n'+ game.world_cards[m].type)
                    if not (game.dungeons[n].type == 'egyszeru'):
                        for m in game.leaders:
                          if m == game.dungeons[n].leader_name:
                              print(m + '\n' + str(game.leaders[m].col_damage) + '/' +str(game.leaders[m].col_hp) + '\n'+ game.leaders[m].type)
                    i += 1

                kaz = input('> ').strip()
                i = 1
                if kaz == '1':
                    for k in game.dungeons:
                        break
                    game.run_battle(k,False)
                elif kaz == '2':
                    for k in game.dungeons:
                        if i == 2:
                            break
                        i += 1
                    game.run_battle(k,False)
                elif (kaz == '3') and nagy:
                    for k in game.dungeons:
                        if i == 3:
                            break
                        i += 1
                    game.run_battle(k,False)
                else:
                    print('Helytelen számot adtál meg, kérlek írd újra.')


        elif inp in ('uj pakli', '2'):
            s = ''
            sz = max(1, len(game.player.collection) + 1) // 2
            for n in game.player.collection:
                s += n + '\n' + str(game.player.collection[n].col_damage) + '/' +str(game.player.collection[n].col_hp) + '\n'+ game.player.collection[n].type + '\n'
            s = s[:-1]
            print(s)
            print(f"Ezek a kártyáid, mindegyik csak egyszer szerepelhet, max {sz} kártya lehet a paklidban.")
            print('Add meg a kártyák számát, ha az érték nagyobb a maximumnál akkor a maximális értékre lesz kerekítve.')
            names = []
            h = True
            while h:
                j = input('> ').strip()
                if j.isnumeric():
                    h = False
                    j = int(j)
                else:
                    print('Helytelen válasz, kérlek írj egy számot.')
            if j > sz :
                j = sz
            i = 0
            while i < j :
                print('Kérem a kártya nevét: ')
                n = input('> ').strip()
                if n not in game.player.collection:
                    print('Ez a kártya nincs meg, kérlek írd újra.')
                elif n in names:
                    print('Ezt a kártyát már beírtad, kérlek írd újra.')
                else:
                    names.append(n)
                    i += 1

            game.player.build_deck(names)

        else:
            print('Helytelen számot írtál be, kérlek írd újra.')

    print('Játek vége')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Használat: python jatek.py <input_folder>  vagy  python jatek.py --ui')
        sys.exit(1)
    if sys.argv[1] == '--ui':
        run_ui()
    else:
        folder = sys.argv[1]
        process_test_folder(folder)
