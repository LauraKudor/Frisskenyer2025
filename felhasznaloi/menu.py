import pygame
pygame.font.init()

screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption("Damareen")

def menu():
    global tavle
    global tav
    global k
    global kp
    global szaml
    global ok
    global oszl
    global old
    oszl = 3
    ok = True
    szaml = 0
    tavle = -70
    screen.fill((195,150,99))
    Pakli_hatter.draw()
    Pakli.draw()
    Jobb.draw()
    if (len(kp)<6)or (6*old>len(kp)):
        Jobb.clicked = True
    else:
        Jobb.clicked = False
    Bal.draw()
    if old==1:
        Bal.clicked = True
    else:
        Bal.clicked = False
    for i in range((old-1)*6,len(kp)):
        if i<(old-1)*6+6:
            for j in k:
                if j.nev == kp[i]:
                    j.draw_pakli(110)
    Kilepes.draw()
    Harc1.draw()
    Harc2.draw()
    Harc3.draw()
    for i in k:
        i.clicked = False


def pakli():
    global tav2
    global tav
    global kp
    global tavle
    global oszl
    global ok
    global szaml
    global old
    old = 1
    tavle = -40
    oszl = 7
    szaml = 0
    if ok:
        kp = []
        ok = False
    screen.fill((195,150,99))
    Uj_pakli_hatter.draw()
    Mentes.draw()
    tav2 = 20
    for i in kg:
        for j in k:
            if (j.nev == i)and(i not in kp):
                j.draw_gyujt()
    for i in kp:
        for j in k:
            if j.nev == i:
                j.draw_pakli(60)

def harc1():
    global ii
    global running
    screen.fill((195,150,99))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ii = 0



def harc2():
    global ii
    global running
    screen.fill((195, 150, 99))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ii = 0

def harc3():
    global ii
    global running
    screen.fill((195, 150, 99))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ii = 0

def kilepes():
    Biztos.draw()
    Igen.draw()
    Megsem.draw()

def igen():
    global running
    running = False

def jobb_():
    global old
    global ii
    old = old+1
    ii = 0

def bal_():
    global old
    global ii
    old = old-1
    ii = 0

ii = 0
defes_tomb = [menu, pakli, harc1, harc2, harc3, kilepes, igen, jobb_, bal_]


kg = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14']
kp = []
szaml = 0
sorok = 0
ok = True
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

jobbra = pygame.image.load("nyil_j.png").convert()
balra = pygame.image.load("nyil_b.png").convert()

#hatterek
biztos = pygame.image.load("biztos.png").convert()
pakli_hatter = pygame.image.load("pakli_keret.png").convert()
uj_pakli_hatter = pygame.image.load("uj_pakli_keret.png").convert()

#kartyak
kartya1 = pygame.image.load("kartya.png").convert()
kartya2 = pygame.image.load("kartya.png").convert()
kartya3 = pygame.image.load("kartya.png").convert()
kartya4 = pygame.image.load("kartya.png").convert()
kartya5 = pygame.image.load("kartya.png").convert()
kartya6 = pygame.image.load("kartya.png").convert()
kartya7 = pygame.image.load("kartya.png").convert()
kartya8 = pygame.image.load("kartya.png").convert()

class Kartyak:
    def __init__(self,x,y,kep,scale,nev, sebzes, hp):
        self.sebzes = sebzes
        self.hp = hp
        self.clicked = False
        self.mouse = False
        self.pressed = False
        self.nev = nev
        self.x = x
        self.y = y
        heigth = kep.get_height()
        width = kep.get_width()
        self.kep = pygame.transform.scale(kep, (int(width * scale), int(heigth * scale)))

    def draw_pakli(self,tav_be):
        global tav
        global szaml
        global tavle
        global oszl
        szaml = szaml+1
        if szaml % oszl == 1:
            tavle = tavle + 140
            tav = tav_be
        self.x = tav
        self.y = tavle
        screen.blit(self.kep, (self.x, self.y))
        text_s = font.render(str(self.sebzes), True, (90, 30, 10))
        text_hp = font.render(str(self.hp), True, (90, 30, 10))
        screen.blit(text_s, (self.x + 43, self.y + 42))
        screen.blit(text_hp, (self.x + 43, self.y + 75))
        tav = tav + 100
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
                    kp.remove(self.nev)
                    self.mouse = False
                    self.pressed = False


    def draw_gyujt(self):
        global tav2
        global font
        self.y = 450
        self.x = tav2
        screen.blit(self.kep, (self.x, self.y))
        text_s = font.render(str(self.sebzes), True, (90, 30, 10))
        text_hp = font.render(str(self.hp), True, (90, 30, 10))
        screen.blit(text_s, (self.x + 43, self.y + 42))
        screen.blit(text_hp, (self.x + 43, self.y + 75))

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

        if ok1 and ok2:
            if self.pressed and pygame.mouse.get_pressed()[0] == 0:
                if (len(kp)+1) <= len(kg) // 2:

                    kp.append(self.nev)
                    self.clicked = True
                    self.mouse = False
                    self.pressed = False




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

#gombok
Pakli = Gombok(80, 463, pakli, 0.95, 'pakli', 1)
Harc1 = Gombok(500,0,harc1, 1,'harc1',2)
Harc2 = Gombok(500,200,harc2, 1,'harc2',3)
Harc3 = Gombok(500,400,harc3, 1,'harc3',4)
Kilepes = Gombok(20, 530, kilepes, 0.9, 'kilepes', 5)
Igen = Gombok(510, 310, igen, 1, 'igen', 6)
Megsem = Gombok(340, 310, megsem, 1, 'megsem', 0)
Mentes = Gombok(400, 350, mentes, 0.8, 'mentes', 0)
Jobb = Gombok(265,400,jobbra,1,'jobb',7)
Bal = Gombok(205,400,balra,1,'bal',8)

#hatterek
Biztos = Ablakok(300,170, biztos,1)
Pakli_hatter = Ablakok(70, 20, pakli_hatter, 1)
Uj_pakli_hatter = Ablakok(30,40,uj_pakli_hatter, 1)

#kartyak
Kartya1 = Kartyak(0,0,kartya1,1,'1',100,2)
Kartya2 = Kartyak(0,0,kartya2,1,'2',4,2)
Kartya3 = Kartyak(0,0,kartya3,1,'3',2,4)
Kartya4 = Kartyak(0,0,kartya4,1,'4',3,3)
Kartya5 = Kartyak(0,0,kartya5,1,'5',2,2)
Kartya6 = Kartyak(0,0,kartya6,1,'6',3,2)
Kartya7 = Kartyak(0,0,kartya7,1,'7',2,3)
Kartya8 = Kartyak(0,0,kartya8,1,'8',12,3)
Kartya9 = Kartyak(0,0,kartya8,1,'9',3,20)

k = [Kartya1, Kartya2, Kartya3, Kartya4, Kartya5, Kartya6, Kartya7, Kartya8, Kartya9]
tav = 0
tav2 = 0
oszl = 0
old = 1
font = pygame.font.Font('freesansbold.ttf', 25)

running = True

while running:

    defes_tomb[ii]()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()