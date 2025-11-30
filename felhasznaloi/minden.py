#!/usr/bin/env python3
import sys
import random
import heapq
import os
from random import random
from typing import List, Dict, Optional

import pygame
# from pygame import K_BACKSPACE

clock = pygame.time.Clock()
pygame.font.init()

screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption("Damareen")
hatter = pygame.image.load("hatter.png").convert()

ii = 9

szaml = 0
sorok = 0
ok = True
Lista_m = []
nevecske = ''

#gombok
kilepes = pygame.image.load("kilepes.png").convert()
#kilepes.set_colorkey((255,255,255))
pakli = pygame.image.load("uj_pakli.png").convert()
#pakli.set_colorkey((255,255,255))
harc1 = pygame.image.load("harc1.png").convert()
harc2 = pygame.image.load("harc2.png").convert()
harc3 = pygame.image.load("harc3.png").convert()
igen = pygame.image.load("igen.png").convert()
#igen.set_colorkey((255,255,255))
megsem = pygame.image.load("nem.png").convert()
#megsem.set_colorkey((255,255,255))
mentes = pygame.image.load("mentes.png").convert()
jatek_m = pygame.image.load('jatek_m.png').convert()
jatekos = pygame.image.load('jatekos_.png').convert()
vissza = pygame.image.load('vissza_.png').convert()
kartya = pygame.image.load('kartya.png').convert()
kazamata = pygame.image.load('kazamata.png').convert()
vezerkartya = pygame.image.load('vezerkartya.png').convert()
uj_jatek = pygame.image.load('uj jatek.png').convert()


jobbra = pygame.image.load("nyil_j.png").convert()
balra = pygame.image.load("nyil_b.png").convert()

#hatterek/feliratok
biztos = pygame.image.load("biztos.png").convert()
pakli_hatter = pygame.image.load("pakli_keret.png").convert()
uj_pakli_hatter = pygame.image.load("uj_pakli_keret.png").convert()
damareen = pygame.image.load("damareen.png").convert_alpha()
lement = pygame.image.load('lement.png').convert()
ment_nev = pygame.image.load('ment_nev.png')
entry = pygame.image.load('entry.png')

class Ablakok:
    def __init__(self,x,y,kep,scale):
        self.x = x
        self.y = y
        heigth = kep.get_height()
        width = kep.get_width()
        self.kep = pygame.transform.scale(kep, (int(width * scale), int(heigth * scale)))
    def draw(self):
        screen.blit(self.kep, (self.x, self.y))

class Gombok:
    def __init__(self,x,y,kep,scale,nev,szam):
        self.nev = nev
        heigth = kep.get_height()
        width = kep.get_width()
        self.kep = pygame.transform.scale(kep,(int(width * scale),int(heigth * scale)))
        self.x = x
        self.y = y
        self.clicked = False
        self.mouse = False
        self.pressed = False
        self.szam = szam
    def draw(self):
        global ii

        pos = pygame.mouse.get_pos()

        ok1=False
        ok2=False

        height = self.kep.get_height()
        width = self.kep.get_width()

        if pos[0]>self.x and pos[0]<self.x+int(width):
            ok1=True
        if pos[1]>self.y and pos[1]<self.y+int(height):
            ok2=True

        if ok1 and ok2:
            self.kep.set_alpha(200)
        else:
            self.kep.set_alpha(255)

        if ok1 and ok2:
            if pygame.mouse.get_pressed()[0] == 0:
                self.mouse = True
        else:
            self.mouse = False
        if ok1 and ok2:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and self.mouse:
                self.pressed = True

        if ok1 and ok2:
            if self.pressed and pygame.mouse.get_pressed()[0] == 0:
                ii = self.szam
                self.mouse = False
                self.pressed = False

        screen.blit(self.kep,(self.x,self.y))


