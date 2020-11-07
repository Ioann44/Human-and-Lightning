import pygame, sys, random, socket

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

    def update(self):
        global n
                    
        self.move_x()
        self.collide_x()
        self.move_y()
        self.collide_y()
        if self.not_killed:
            self.not_killed -= 1
        self.i += 1
        if self.i == 4:
            self.i = 0  
        n += 1
        if n == 30:
            n = 0
        if n < 15:
            self.num = 0
        else:
            self.num = 1
        self.anim()

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

    def update(self):
        global fired, time_shot
        if fired:
            if time_shot > 0:
                self.shooting = False
                time_shot -= 0.25
                self.image = self.fired[dog.num]
            else:
                fired = False
        elif not self.shooting:
            if time_shot > 0:
                time_shot -= 1
            self.image = self.cloud[dog.num]
        elif time_shot < 120:
            time_shot += 2
            self.image = self.shot[dog.num]
        else:
            fired = True

class PaddleClass(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)

        image_surface = pygame.surface.Surface([100,100])
        image_surface.fill([100,100,100])
        pygame.draw.rect(image_surface, (0,0,0), [0,0,100,100], 10)
        self.image = image_surface.convert()
        
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

    def update(self):
        self.move()
        self.fix()

def read(msg, num):
    info = []
    for j in range(num):
        info.append(0)
    num_msg = 0#before was 'n'
    minus = False
    message = ''
    for i in msg:
        if i == ' ':
            if message == 'True':
                info[num_msg] = True
            elif message == 'False':
                info[num_msg] = False
            else:
                info[num_msg] = float((message))
                if info[num_msg] == int(info[num_msg]):
                    info[num_msg] = int(info[num_msg])
                if minus:
                    info[num_msg] = -info[num_msg]
            message = ''
            num_msg += 1
            minus = False
        elif i == '-':
            minus = True
        else:
            message = message + i
    return info

def shooter():
    global shot, dog, running, sock, hart, hart_n
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            going = False
            sock.close()
            print 'socket closed'
        elif event.type == pygame.MOUSEMOTION:
            shot.rect.center = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            shot.shooting = True
        elif event.type == pygame.MOUSEBUTTONUP:
            shot.shooting = False

    message = str(shot.shooting)+' '+str(shot.rect.left)+' '\
              +str(shot.rect.top)+' '
    sock.send(message)

    taked_message = read(sock.recv(1024),5)
    dog.rect.left, dog.rect.top ,dog.x_vel, dog.y_vel, hart_n = taked_message
    if hart_n == 4:
        hart = False
    else:
        hart = HartClass(spawn_dots[hart_n])

def jumper():
    global dog, shot, running, sock, hart, hart_n
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            going = False
            sock.close()
            print 'socket closed'
        if event.type == pygame.KEYUP:#was 'elif'
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
    taked_message = read((sock.recv(1024)),4)
    shot.shooting, shot.rect.left, shot.rect.top, hart_n = taked_message
    message = str(dog.rect.left)+' '+str(dog.rect.top)+' '+\
              str(dog.x_vel)+' '+str(dog.y_vel)+' '
    sock.send(message)
    if hart_n == 4:
        hart = False
    else:
        hart = HartClass(spawn_dots[hart_n])

def game():
    global game_mode,l,hart,platforms,running
    running = True
    while running:
        clock.tick(60)
        screen.fill([0,170,0])

        if game_mode:
            jumper()
        else:
            shooter()

    ##    cam.update()

        dog.update()
        shot.update()

        if pygame.sprite.spritecollide(shot, hero, False):
            if shot.shooting and not dog.not_killed:
                dog.lives -= 1
                dog.not_killed = 60
                if dog.lives == 0:
                    running = False
                
        if hart:
            if pygame.sprite.spritecollide(hart, hero, False):
                if dog.lives < 3:
                    dog.lives += 1
                l = 0
                hart = 0
            else:
                screen.blit(hart.image, hart.rect.topleft)
                
        screen.blit(dog.image, [dog.rect.left, dog.rect.top])
        for paddle in platforms:
            screen.blit(paddle.image, [paddle.rect.left, paddle.rect.top])
        x_lives = 950
        y_lives = 105
        for lives in range(dog.lives):
            screen.blit(dog.live_image, [x_lives, y_lives])
            x_lives += 50
        screen.blit(shot.image, shot.rect.topleft)
        
        pygame.display.flip()
            
pygame.init()
gabarits = [1200,900]
screen = pygame.display.set_mode(gabarits)
screen_rect = pygame.Rect(0,0,gabarits[0],gabarits[1])
clock = pygame.time.Clock()
dog = DogClass([100,100])
hero = pygame.sprite.Group(dog)
shot = ShotClass()
spawn_dots = [[250,250],[950,250],[250,650],[950,650]]
hart = 0
going = True

font = pygame.font.Font(None, 100)
change_surf = font.render('Change of players...', 1, (255,255,255))

n = 0
time_shot = 0
fired = False

everybody = [dog]

level = [
    '------------',
    '-          -',
    '-          -',
    '-          -',
    '---     ----',
    '-          -',
    '-          -',
    '-    --    -',
    '------------']

platforms = []
y = 0
max_x = 0
max_y = 0
for p in level:
    x = 0
    for i in p:
        if i == '-':
            pddl = PaddleClass([x,y])
            platforms.append(pddl)
            everybody.append(pddl)
            if pddl.rect.right > max_x:
                max_x = pddl.rect.right
            if pddl.rect.bottom > max_y:
                max_y = pddl.rect.bottom
        x += 100
    y += 100
cam = Camera()

sock = socket.socket()
sock.connect(('192.168.0.104', 7777))
game_mode = False

while going and sock:
    dog.lives = 3
    game()
    if game_mode:
        game_mode = False
    else:
        game_mode = True
    shot.shooting = False
    dog.not_killed = 60
    screen.blit(change_surf, [gabarits[0]/2-change_surf.get_width()/2,\
                              gabarits[1]/2-change_surf.get_height()])
    pygame.display.flip()
    pygame.time.delay(1000)
        
pygame.quit()
