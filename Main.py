import pygame

pygame.init()

win = pygame.display.set_mode((1200, 600))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
walkUp = [pygame.image.load('U1.png'), pygame.image.load('U2.png'), pygame.image.load('U3.png'),
            pygame.image.load('U4.png'), pygame.image.load('U5.png'), pygame.image.load('U6.png'),
            pygame.image.load('U7.png'), pygame.image.load('U8.png'), pygame.image.load('U9.png')]
walkDown = [pygame.image.load('D1.png'), pygame.image.load('D2.png'), pygame.image.load('D3.png'),
            pygame.image.load('D4.png'), pygame.image.load('D5.png'), pygame.image.load('D6.png'),
            pygame.image.load('D7.png'), pygame.image.load('D8.png'), pygame.image.load('D9.png')]
bg = pygame.image.load('bg.png')


clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('PEW-Sound-effect-Gaming.wav')
hitSound = pygame.mixer.Sound("Bruh-Sound-Effect-2.wav")
death = pygame.mixer.Sound('coffin dance.wav')


class player(object):
    def __init__(self,x ,y ,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x, self.y, 100, 150)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.up:
                win.blit(walkUp[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.down:
                win.blit(walkDown[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            elif self.left:
                win.blit(walkLeft[0], (self.x, self.y))
            elif self.up:
                win.blit(walkUp[0], (self.x, self.y))
            else:
                win.blit(walkDown[0], (self.x, self.y))

        self.hitbox = (self.x, self.y, 100, 150)  # NEW
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # To draw the hit box around the player

    def hit(self):
        death.play()
        self.x = 60
        self.y = 410
        self.walkCount = 0
        pygame.display.update()
        i = 0
        while i < 50000:
            print(i)
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 50001
                    pygame.quit()
        

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('MR1.png'), pygame.image.load('MR2.png'), pygame.image.load('MR3.png'),
                 pygame.image.load('MR4.png'), pygame.image.load('MR5.png'), pygame.image.load('MR6.png'),
                 pygame.image.load('MR7.png'), pygame.image.load('MR8.png'), pygame.image.load('MR9.png'),
                 pygame.image.load('MR10.png'), pygame.image.load('MR11.png')]
    walkLeft = [pygame.image.load('ML1.png'), pygame.image.load('ML2.png'), pygame.image.load('ML3.png'),
                pygame.image.load('ML4.png'), pygame.image.load('ML5.png'), pygame.image.load('ML6.png'),
                pygame.image.load('ML7.png'), pygame.image.load('ML8.png'), pygame.image.load('ML9.png'),
                pygame.image.load('ML10.png'), pygame.image.load('ML11.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]  # This will define where our enemy starts and finishes their path.
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x , self.y , 150, 150)
        self.health = 10  # NEW
        self.visible = True  # NEW

    def draw(self, win):
        self.move()
        if self.visible:  # NEW
            if self.walkCount + 1 >= 33:  # Since we have 11 images for each animtion our upper bound is 33.
                # We will show each image for 3 frames. 3 x 11 = 33.
                self.walkCount = 0

            if self.vel > 0:  # If we are moving to the right we will display our walkRight images
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:  # Otherwise we will display the walkLeft images
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            self.hitbox = (self.x, self.y, 150, 150)  # NEW

            pygame.draw.rect(win, (0, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # Draws the hit box around the enemy



    def move(self):
        if self.vel > 0:  # If we are moving right
            if self.x < self.path[1] + self.vel:  # If we have not reached the furthest right point on our path.
                self.x += self.vel
            else:  # Change direction and move back the other way
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:  # If we are moving left
            if self.x > self.path[0] - self.vel:  # If we have not reached the furthest left point on our path
                self.x += self.vel
            else:  # Change direction
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

    def hit(self): # ALL NEW
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')

def BomWindow():
    win.blit(bg, (0, 0))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


# mainloop
man = player(200, 450, 100, 150)
goblin = enemy(0, 150, 150, 150, 1200)
shootLoop = 0
bullets = [] # This goes right above the while loop
run = True
while run:
    clock.tick(27)

    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
            man.hit()

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if goblin.visible == True:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    hitSound.play()
                    goblin.hit()
                    bullets.pop(bullets.index(bullet))

    for bullet in bullets:
        if man.left:
            bullet.x += bullet.vel
        elif man.right:
            bullet.x += bullet.vel
        elif man.up:
            bullet.y += bullet.vel
        elif man.down:
            bullet.y += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))  # This will remove the bullet if it is off the screen

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -3
        elif man.left:
            facing = 3
        elif man.up:
            facing = -3
        else:
            facing = 3


        if len(bullets) < 100:
            if man.right:
                bullets.append(projectile(round(man.x + man.width + 10), round(man.y + man.height-55), 6, (0, 0, 0), facing))
            elif man.left:
                bullets.append(projectile(round(man.x + man.width - 110), round(man.y + man.height - 55), 6, (0, 0, 0), facing))
            elif man.up:
                bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height - 155), 6, (0, 0, 0), facing))
            else:
                bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height-50), 6, (0, 0, 0), facing))

        shootLoop = 1


    if keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.up = False
        man.down = False
        man.standing = False  # NEW
    elif keys[pygame.K_RIGHT] and man.x < 1100:
        man.x += man.vel
        man.right = True
        man.left = False
        man.up = False
        man.down = False
        man.standing = False  # NEW
    elif keys[pygame.K_UP] and man.y > 0:
        man.y -= man.vel
        man.right = False
        man.left = False
        man.up = True
        man.down = False
        man.standing = False  # NEW
    elif keys[pygame.K_DOWN] and man.y < 445:
        man.y += man.vel
        man.right = False
        man.left = False
        man.up = False
        man.down = True
        man.standing = False  # NEW
    else:
        man.standing = True  # NEW (r# emoved two lines)
        man.walkCount = 0


    BomWindow()

pygame.quit()
