import pygame
pygame.init()

screen_width = 700
screen_height = 480

window = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Street Fighter")

idle = [pygame.image.load('idle1.png'), pygame.image.load('idle2.png'),
        pygame.image.load('idle3.png'), pygame.image.load('idle4.png')]

idle_left = [pygame.image.load('idleleft1.png')]


walk_right = [pygame.image.load('walking1.png'), pygame.image.load('walking2.png'),
           pygame.image.load('walking3.png'), pygame.image.load('walking4.png')]

walk_left = [pygame.image.load('walkleft1.png'), pygame.image.load('walkleft2.png'),
           pygame.image.load('walkleft3.png'), pygame.image.load('walkleft4.png')]

idle2 = [pygame.image.load('idle_1.png')]

idle_left2 = [pygame.image.load('idle_left1.png')]

walk_right2 = [pygame.image.load('walk_right1.png'), pygame.image.load('walk_right2.png'),
           pygame.image.load('walk_right3.png'), pygame.image.load('walk_right4.png'),
               pygame.image.load('walk_right5.png')]

walk_left2 = [pygame.image.load('walk_left1.png'), pygame.image.load('walk_left2.png'),
           pygame.image.load('walk_left3.png'), pygame.image.load('walk_left4.png'),
               pygame.image.load('walk_left5.png')]

jump = [pygame.image.load('jump1.png'), pygame.image.load('jump2.png')]

punch = [pygame.image.load('punch1.png'), pygame.image.load('punchleft.png'), pygame.image.load('punch2.png')]

fireball = [pygame.image.load('fireball.png')]

fireball_left = [pygame.image.load('fireballleft.png')]

background = pygame.image.load('bg.jpg')

fireball_sound = pygame.mixer.Sound('bullet.wav')
hit_sound = pygame.mixer.Sound('hit.wav')

clock = pygame.time.Clock()

player_total_sprite = 12

fireball_speed = 8


