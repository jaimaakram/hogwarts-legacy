import pygame
pygame.init()

window = pygame.display.set_mode((800,550))
name = pygame.display.set_caption("Hogwarts Legacy")

walkLeft = [pygame.image.load("L1.png"), pygame.image.load("L2.png"), pygame.image.load("L3.png"), pygame.image.load("L4.png"), pygame.image.load("L5.png"), pygame.image.load("L6.png"), pygame.image.load("L7.png"), pygame.image.load("L8.png")]
walkRight = [pygame.image.load("R1.png"), pygame.image.load("R2.png"), pygame.image.load("R3.png"), pygame.image.load("R4.png"), pygame.image.load("R5.png"), pygame.image.load("R6.png"), pygame.image.load("R7.png"), pygame.image.load("R8.png")]
bg = pygame.image.load("bg.jpg")
idleR = pygame.image.load("idleR.png")
idleL = pygame.image.load("idleL.png")

BulletSound = pygame.mixer.Sound("Bullet.mp3")
BulletSound.set_volume(0.05)
CollisionSound = pygame.mixer.Sound("Collision.mp3")
CollisionSound.set_volume(0.05)

Music = pygame.mixer.music.load("BackgroundMusic.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)


clock = pygame.time.Clock()

score = 0

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.left = False
        self.right = False
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 10, self.y,50,80)

    def draw(self, window):
        if self.walkCount + 1 >= 24:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                window.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                window.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.left:
                window.blit(idleL, (self.x,self.y))
            else:
                window.blit(idleR, (self.x,self.y))
        self.hitbox = (self.x + 10, self.y,50,80)       
        #pygame.draw.rect(window, (255,0,0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 200
        self.y = 290
        self.walkCount = 0
        font1 = pygame.font.SysFont("comicsans", 100)
        text = font1.render("-5", 1, (161, 2, 2))
        window.blit(text, (400 - (text.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

        

class projectile(object):
    def __init__(self, x, y, radius, colour, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.facing = facing
        self.velocity = 7.5 * facing

    def draw(self, window):
        pygame.draw.circle(window, self.colour, (self.x, self.y), self.radius)


class enemy(object):

    walkLeft = [pygame.image.load("LE1.png"), pygame.image.load("LE2.png"), pygame.image.load("LE3.png"), pygame.image.load("LE4.png"), pygame.image.load("LE5.png"), pygame.image.load("LE6.png"), pygame.image.load("LE7.png")]
    walkRight = [pygame.image.load("RE1.png"), pygame.image.load("RE2.png"), pygame.image.load("RE3.png"), pygame.image.load("RE4.png"), pygame.image.load("RE5.png"), pygame.image.load("RE6.png"), pygame.image.load("RE7.png")]


    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 3
        self.path = [x, end]
        self.walkCount = 0
        self.hitbox = (self.x + 10, self.y + 40,85,90)
        self.health = 9
        self.visible = True

    def draw(self, window):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 21:
                self.walkCount = 0
            if self.velocity > 0:
                window.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            else:
                window.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            self.hitbox = (self.x + 10, self.y + 40,85,90)
            pygame.draw.rect(window, (199, 43, 0), (self.hitbox[0],self.hitbox[1] -12, 75,10))
            pygame.draw.rect(window, (0, 194, 61), (self.hitbox[0],self.hitbox[1] -12, 75 - (8 * (9 - self.health)),10))
        #pygame.draw.rect(window, (255,0,0), self.hitbox, 2)
        

    def move(self):
        if self.velocity > 0:
            if self.x < self.path[1] + self.velocity:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.x += self.velocity
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.velocity:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.x += self.velocity
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print("hit")

        

def redrawGameWindow():
    window.blit(bg, (0,0))
    text = font.render("Score: " + str(score),1, (0,0,0))
    window.blit(text, (620,10))
    wizard.draw(window)
    DarkLord.draw(window)
    for bullet in bullets:
        bullet.draw(window)
    pygame.display.update()
    
font = pygame.font.SysFont("comicsans", 30, True)
wizard = Player(200, 290, 64, 64)
DarkLord = enemy(300, 240, 109, 109, 600)
shootLoop = 0
bullets = []
run = True
while run:
    
    clock.tick(24)
    if DarkLord.visible == True:
        if wizard.hitbox[1] < DarkLord.hitbox[1] + DarkLord.hitbox[3] and wizard.hitbox[1] + wizard.hitbox[3] > DarkLord.hitbox[1]:
                if wizard.hitbox[0] + wizard.hitbox[2] > DarkLord.hitbox[0] and wizard.hitbox[0] < DarkLord.hitbox[0] + DarkLord.hitbox[2]:
                    wizard.hit()
                    score -= 5
                
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for bullet in bullets:
        if bullet.y - bullet.radius < DarkLord.hitbox[1] + DarkLord.hitbox[3] and bullet.y + bullet.radius > DarkLord.hitbox[1]:
            if bullet.x + bullet.radius > DarkLord.hitbox[0] and bullet.x - bullet.radius < DarkLord.hitbox[0] + DarkLord.hitbox[2]:
                CollisionSound.play()
                DarkLord.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
                
        if bullet.x < 800 and bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] and shootLoop == 0:
        BulletSound.play()
        if wizard.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 7.5:
            bullets.append(projectile (round(wizard.x + wizard.width // 2), round(wizard.y + wizard.height // 2), 6, (102,0,0), facing ))
        shootLoop = 1
        
    if keys[pygame.K_LEFT] and wizard.x > 0 :
        wizard.x -= wizard.velocity
        wizard.left = True
        wizard.right = False
        wizard.standing = False
    elif keys[pygame.K_RIGHT] and wizard.x < 800 - wizard.width:
        wizard.x += wizard.velocity
        wizard.right = True
        wizard.left = False
        wizard.standing = False
    else:
        wizard.standing = True
        wizard.walkCount = 0
        
    if not(wizard.isJump):
        if keys[pygame.K_UP]:
            wizard.isJump = True
            wizard.right = False
            wizard.left = False
            wizard.walkCount = 0
    else:
        if wizard.jumpCount >= -10:
            neg = 1
            if wizard.jumpCount < 0:
                neg = -1
            wizard.y -= (wizard.jumpCount ** 2) * 0.5 * neg
            wizard.jumpCount -= 1
        else:
            wizard.isJump = False
            wizard.jumpCount = 10
    redrawGameWindow()

pygame.quit()