class Mentes_kinyitas:
    def __init__(self,x,y,kep,scale,nev):
        self.nev = nev
        heigth = kep.get_height()
        width = kep.get_width()
        self.kep = pygame.transform.scale(kep, (int(width * scale), int(heigth * scale)))
        self.x = x
        self.y = y
        self.clicked = False
        self.mouse = False
        self.pressed = False

    def draw(self,hanyadik):
        global ii
        self.x = 360
        self.y = 90 + hanyadik * 50
        my_font = pygame.font.Font('ByteBounce.ttf', 30)
        text_s = my_font.render(str(self.nev[16:len(self.nev)-4]), True, (195, 150, 99))
        screen.blit(self.kep, (self.x, self.y))
        screen.blit(text_s, (self.x + 7, self.y + 7))

        pos = pygame.mouse.get_pos()

        ok1=False
        ok2=False

        height = self.kep.get_height()
        width = self.kep.get_width()

        if pos[0]>self.x and pos[0]<self.x+int(width):
            ok1=True
        if pos[1]>self.y and pos[1]<self.y+int(height):
            ok2=True


        if ok1 and ok2:
            if pygame.mouse.get_pressed()[0] == 0:
                self.mouse = True
        else:
            self.mouse = False
        if ok1 and ok2:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and self.mouse:
                self.pressed = True

        if ok1 and ok2:
            if self.pressed and pygame.mouse.get_pressed()[0] == 0:
                Game.kinyit(Game, self.nev)
                ii = 0
                self.mouse = False
                self.pressed = False


