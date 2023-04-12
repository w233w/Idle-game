import pygame
from pygame.mask import from_surface
from pygame.math import Vector2

# 各类参数
# 窗口大小
WIDTH = 400
HEIGHT = 600
SIZE = WIDTH, HEIGHT
HEADLINE = 40
# 刷新率
FPS = 1000
# 颜色
BackgroundColor = 255, 229, 204
Black = 0, 0, 0
White = 255, 255, 255
Red = 255, 0, 0
Green = 0, 255, 0
Blue = 0, 0, 255

class Main_Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([100,100])
        self.image.fill(pygame.Color(Red))
        self.pos = Vector2(200,200)
        self.rect = self.image.get_rect(center=self.pos)
        self.clicked = False

    def update(self, pos, type):
        global money
        self.clicked = self.rect.collidepoint(pos)
        if self.clicked and type == 1:
            money += earn_by_click
            self.image.fill(pygame.Color(Black))
        else:
            self.image.fill(pygame.Color(Red))

class Upgrade_Button1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("button1.png")
        self.pos = Vector2(50,50)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = from_surface(self.image)
        self.clicked = False
        self.cost = 10
        self.level = 1
        self.level_up_reward = 1
        self.cost_info = Font_Small.render(f"Cost: {self.cost}", False, White)
        self.lv_info = Font_Small.render(f"Level: {self.level}", False, Green)
    
    def update(self, pos, type):
        global money, earn_by_click
        self.info = Font_Small.render(f"Cost: {self.cost}", False, White)
        self.lv_info = Font_Small.render(f"Level: {self.level}", False, Green)
        try:
            self.clicked = self.mask.get_at([x-y for x,y in zip(pos, [0, 25])]) == 1
        except:
            self.clicked = False
        if self.clicked and type == 1:
            if money >= self.cost:
                money -= self.cost
                earn_by_click += self.level_up_reward
                self.cost = int(self.cost*1.1)
                self.level += 1
            self.image = pygame.image.load("button2.png")
        else:
            self.image = pygame.image.load("button1.png")
        self.image.blit(self.info, (16,5))
        self.image.blit(self.lv_info, (16,25))

class Auto_Button1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("button1.png")
        self.pos = Vector2(50,125)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = from_surface(self.image)
        self.clicked = False
        self.cost = 10
        self.level = 0
        self.level_up_reward = 1
        self.cost_info = Font_Small.render(f"Cost: {self.cost}", False, White)
        self.lv_info = Font_Small.render(f"Level: {self.level}", False, Green)
    
    def update(self, pos, type):
        global money, earn_by_auto, is_auto, last_auto_gain
        self.info = Font_Small.render(f"Cost: {self.cost}", False, White)
        self.lv_info = Font_Small.render(f"Level: {self.level}", False, Green)
        try:
            self.clicked = self.mask.get_at([x-y for x,y in zip(pos, [0, 100])]) == 1
        except:
            self.clicked = False
        if self.clicked and type == 1:
            if not is_auto:
                is_auto = True
                last_auto_gain = pygame.time.get_ticks()
            if money >= self.cost:
                money -= self.cost
                earn_by_auto += self.level_up_reward
                self.cost = int(self.cost*1.3)
                self.level += 1
            self.image = pygame.image.load("button2.png")
        else:
            self.image = pygame.image.load("button1.png")
        self.image.blit(self.info, (16,5))
        self.image.blit(self.lv_info, (16,25))

# Init pygame & Crate screen
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("测试")
clock = pygame.time.Clock()

# 状态栏
# setting the pygame font style(1st parameter)
# and size of font(2nd parameter)
Font_Large = pygame.font.SysFont('timesnewroman',  30)    
Font_Medium = pygame.font.SysFont('timesnewroman',  20)               
Font_Small = pygame.font.SysFont('timesnewroman',  15)

button = pygame.sprite.Group()
button.add(Main_Button())
a = Upgrade_Button1()
button.add(a)
button.add(Auto_Button1())

# init stats
money = 0
earn_by_click = 1
earn_by_auto = 0
last_auto_gain = 0
is_auto = False


running = True
while running:
    # 点×时退出。。
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            button.update(pygame.mouse.get_pos(), 1)
        else:
            button.update(pygame.mouse.get_pos(), 2)
    # 每一秒增加一次钱        
    if is_auto and pygame.time.get_ticks() - last_auto_gain > 1000:
        last_auto_gain = pygame.time.get_ticks()
        money += earn_by_auto
    Info1 = Font_Large.render(f"$:{money}", False, Red, BackgroundColor)
    screen.fill(pygame.Color(BackgroundColor))
    screen.blit(Info1, (180, 0))
    Discribetion1 = Font_Medium.render("Level up click", False, Black)
    screen.blit(Discribetion1, Vector2(0, 0))
    Discribetion1 = Font_Medium.render("Level up auto", False, Black)
    screen.blit(Discribetion1, Vector2(0, 75))
    button.draw(screen)
    pygame.display.flip()