class Player1(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = True
        self.walk_count = 0
        self.standing = True
        self.health = 10
        self.hit_box = (self.x + -2, self.y + 2, 82, 190)
        self.punching = False
        self.punching_left = False

    def draw(self, window):
        if self.walk_count + 1 >= player_total_sprite:
            self.walk_count = 0

        if not self.standing:
            if self.left:
                window.blit(walk_left[self.walk_count // 3], (self.x, self.y))  # // 3 for smooth animation
                self.walk_count += 1
            elif self.right:
                window.blit(walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.right:
                window.blit(idle[0], (self.x, self.y))
            elif self.left:
                window.blit(idle_left[0], (self.x, self.y))

        if self.punching:
            window.blit(punch[0], (self.x, self.y))

        pygame.draw.rect(window, (255, 0, 0), (self.hit_box[0], self.hit_box[1] - 20, 70, 10))
        pygame.draw.rect(window, (0, 128, 0),
                         (self.hit_box[0], self.hit_box[1] - 20, 70 - (5 * (10 - self.health)), 10))

        self.hit_box = (self.x + -2, self.y + 2, 82, 190)

        pygame.draw.rect(window, (255, 0, 0), self.hit_box, 2)


class Player2(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = True
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.hit_box = (self.x + -2, self.y + 2, 82, 190)
        self.health = 10

    def draw(self, window):
        if self.walk_count + 1 >= player_total_sprite:
            self.walk_count = 0

        if not self.standing:
            if self.left:
                window.blit(walk_left2[self.walk_count // 3], (self.x, self.y))  # // 3 for smooth animation
                self.walk_count += 1
            elif self.right:
                window.blit(walk_right2[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.right:
                window.blit(idle2[0], (self.x, self.y))
            elif self.left:
                window.blit(idle_left2[0], (self.x, self.y))

        pygame.draw.rect(window, (255, 0, 0), (self.hit_box[0], self.hit_box[1] - 20, 70, 10))
        pygame.draw.rect(window, (0, 128, 0),
                         (self.hit_box[0], self.hit_box[1] - 20, 70 - (5 * (10 - self.health)), 10))

        self.hit_box = (self.x + -2, self.y + 2, 82, 190)
        pygame.draw.rect(window, (255, 0, 0), self.hit_box, 2)

    def hit(self):
        if self.health > 1:
            self.health -= 1


class Fireball(object):
    def __init__(self, x, y, radius, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = facing
        self.velocity = fireball_speed * facing
        self.fireballs = [pygame.image.load('fireball.png'), [pygame.image.load('fireballleft.png')]]

    def __getitem__(self, item):
        return self.fireballs[item]

    def draw(self, window):
        if player1.left:
            window.blit(fireball_left[0], (self.x, self.y))
        else:
            window.blit(fireball[0], (self.x, self.y))


def redraw_game_window():
    window.blit(background, (0, 0))
    player1.draw(window)
    player2.draw(window)
    for fireball in fireballs:
        fireball.draw(window)
    pygame.display.update()


# Main loop
font = pygame.font.SysFont('comicsans', 30, True)
player1 = Player1(200, 285, 75, 64)
player2 = Player2(600, 285, 75, 64)
fireballs = []
hit = []
maximum_fireballs = 1
frame_per_second = 16
screen_length_right = 600
screen_length_left = 0
run = True

while run:
    clock.tick(frame_per_second)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for fireball in fireballs:
        if fireball.y - fireball.radius < player2.hit_box[1] + player2.hit_box[3] and fireball.y + \
                fireball.radius > player2.hit_box[1]:
            if fireball.x + fireball.radius > player2.hit_box[0] and fireball.x - fireball.radius < player2.hit_box[0] \
                    + player2.hit_box[2]:
                hit_sound.play()
                player2.hit()
                fireballs.pop(fireballs.index(fireball))

        if screen_length_right > fireball.x > screen_length_left:
            fireball.x += fireball.velocity
        else:
            fireballs.pop(fireballs.index(fireball))



    keys = pygame.key.get_pressed()

    if keys[pygame.K_f]:
        player1.punching = True
        player1.right = False
        player1.left = False
    else:
        player1.punching = False
        player1.right = True

    if keys[pygame.K_a] and player1.x > player1.velocity:
        player1.x -= player1.velocity
        player1.left = True
        player1.right = False
        player1.standing = False

    elif keys[pygame.K_d] and player1.x < screen_width - player1.width - player1.velocity:
        player1.x += player1.velocity
        player1.right = True
        player1.left = False
        player1.standing = False
    else:
        player1.standing = True
        player1.walk_count = 0

    if keys[pygame.K_SPACE]:

        if player1.left:
            facing = -1
        else:
            facing = 1

        if len(fireballs) < maximum_fireballs:
            fireballs.append(Fireball(player1.x + player1.width // 2, round(player1.y + player1.height // 2), 6,
                                      facing))
            fireball_sound.play()

    if not player1.is_jump:
        if keys[pygame.K_w]:
            player1.is_jump = True
            player1.walk_count = 0
    else:
        if player1.jump_count >= -10:  # land on ground
            neg = 1
            if player1.jump_count < 0:
                neg = -1
            player1.y -= (player1.jump_count ** 2) / 2 * neg
            player1.jump_count -= 1
        else:
            player1.is_jump = False
            player1.jump_count = 10

    if keys[pygame.K_LEFT] and player2.x > player2.velocity:
        player2.x -= player2.velocity
        player2.left = True
        player2.right = False
        player2.standing = False

    elif keys[pygame.K_RIGHT] and player2.x < screen_width - player2.width - player2.velocity:
        player2.x += player2.velocity
        player2.right = True
        player2.left = False
        player2.standing = False
    else:
        player2.standing = True
        player2.walk_count = 0

    if not player2.is_jump:
        if keys[pygame.K_UP]:
            player2.is_jump = True
            player2.walk_count = 0
    else:
        if player2.jump_count >= -10:  # land on ground
            neg = 1
            if player2.jump_count < 0:
                neg = -1
            player2.y -= (player2.jump_count ** 2) / 2 * neg
            player2.jump_count -= 1
        else:
            player2.is_jump = False
            player2.jump_count = 10

    redraw_game_window()
pygame.quit()



