class Slider:
    def __init__(self, pos : tuple, size : tuple, initial_val : float, min : int, max : int) -> None:
        self.pos = pos
        self.size = size

        self.slider_left_pos = self.pos[0] - (size[0]//2)
        self.slider_right_pos = self.pos[0] - (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10, self.size[1])

    def move_slider(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]
    def draw(self):
        pygame.draw.rect(screen, "darkgray", self.container_rect)
        pygame.draw.rect(screen, "blue", self.button_rect)
    def get_value(self):
        val_range = self.slider_left_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos

        return (button_val / val_range) * (self.max - self.min) + self.min

#gombok
Pakli = Gombok(90, 463, pakli, 0.95, 'pakli', 1)
'''
Harc1 = Gombok(500,0,harc1, 1,'harc1',2)
Harc2 = Gombok(500,200,harc2, 1,'harc2',2)
Harc3 = Gombok(500,400,harc3, 1,'harc3',2)
'''
Kilepes = Gombok(416, 365, kilepes, 1.1, 'kilepes', 5)
Igen = Gombok(515, 310, igen, 1, 'igen', 6)
Megsem = Gombok(345, 310, megsem, 1, 'megsem', 9)
Mentes = Gombok(400, 350, mentes, 0.8, 'mentes', 0)
Jobb = Gombok(275,400,jobbra,1,'jobb',7)
Bal = Gombok(215,400,balra,1,'bal',8)
Jobb_g = Gombok(900,480,jobbra,1,'jobb gyujtemeny',11)
Bal_g = Gombok(50,480,balra,1,'bal gyujtemeny',12)
J_mester = Gombok(363,270,jatek_m,0.85,'jatekmester',10)
Jatekos = Gombok(388,180,jatekos,0.82,'jatekos',13)
Vissza = Gombok(15,20,vissza, 1,'vissza',14)
Kartya = Gombok(370, 100, kartya, 1, 'uj kartya', 10)
Kazamata = Gombok(351,340,kazamata,1,'uj kazamata',10)
Vezerkartya = Gombok(340, 200, vezerkartya, 1, 'uj vezerkartya',10)
Nehezseg = Slider((300, 560), (300, 30),0, 0, 10)
Uj_jatek = Gombok(390, 50, uj_jatek, 1,'uj jatek',17)
L_igen = Gombok(515, 310, igen, 1, 'menti', 15)
L_nem = Gombok(345, 310, megsem, 1, 'nem menti', 9)
Ment = Gombok(420,320,mentes, 0.9,'lement',16)


#hatterek/feliratok
Biztos = Ablakok(305,170, biztos,1)
Pakli_hatter = Ablakok(80, 20, pakli_hatter, 1)
Uj_pakli_hatter = Ablakok(30,40,uj_pakli_hatter, 1)
Damareen = Ablakok(307, 30, damareen,1)
Lement = Ablakok(305, 170, lement, 1)
Ment_nev = Ablakok(305, 170, ment_nev,1)
Entry = Ablakok(355,270 ,entry,1) # a tombbe valtoztatas nem lesz ok
#miklol old meg magad
#kartyak
tav = 0
tav2 = 0
tav3 = 0
oszl = 0
old = 1
old2 = 1
old3 = 1
ok2 = False
ii_e = 0
text = ''
ok_uj = False
kep = pygame.image.load('entry_.png').convert_alpha()
my_font = pygame.font.Font('ByteBounce.ttf', 25)

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
    def __init__(self, name: str, damage: int, hp: int, ctype: str, is_leader=False, scale = 1.00):
        self.name = name
        self.base_damage = int(damage)
        self.base_hp = int(hp)
        self.type = ctype
        self.is_leader = is_leader
        # current 'base' stats in player's collection (can be increased by rewards)
        self.col_damage = int(damage)
        self.col_hp = int(hp)

        # kartyak vizualis

        if ctype == "levego":
            self.kep = pygame.image.load("kartya_l.png").convert()
            #self.kartya_l
        elif ctype == "fold":
            self.kep = pygame.image.load("kartya_f.png").convert()
            #self.kartya_f
        elif ctype == "viz":
            self.kep = pygame.image.load("kartya_v.png").convert()
            #self.kartya_v
        elif ctype == "tuz":
            self.kep = pygame.image.load("kartya_t.png").convert()
            #self.kartya_t


        # Click detection.
        self.clicked = False
        self.mouse = False
        self.pressed = False

        self.x = 0
        self.y = 0
        height = self.kep.get_height()
        width = self.kep.get_width()
        self.kep = pygame.transform.scale(self.kep, (int(width * scale), int(height * scale)))

    def copy_for_battle(self):
        # returns a fresh mutable battle instance with hp and damage
        return BattleCard(self.name, self.col_damage, self.col_hp, self.type)

    def serialize_world(self) -> str:
        return f"kartya;{self.name};{self.base_damage};{self.base_hp};{self.type}"

    def serialize_collection(self) -> str:
        return f"gyujtemeny;{self.name};{self.col_damage};{self.col_hp};{self.type}"

    def draw_pakli(self, tav_be, kp, szorzo = 1):
        global tav
        global szaml
        global tavle
        global oszl
        szaml = szaml + 1
        if szaml % oszl == 1:
            tavle = tavle + 140
            tav = tav_be
        self.x = tav
        self.y = tavle
        screen.blit(self.kep, (self.x, self.y))
        text_s = my_font.render(str(self.col_damage), True, (90, 30, 10))
        text_hp = my_font.render(str(self.col_hp), True, (90, 30, 10))
        screen.blit(text_s, (self.x + 44, self.y + 42))
        screen.blit(text_hp, (self.x + 44, self.y + 75))
        if self.is_leader:
            nev1 = my_font.render(str(self.name)[0:4], True, (90, 30, 10))
            screen.blit(nev1, (self.x + 25, self.y + 9))
            nev2 = my_font.render(str(self.name)[5:len(self.name)], True, (90, 30, 10))
            screen.blit(nev2, (self.x + 17, self.y + 24))
        else:
            nev = my_font.render(str(self.name), True, (90, 30, 10))
            screen.blit(nev, (self.x + 15, self.y + 10))
        tav = tav + 100 * szorzo
        if ii == 1:
            self.clicked = False
            pos = pygame.mouse.get_pos()

            ok1 = False
            ok2 = False

            height = self.kep.get_height()
            width = self.kep.get_width()

            if pos[0] > self.x and pos[0] < self.x + int(width):
                ok1 = True
            if pos[1] > self.y and pos[1] < self.y + int(height):
                ok2 = True

            if ok1 and ok2:
                if pygame.mouse.get_pressed()[0] == 0:
                    self.mouse = True
            else:
                self.mouse = False
            if ok1 and ok2:
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and self.mouse:
                    self.pressed = True

            if ok1 and ok2:
                if self.pressed and pygame.mouse.get_pressed()[0] == 0:
                    kp.remove(self.name)
                    self.mouse = False
                    self.pressed = False

        return kp

    def draw_gyujt(self, kg, kp):
        global tav2
        global font
        self.y = 430
        self.x = tav2
        screen.blit(self.kep, (self.x, self.y))
        text_s = my_font.render(str(self.col_damage), True, (90, 30, 10))
        text_hp = my_font.render(str(self.col_hp), True, (90, 30, 10))
        if self.is_leader:
            nev1 = my_font.render(str(self.name)[0:4], True, (90, 30, 10))
            screen.blit(nev1, (self.x + 25, self.y + 9))
            nev2 = my_font.render(str(self.name)[5:len(self.name)], True, (90, 30, 10))
            screen.blit(nev2, (self.x + 17, self.y + 24))
        else:
            nev = my_font.render(str(self.name), True, (90, 30, 10))
            screen.blit(nev, (self.x + 15, self.y + 10))

        screen.blit(text_s, (self.x + 44, self.y + 42))
        screen.blit(text_hp, (self.x + 44, self.y + 75))


        tav2 = tav2 + 100

        pos = pygame.mouse.get_pos()

        ok1 = False
        ok2 = False

        height = self.kep.get_height()
        width = self.kep.get_width()

        if pos[0] > self.x and pos[0] < self.x + int(width):
            ok1 = True
        if pos[1] > self.y and pos[1] < self.y + int(height):
            ok2 = True

        if ok1 and ok2:
            if pygame.mouse.get_pressed()[0] == 0:
                self.mouse = True
        else:
            self.mouse = False
        if ok1 and ok2:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and self.mouse:
                self.pressed = True
        #if ok1 and ok2:
            if self.pressed and pygame.mouse.get_pressed()[0] == 0:
                if (len(kp) + 1) <= len(kg) // 2:
                    kp.append(self.name)
                    self.clicked = True
                    self.mouse = False
                    self.pressed = False

        return kp


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
        self.source = source  # a Card objektum, amiből származik
        self.boost = boost  # 'sebzes' vagy 'eletero'

class Dungeon:
    def __init__(self, dtype: str, name: str, simple_cards: List[str], leader_name: Optional[str], reward: Optional[str], scale = 1.00):
        self.type = dtype  # egyszeru, kis, nagy
        self.name = name
        self.simple_cards = simple_cards[:]  # names in order
        self.leader_name = leader_name
        self.reward = reward  # 'sebzes' or 'eletero' or 'uj kartya' ba

        # Click detection.
        self.clicked = False
        self.mouse = False
        self.pressed = False

        if self.type == 'egyszeru':
            self.kep = pygame.image.load("harc1.png").convert()
        elif self.type == 'kis':
            self.kep = pygame.image.load("harc2.png").convert()
        else:
            self.kep = pygame.image.load("harc3.png").convert()

        self.x = 0
        self.y = 0
        height = self.kep.get_height()
        width = self.kep.get_width()
        self.kep = pygame.transform.scale(self.kep, (int(width * scale), int(height * scale)))

    def serialize(self) -> str:
        if self.type == 'egyszeru':
            return f"kazamata;egyszeru;{self.name};{self.simple_cards[0]};{self.reward}"
        elif self.type == 'kis':
            return f"kazamata;kis;{self.name};{','.join(self.simple_cards)};{self.leader_name};{self.reward}"
        else:
            return f"kazamata;nagy;{self.name};{','.join(self.simple_cards)};{self.leader_name}"

    def draw_button(self,nev1,cards):
        global tav3
        global font
        global ii
        self.y = tav3
        self.x = screen.get_width()/2
        screen.blit(self.kep, (self.x, self.y))

        '''
        text_s = my_font.render(str(self.col_damage), True, (90, 30, 10))
        text_hp = my_font.render(str(self.col_hp), True, (90, 30, 10))
        if self.is_leader:
            nev1 = my_font.render(str(self.name)[0:4], True, (90, 30, 10))
            screen.blit(nev1, (self.x + 25, self.y + 9))
            nev2 = my_font.render(str(self.name)[5:len(self.name)], True, (90, 30, 10))
            screen.blit(nev2, (self.x + 17, self.y + 24))
        else:
            nev = my_font.render(str(self.name), True, (90, 30, 10))
            screen.blit(nev, (self.x + 15, self.y + 10))
            
        screen.blit(text_s, (self.x + 44, self.y + 42))
        screen.blit(text_hp, (self.x + 44, self.y + 75))
        '''

        nev = my_font.render(str(self.name), True, (90, 30, 10))
        screen.blit(nev, (self.x + 15, self.y + 10))

        tav3 = tav3 + 200

        pos = pygame.mouse.get_pos()

        ok1 = False
        ok2 = False

        height = self.kep.get_height()
        width = self.kep.get_width()

        if pos[0] > self.x and pos[0] < self.x + int(width):
            ok1 = True
        if pos[1] > self.y and pos[1] < self.y + int(height):
            ok2 = True

        if ok1 and ok2:
            if pygame.mouse.get_pressed()[0] == 0:
                self.mouse = True
        else:
            self.mouse = False
        if ok1 and ok2:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and self.mouse:
                self.pressed = True

            if self.pressed and pygame.mouse.get_pressed()[0] == 0:
                self.clicked = True
                self.mouse = False
                self.pressed = False
                ii = 3
                return self.name

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
        global nehezseg
        nehezseg=0
        self.defes_tomb = [self.menu, self.pakli, self.harc, self.harc, self.harc, self.kilepes, self.igen, self.jobb_, self.bal_, self.fomenu, self.jatekmester,self.jobb_g,self.bal_g, self.jatek, self.vissza_, self.mentes, self.lement, self.uj]
        #18 drb
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

    def automatapakli(self):
        global autopakli
        autopakli=[]
        mindennovekvo=[]
        for nev,kartya in self.player.collection.items():
            heapq.heappush(mindennovekvo, (1/(kartya.col_damage*kartya.col_hp), kartya))
        for _ in range(len(self.player.collection)//2):
            _, nev = heapq.heappop(mindennovekvo)
            autopakli.append(nev)

    def run_battle(self, dungeon_name: str, test = True) -> List[str]:
        global harclog
        global nehezseg

        harclog=[]
        #if not test:
        #    nehezseg=int(input("nehezsegi szint (1-10) "))
        if dungeon_name not in self.dungeons:
            if test:
                return [f"error;nem_letezik_kazamata;{dungeon_name}"]
            else:
                harclog.append('Nem létezik ilyen kazamata')
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
            pass
        # initial play actions (kijatszik) for both sides when their card enters play
        # --- 5. Első kör kijátszásai
        round_no = 1
        if not test:
            harclog.append(f"{round_no}.kor")
        enemy_next_kijatsz=False
        if enemy_cards:
            e = enemy_cards[0]
            line = f"{round_no}.kor;kazamata;kijatszik;{e.name};{e.damage};{e.hp};{e.type}"
            logs.append(line)
            if not test:
                harclog.append(f"k;k;{e.name}")
                # harclog.append(f"👹 A kazamata kijátszotta: {e.name} | sebzés: {e.damage}, életerő: {e.hp}, típus: {e.type}")
        if player_deck:
            p = player_deck[0]
            line = f"{round_no}.kor;jatekos;kijatszik;{p.name};{p.damage};{p.hp};{p.type}"
            logs.append(line)
            if not test:
                harclog.append(f"j;k;{p.name}")
                # harclog.append(f"🧙‍♂️ A játékos kijátszotta: {p.name} | sebzés: {p.damage}, életerő: {p.hp}, típus: {p.type}")

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
                harclog.append(f"{round_no}.kor")
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
                        harclog.append(f"k;t;{attacker_e.name};{defender_p.name};{dmg};{defender_p.hp}")
            else:
                # új ellenség kijátszása
                new_enemy = enemy_cards[enemy_index]
                enemy_next_kijatsz = False
                line = f"{round_no}.kor;kazamata;kijatszik;{new_enemy.name};{new_enemy.damage};{new_enemy.hp};{new_enemy.type}"
                logs.append(line)
                if not test:
                    harclog.append(f"k;k;{new_enemy.name}")
            # --- Ha a játékos kártyája meghalt ---
            if defender_p.hp <= 0:
                player_index += 1
                if player_index >= len(player_deck):
                    logs.append("jatekos vesztett")
                    if not test:
                        harclog.append("j;v")
                    return logs
                # új kártya kijátszása
                new_card = player_deck[player_index]
                line = f"{round_no}.kor;jatekos;kijatszik;{new_card.name};{new_card.damage};{new_card.hp};{new_card.type}"
                logs.append(line)
                if not test:
                    harclog.append(f"j;k;{new_card.name}")
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
                harclog.append(f"j;t;{attacker_p.name};{defender_e.name};{dmg2};{defender_e.hp}")
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
                            harclog.append(f"j;n;{player_deck[player_index].name};h")
                    elif d.reward=="sebzes":
                        if self.player.collection[player_deck[player_index].name].col_damage<100:
                            self.player.collection[player_deck[player_index].name].col_damage+=1
                        if not test:
                            harclog.append(f"j;n;{player_deck[player_index].name};s")
                    else:
                        if not test:
                            harclog.append(f"j;n;{uj}")
                    return logs
        if not test:
            return harclog



        # Ha ide jut, valami hiba
        if not alive(player_deck):
            logs.append("jatekos vesztett")
        elif not alive(enemy_cards):
            logs.append("jatekos nyert")
        else:
            logs.append("error;ismeretlen_allapot")

        return logs
    #0
    def menu(self):
        global tavle
        global k
        global kp
        global szaml
        global ok
        global oszl
        global old
        global old2
        global ii_e
        global harcolte
        global s
        global tav3
        screen.blit(hatter, (0, -150))
        harcolte = False
        ii_e = 1
        old2 = 1
        oszl = 3
        ok = True
        szaml = 0
        tavle = -70
        tav3 = 0
        #screen.fill((195, 150, 99))
        print(self.player.deck_order)
        Pakli_hatter.draw()
        Pakli.draw()

        # Click detection
        Jobb.draw()
        if (len(self.player.deck_order) < 6) or (6 * old > len(self.player.deck_order)):
            Jobb.clicked = True
        else:
            Jobb.clicked = False

        Bal.draw()
        if old == 1:
            Bal.clicked = True
        else:
            Bal.clicked = False

        # Megjeleniti a paklit
        for i in range((old - 1) * 6, len(self.player.deck_order)):
            if i < (old - 1) * 6 + 6:
                #for j in self.player.deck_order:
                if self.player.deck_order[i] in self.world_cards:
                    self.world_cards[self.player.deck_order[i]].draw_pakli(110, self.player.deck_order)
                else:
                    self.leaders[self.player.deck_order[i]].draw_pakli(110, self.player.deck_order)

        # Par rajzolas
        Vissza.draw()
        for i in self.dungeons:
            s = self.dungeons[i].draw_button(i,self.dungeons[i].simple_cards)
            if s != None:
                break

        #Harc1.draw()
        #Harc2.draw()
        #Harc3.draw()

        #print(s)

        for i in self.world_cards:
            self.world_cards[i].clicked = False
    #1
    def pakli(self):
        global tav2
        global tav
        global kp
        global tavle
        global oszl
        global ok
        global szaml
        global old
        global old2
        screen.blit(hatter, (0, -150))
        old = 1
        tavle = -40
        oszl = 7
        szaml = 0
        '''if ok:
            self.player.deck_order = []
            ok = False'''
        #screen.fill((195, 150, 99))
        Uj_pakli_hatter.draw()
        Mentes.draw()
        tav2 = 95
        #for i in kg:
        sz = 0
        Jobb_g.draw()
        if (len(self.player.collection) < 8) or (8 * old2 > len(self.player.collection)-len(self.player.deck_order)-1):
            Jobb_g.clicked = True
        else:
            Jobb_g.clicked = False

        Bal_g.draw()
        if old2 == 1:
            Bal_g.clicked = True
        else:
            Bal_g.clicked = False

        for j in self.player.collection:
            if j in self.player.deck_order:
                pass
            else:
                sz = sz + 1
                if (sz > (old2 - 1) * 8) and (sz < (old2 - 1) * 8 + 9):
                    if j in self.world_cards:
                        self.player.deck_order = self.world_cards[j].draw_gyujt(self.player.collection, self.player.deck_order)
                    else:
                        self.player.deck_order = self.leaders[j].draw_gyujt(self.player.collection, self.player.deck_order)
        for i in self.player.deck_order:
            if i in self.world_cards:
                self.player.deck_order = self.world_cards[i].draw_pakli(60, self.player.deck_order)
            else:
                self.player.deck_order = self.leaders[i].draw_pakli(60, self.player.deck_order)


    #2,3,4
    def harc(self):
        global ii
        global running
        global harcolte
        global s
        global harclog
        global tav2
        global tav
        global tavle
        global ok
        global szaml
        global tavle
        global k
        global kp
        global ok
        global oszl
        global old
        global old2
        global ii_e
        global szamlalo
        global lepes
        ii_e = 1
        old = 1
        tav2 = 95
        ii_e = 1
        old2 = 1
        oszl = len(self.world_cards)
        ok = True
        szaml = 0
        tavle = 67
        tav = 510

        screen.fill((195, 150, 99))
        kor_font = pygame.font.Font('ByteBounce.ttf', 40)

        # Battle simulation
        if not harcolte:
            self.run_battle(s,False)
            harcolte = True
            print(ii)
            print(harclog)
            print(s)
            print(self.dungeons[s].leader_name)
            szamlalo = 0
            lepes = 1

        #screen.fill((195, 150, 99))
        screen.blit(hatter, (0, -150))

        #kor
        kor = kor_font.render(str(harclog[szamlalo]), True, (195, 150, 99))
        screen.blit(kor,((screen.get_width() - kor.get_width())//2-40, 0))

        # Input detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ii = 0
                if event.key == pygame.K_SPACE:
                    print(lepes)
                    lepes = lepes + 1
                    print(lepes)
                    print(szamlalo)
                    timer = 60 * 2
                    if lepes == 3:
                        szamlalo = szamlalo + 3
                        lepes = 1
                    print(lepes)
                    print(szamlalo)

        ok = True
        
        if lepes == 1:
            jel = harclog[szamlalo+lepes].split(;)
            
            pass
        else:
            pass

        # player's deck battle copies
        player_deck: List[BattleCard] = []
        for nm in self.player.deck_order:
            if nm in self.player.collection:
                player_deck.append(self.player.collection[nm].copy_for_battle())

        for i in player_deck:
            if i.name in self.world_cards:
                self.world_cards[i.name].draw_pakli(370, self.player.deck_order,-1)
            else:
                self.leaders[i.name].draw_pakli(370, self.player.deck_order,-1)

        ii_e = 1
        old = 1
        tav2 = 95
        ii_e = 1
        old2 = 1
        ok = True
        szaml = 0
        tavle = 67
        tav = 510



        d = self.dungeons[s]
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

        for j in enemy_cards:
            if j.name in self.world_cards:
                self.world_cards[j.name].draw_pakli(520, self.world_cards[j.name])
            else:
                self.leaders[j.name].draw_pakli(360, self.leaders[j.name])

        '''for j in self.dungeons[s].simple_cards:
            self.world_cards[j].draw_pakli(520, self.world_cards[j])
        if self.dungeons[s].leader_name != None:
            self.leaders[self.dungeons[s].leader_name].draw_pakli(360, self.leaders[self.dungeons[s].leader_name])'''




    #5
    def kilepes(self):
        Biztos.draw()
        Igen.draw()
        Megsem.draw()
    #6
    def igen(self):
        pygame.quit()
        sys.exit()
    #7
    def jobb_(self):
        global ii
        global old
        old = old + 1
        ii = 0
    #8
    def bal_(self):
        global ii
        global old
        old = old - 1
        ii = 0
    #9
    def fomenu(self):
        global ii_e
        global old3
        global ok2
        global Lista_m
        global text
        screen.blit(hatter,(0,-150))
        text = ''
        Lista_m = []
        old3 = 1
        ii_e = 0
        #screen.fill((195, 150, 99))
        Damareen.draw()
        Jatekos.draw()
        J_mester.draw()
        Kilepes.draw()
        self.player.deck_order = []
        ok2 = False
    #10
    def jatekmester(self):
        #uj kartya, uj dungeon, uj vezerkartya => mentes
        #screen.fill((195,150,99))
        screen.blit(hatter,(0,-150))
        Kartya.draw()
        Kazamata.draw()
        Vezerkartya.draw()
        Vissza.draw()
    #11
    def jobb_g(self):
        global ii
        global old2
        old2 = old2 + 1
        ii = 1
    #12
    def bal_g(self):
        global ii
        global old2
        global nehezseg
        old2 = old2 - 1
        ii = 1
    #13
    def jatek(self):
        global old3
        global ok2
        global kep
        #screen.fill((195, 150, 99))
        screen.blit(hatter, (0, -150))
        Uj_jatek.draw()
        Vissza.draw()

        # Nehezseges cucc
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
        if Nehezseg.container_rect.collidepoint(mouse_pos) and mouse[0]:
            Nehezseg.move_slider(mouse_pos)

        nehezseg = round(Nehezseg.get_value())
        # print(Nehezseg.get_value())

        Nehezseg.draw()
        pygame.display.update()

        if ok2 == False:
            mentett = filenevek('.','jatekos')
            ok2 = True
            for i in mentett:
                Lista_m.append(Mentes_kinyitas(0, 0, kep, 1, i))
        sza = 0
        for i in Lista_m:
            sza = sza + 1
            i.draw(sza)

    #14
    def vissza_(self):
        global ii_e
        global ii
        if ii_e == 1:
            Lement.draw()
            L_igen.draw()
            L_nem.draw()
        else:
            ii = 9

    #15
    def mentes(self):
        global ii
        global text
        global ok_uj
        global nevecske
        if ok_uj:
            Ment_nev.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text)<10:
                            text += event.unicode
            Entry.draw()
            my_font = pygame.font.Font('ByteBounce.ttf', 50)
            text_surface = my_font.render(text, True, (54,10,10))
            screen.blit(text_surface,(360,270))
            Ment.draw()
        else:
            text = nevecske[16:len(nevecske)-4]
            ii = 16

        #mentes
        #ragebait <3 hi hi hi

    def lement(self):
        global ii
        global text
        save_jatekkornyezet(self, ".", f"jatekkornyezetj_{text}.txt", "jatekos")
        ii = 9

    def uj(self):
        global ii
        global ok_uj
        ok_uj = True
        ii = 0

    def kinyit(self, nev):
        global ok_uj
        global nevecske
        ok_uj = False
        nevecske = nev
        self.import_jatekkornyezet(self,nev)
#67
    def export_jatekkornyezet(self, mode: str) -> List[str]:
        lines = []

        # WORLD CARDS
        for name, card in self.world_cards.items():
            lines.append(f"kartya;{name};{card.col_damage};{card.col_hp};{card.type}")

        # LEADER CARDS
        for name, card in self.leaders.items():
            lines.append(f"vezer;{name};{card.source.name};{card.boost}")

        # DUNGEONS
        for dname, d in self.dungeons.items():
            simple = ",".join(d.simple_cards) if d.simple_cards else ""
            leader = d.leader_name if d.leader_name else ""
            reward = d.reward if d.reward else ""
            lines.append(f"kazamata;{d.type};{dname};{simple};{leader};{reward}")

        # PLAYER COLLECTION
        if mode == "jatekos":
            for name, card in self.player.collection.items():
                lines.append(
                    f"jatekoskartya;{name};{card.col_damage};{card.col_hp};{card.type}"
                )

            # PLAYER DECK
            deck = ",".join(self.player.deck_order)
            lines.append(f"pakli;{deck}")

        #NEHEZSEG
        lines.append(f"{nehezseg}")
        return lines

    # pakli;Arin,Liora...
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


def save_jatekkornyezet(game, folder, filename, mode):
    #save_jatekkornyezet(game, ".", f"jatekkornyezet_{nev}.txt", "jatekmester") ezt igy kell behivni!!
    #save_jatekkornyezet(game, ".", f"jatekkornyezet_{nev}.txt", "jatekos")
    lines = game.export_jatekkornyezet(mode)

    if not filename.endswith(".txt"):
        filename += ".txt"

    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as f:
        for ln in lines:
            f.write(ln + "\n")


def filenevek(folder,mode):
    global nevek
    nevek=[]
    if mode=="jatekos":
        for file in os.listdir(folder):
            if file.endswith(".txt"):
                if file[:15]=="jatekkornyezetj":
                    nevek.append(file)
    if mode=="jatekmester":
        for file in os.listdir(folder):
            if file.endswith(".txt"):
                if file[:15]=="jatekkornyezetm":
                    nevek.append(file)
    return nevek

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

    running = True

    while running:

        game.defes_tomb[ii]()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        clock.tick(60)

    """
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
    """


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Használat: python jatek.py <input_folder>  vagy  python jatek.py --ui')
        sys.exit(1)
    if sys.argv[1] == '--ui':
        run_ui()
    else:
        folder = sys.argv[1]
        process_test_folder(folder)


pygame.quit() #67 <3












































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































