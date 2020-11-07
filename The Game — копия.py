import pygame, sys, random

class DogClass(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('stay_1.png')
        
        self.stay = [[pygame.image.load('stay_1.png'),pygame.image.load('stay_2.png')],\
                     [pygame.image.load('stay_down_1.png'),pygame.image.load('stay_down_2.png')],\
                     [pygame.image.load('stay_up_1.png'),pygame.image.load('stay_up_2.png')]]
        self.left = [[pygame.image.load('left_1.png'),pygame.image.load('left_2.png')],\
                     [pygame.image.load('left_down_1.png'),pygame.image.load('left_down_2.png')],\
                     [pygame.image.load('left_up_1.png'),pygame.image.load('left_up_2.png')]]
        self.right = [[pygame.image.load('right_1.png'),pygame.image.load('right_2.png')],\
                     [pygame.image.load('right_down_1.png'),pygame.image.load('right_down_2.png')],\
                     [pygame.image.load('right_up_1.png'),pygame.image.load('right_up_2.png')]]

        self.num = 0
        
        self.rect = self.image.get_rect()
        self.location = self.rect.left, self.rect.top = location
        self.rect.width = 48
        self.rect.height = 84
        self.x_vel, self.y_vel = [0,0]
        self.jump_power = 20
        self.walk_power = 10
        self.gravity = 0.5
        self.onGround = [0,0,0,0]
        self.i = 0
        
        self.live_image = pygame.image.load('hart.png')
        self.lives = 3
        self.not_killed = 60

    def move_x(self):
        self.rect.left += self.x_vel

    def move_y(self):
        for d in dog.onGround:
            if not d:
                self.y_vel -= self.gravity
                break
        self.rect.top -= self.y_vel

    def collide_x(self):
        for p in platforms:
            if pygame.sprite.spritecollide(p, hero, False):
                if self.x_vel > 0:
                    if p.rect.right > self.rect.right > p.rect.left:
                        self.rect.right = p.rect.left
                if self.x_vel < 0:
                    if p.rect.right > self.rect.left > p.rect.left:
                        self.rect.left = p.rect.right

    def collide_y(self):
        self.onGround[self.i] = 0
        for p in platforms:
            if pygame.sprite.spritecollide(p, hero, False):
                if self.y_vel > 0:
                    if p.rect.bottom > self.rect.top > p.rect.top:
                        self.rect.top = p.rect.bottom
                        self.y_vel = 0
                if self.y_vel < 0:
                    if p.rect.bottom > self.rect.bottom > p.rect.top:
                        self.rect.bottom = p.rect.top
                        self.onGround = [1,1,1,1]
                        self.y_vel = 0

    def anim(self):
        self.animGRD = False
        for i in self.onGround:
            if i == 1:
                self.animGRD = True
                break
        if self.x_vel == 0:
            if self.animGRD:
                self.image = self.stay[0][self.num]
            elif self.y_vel < 0:
                self.image = self.stay[1][self.num]
            else:
                self.image = self.stay[2][self.num]
        elif self.x_vel > 0:
            if self.animGRD:
                self.image = self.right[0][self.num]
            elif self.y_vel < 0:
                self.image = self.right[1][self.num]
            else:
                self.image = self.right[2][self.num]
        else:
            if self.animGRD:
                self.image = self.left[0][self.num]
            elif self.y_vel < 0:
                self.image = self.left[1][self.num]
            else:
                self.image = self.left[2][self.num]

class HartClass(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('hart.png')
        self.rect = self.image.get_rect()
        self.rect.center = location

class ShotClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.shooting = False
        self.cloud = [pygame.image.load('cloud_1.png'),pygame.image.load('cloud_2.png')]
        self.shot = [pygame.image.load('shot_1.png'),pygame.image.load('shot_2.png')]
        self.fired = [pygame.image.load('fired_1.png'),pygame.image.load('fired_2.png')]
        self.image = self.cloud[0]
        self.rect = self.image.get_rect()

class PaddleClass(pygame.sprite.Sprite):
    def __init__(self, location, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        
        self.rect = self.image.get_rect()
        self.location = self.rect.left, self.rect.top = location

class Camera():
    def __init__(self):
        global gabarits, everybody, max_x, max_y
        self.rect = pygame.Rect(0,0,gabarits[0],gabarits[1])
        self.gamerect = pygame.Rect(0,0,max_x,max_y)
        self.amplitude = [0,0]

    def fix(self):
        if self.gamerect.left > 0:
            for i in everybody:
                i.rect.left -= self.gamerect.left
            self.gamerect.left = 0
        elif self.gamerect.right < self.rect.right:
            for i in everybody:
                i.rect.right -= self.gamerect.right - self.rect.right
            self.gamerect.right = self.rect.right
            
        if self.gamerect.top > 0:
            for i in everybody:
                i.rect.top -= self.gamerect.top
            self.gamerect.top = 0
        elif self.gamerect.bottom < self.rect.bottom:
            for i in everybody:
                i.rect.bottom -= self.gamerect.bottom - self.rect.bottom
            self.gamerect.bottom = self.rect.bottom

    def move(self):
        self.amplitude[0] = dog.rect.center[0] - self.rect.center[0]
        self.amplitude[1] = dog.rect.center[1] - self.rect.center[1]
        
        self.gamerect.left -= self.amplitude[0]
        self.gamerect.top -= self.amplitude[1]
        
        for items in everybody:
            items.rect.left -= self.amplitude[0]
            items.rect.top -= self.amplitude[1]
            
pygame.init()
gabarits = [864,672]
screen = pygame.display.set_mode(gabarits)
screen_image = pygame.image.load('side.png')
screen_rect = pygame.Rect(0,0,gabarits[0],gabarits[1])
clock = pygame.time.Clock()
dog = DogClass([100,100])
hero = pygame.sprite.Group(dog)
##shot = ShotClass()
##spawn_dots = [[250,150],[950,150],[250,550],[950,550]]
##hart = 0

n = 0
##l = 0
##time_shot = 0
##fired = False

everybody = [dog]

level = [
    '5555555555555555555555',
    '5588888888888888888855',
    '56                  45',
    '56                  45',
    '56                  45',
    '56                  45',
    '56                  45',
    '56                  45',
    '552223           12255',
    '558889           78855',
    '56                  45',
    '56                  45',
    '56                  45',
    '56        1223      45',
    '5522222222555522222255',
    '5555555555555555555555']

Top = pygame.image.load('tiles/Top.png')
TopLeft = pygame.image.load('tiles/TopLeft.png')
TopRight = pygame.image.load('tiles/TopRight.png')
Center = pygame.image.load('tiles/Center.png')
Left = pygame.image.load('tiles/Left.png')
Right = pygame.image.load('tiles/Right.png')
Bottom = pygame.image.load('tiles/Bottom.png')
BottomLeft = pygame.image.load('tiles/BottomLeft.png')
BottomRight = pygame.image.load('tiles/BottomRight.png')

platforms = []
y = 0
max_x = 0
max_y = 0
for p in level:
    x = 0
    for i in p:
        if i == '1':
            pddl = PaddleClass([x,y],TopLeft)
            platforms.append(pddl)
            everybody.append(pddl)
        elif i == '2':
            pddl = PaddleClass([x,y],Top)
            platforms.append(pddl)
            everybody.append(pddl)
        elif i == '3':
            pddl = PaddleClass([x,y],TopRight)
            platforms.append(pddl)
            everybody.append(pddl)
        elif i == '4':
            pddl = PaddleClass([x,y],Left)
            platforms.append(pddl)
            everybody.append(pddl)
        elif i == '5':
            pddl = PaddleClass([x,y],Center)
            platforms.append(pddl)
            everybody.append(pddl)
        elif i == '6':
            pddl = PaddleClass([x,y],Right)
            platforms.append(pddl)
            everybody.append(pddl)
        elif i == '7':
            pddl = PaddleClass([x,y],BottomLeft)
            pddl.rect.height = 33
            platforms.append(pddl)
            everybody.append(pddl)
        elif i == '8':
            pddl = PaddleClass([x,y],Bottom)
            pddl.rect.height = 33
            platforms.append(pddl)
            everybody.append(pddl)
        elif i == '9':
            pddl = PaddleClass([x,y],BottomRight)
            pddl.rect.height = 33
            platforms.append(pddl)
            everybody.append(pddl)
        x += 48
        if x > max_x:
            max_x = x
    y += 48
    max_y = y
cam = Camera()

running = True
while running:
    clock.tick(60)
    screen.blit(screen_image,[0,0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
##        elif event.type == pygame.MOUSEMOTION:
##            shot.rect.center = event.pos
##        elif event.type == pygame.MOUSEBUTTONDOWN:
##            shot.shooting = True
##        elif event.type == pygame.MOUSEBUTTONUP:
##            shot.shooting = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if dog.x_vel < 0:
                    dog.x_vel = 0
            elif event.key == pygame.K_RIGHT:
                if dog.x_vel > 0:
                    dog.x_vel = 0
        elif event.type == pygame.KEYDOWN:                            
            if event.key == pygame.K_LEFT:
                dog.x_vel = -dog.walk_power
            elif event.key == pygame.K_RIGHT:
                dog.x_vel = dog.walk_power
            elif event.key == pygame.K_UP:
                for d in dog.onGround:
                    if d:
                        dog.y_vel = dog.jump_power
                        break
                    
    dog.move_x()
    dog.collide_x()
    dog.move_y()
    dog.collide_y()

    cam.move()
    cam.fix()

    if dog.not_killed:
        dog.not_killed -= 1
    
    dog.i += 1
    if dog.i == 4:
        dog.i = 0
        
    n += 1
    if n == 30:
        n = 0

    if n < 15:
        dog.num = 0
    else:
        dog.num = 1
        
##    l += 1
##    if l == 420:
##        l = 0
##        hart = HartClass(random.choice(spawn_dots))

    dog.anim()
##    if fired:
##        if time_shot > 0:
##            shot.shooting = False
##            time_shot -= 0.25
##            shot.image = shot.fired[dog.num]
##        else:
##            fired = False
##    elif not shot.shooting:
##        if time_shot > 0:
##            time_shot -= 1
##        shot.image = shot.cloud[dog.num]
##    elif time_shot < 120:
##        time_shot += 2
##        shot.image = shot.shot[dog.num]
##    else:
##        fired = True
##        
##
##    if pygame.sprite.spritecollide(shot, hero, False):
##        if shot.shooting and not dog.not_killed:
##            dog.lives -= 1
##            dog.not_killed = 60
##            if dog.lives == 0:
##                running = False
            
##    if hart:
##        if pygame.sprite.spritecollide(hart, hero, False):
##            if dog.lives < 3:
##                dog.lives += 1
##            l = 0
##            hart = 0
##        else:
##            screen.blit(hart.image, hart.rect.topleft)
            
    screen.blit(dog.image, [dog.rect.left-24, dog.rect.top-12])
    for paddle in platforms:
        screen.blit(paddle.image, [paddle.rect.left, paddle.rect.top])
##    x_lives = 950
##    y_lives = 5
##    for lives in range(dog.lives):
##        screen.blit(dog.live_image, [x_lives, y_lives])
##        x_lives += 50
##    screen.blit(shot.image, shot.rect.topleft)
    
    pygame.display.flip()

pygame.quit()
