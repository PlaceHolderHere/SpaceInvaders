import pygame
from random import randint

# CLASSES
class Alien:
    def __init__(self, x, y, size, change_X, sprite, movement_timer):
        self.x = x
        self.y = y
        self.size = size
        self.change_X = change_X
        self.sprite = sprite
        self.movement_timer = movement_timer
        self.bullets = []

    def blit(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def move(self, cooldown):
        self.movement_timer -= 1

        if self.movement_timer <= 0:
            self.movement_timer = cooldown
            self.x += self.change_X

    def collision(self, x, y, size_X, size_Y):
        alien_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        collision_rect = pygame.Rect(x, y, size_X, size_Y)

        return alien_rect.colliderect(collision_rect)

    def shoot(self):
        self.bullets.append(Bullet(self.x + (self.size / 2) - 8, self.y, 16, 32,2, pygame.image.load("enemy_bullet.png")))

class Player:
    def __init__(self, x, y, size, change_X, sprite):
        self.x = x
        self.y = y
        self.size = size
        self.change_X = change_X
        self.sprite = sprite
        self.firing_cooldown = 0
        self.bullets = []
        self.alive = True
        self.lives = 3

    def blit(self, win):
        win.blit(self.sprite, (self.x, self.y))

        if self.firing_cooldown > 0:
            self.firing_cooldown -= 1

    def move(self):
        self.x += self.change_X

    def collision(self, x, y, size_X, size_Y):
        self_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        collision_rect = pygame.Rect(x, y, size_X, size_Y)

        return self_rect.colliderect(collision_rect)

    def shoot(self, firing_cooldown, shoot_SFX):
        if self.firing_cooldown == 0:
            self.bullets.append(Bullet(self.x + (self.size / 2) - 8, self.y, 18, 64, -8, pygame.image.load("bullet.png")))
            self.firing_cooldown = firing_cooldown
            shoot_SFX.play()

class Bullet:
    def __init__(self, x, y, sizeX, sizeY, change_Y, sprite):
        self.x = x
        self.y = y
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.change_Y = change_Y
        self.sprite = sprite

    def blit(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def move(self):
        self.y += self.change_Y

    def collision(self, *args):
        for rect in args:
            self_rect = pygame.Rect(self.x, self.y, self.sizeX, self.sizeY)
            return self_rect.colliderect(rect)

class Fortress_block:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def blit(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

class Button():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.rect.Rect(x, y, image.get_width(), image.get_height())

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

        mouse_position = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

# FUNCTIONS
def display_text(win, x, y, msg, color):
    pygame.font.init()

    font = pygame.font.SysFont('Arial', 35)
    text = font.render(msg, False, color)
    text_rect = text.get_rect(center=(x, y))

    win.blit(text, text_rect)

def alien_init(startX, X_spacing, sprite_size, alien_speed):
    aliens1 = []
    aliens2 = []
    aliens3 = []
    aliens4 = []
    for i in range(8):
        aliens1.append(Alien(startX + (X_spacing * i), 64, sprite_size, alien_speed, pygame.image.load('enemy1.png'), 120))
        aliens2.append(Alien(startX + (X_spacing * i), 128, sprite_size, alien_speed, pygame.image.load('enemy2.png'), 90))
        aliens3.append(Alien(startX + (X_spacing * i), 192, sprite_size, alien_speed, pygame.image.load('enemy3.png'), 60))
        aliens4.append(Alien(startX + (X_spacing * i), 256, sprite_size, alien_speed, pygame.image.load('enemy4.png'), 30))
    aliens = [aliens4, aliens3, aliens2, aliens1]
    return aliens

def fortress_init(x, y, block_size, color):
    output = []
    fortress = [
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1]
        ]

    for row in fortress:
        for i, num in enumerate(row):
            if num == 1:
                output.append(Fortress_block(x + (block_size*i), y, block_size, color))

        y += block_size

    return output

def difficulty_calculator(wave_number, difficulty_cap, difficulty):
    if (wave_number / difficulty) + 1 < difficulty_cap:
        return ((wave_number / difficulty) + 2)

    else:
        return difficulty_cap

# Main
def main():
    # Constants
    SCREEN_WIDTH = 704
    SCREEN_HEIGHT = 704
    CLOCK = pygame.time.Clock()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    SPRITE_SIZE = 64
    DIFFICULTY = 5
    DIFFICULTY_CAP = 15
    PLAYER_SPEED = 4
    PLAYER_FIRING_COOLDOWN = 50
    ALIEN_SPEED = 8
    ALIEN_MOVEMENT_SPEED = 120
    LIVES_ICON = pygame.transform.scale(pygame.image.load("Player.png"), (32, 32))

    STARS = []
    for i in range(100):
        STARS.append((randint(0, 704), randint(0, 704)))

    # Pygame Init
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Space Invaders by PlaceHolderHere")
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Buttons
    resume_Button = Button(254, 222, pygame.image.load("Resume.png"))
    restart_Button = Button(254, 320, pygame.image.load("Restart.png"))
    quit_Button = Button(254, 418, pygame.image.load("Quit.png"))
    play_Button = Button(254, 254, pygame.image.load("Play.png"))
    controls_Button = Button(254, 352, pygame.image.load("Controls.png"))
    main_menu_Button = Button(254, 124, pygame.image.load("Main Menu.png"))
    retry_Button = Button(254, 320, pygame.image.load("Retry.png"))

    # SFX
    player_shoot_SFX = pygame.mixer.Sound("fire.wav")
    player_explode_SFX = pygame.mixer.Sound("explode_player.wav")
    alien_explode_SFX = pygame.mixer.Sound("explode.wav")
    alien_fire_SFX = pygame.mixer.Sound("enemy_fire.wav")
    fortress_hit_SFX = pygame.mixer.Sound("fortress_hit.wav")

    # Variables
    running = True
    paused = 1
    player_score = 0
    wave_number = 1
    menu = 0

    player = Player(0, 630, SPRITE_SIZE, 0, pygame.image.load("Player.png"))
    aliens = alien_init(68, 72, SPRITE_SIZE, ALIEN_SPEED)
    fortresses = [fortress_init(100, 500, 8, WHITE), fortress_init(300, 500, 8, WHITE), fortress_init(500, 500, 8, WHITE)]

    # GAME LOOP
    while running:
        # 60 FPS
        CLOCK.tick(60)

        # INPUTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused *= -1

                if paused > 0 and menu == 2:
                    if event.key == pygame.K_a:
                        player.change_X = -PLAYER_SPEED

                    if event.key == pygame.K_s:
                        player.change_X = PLAYER_SPEED

                    if event.key == pygame.K_SPACE:
                        player.shoot(PLAYER_FIRING_COOLDOWN, player_shoot_SFX)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_s:
                    player.change_X = 0

        win.fill(BLACK)
        for star in STARS:
            x, y = star
            pygame.draw.rect(win, WHITE, (x, y, 4, 4))

        # Main Menu
        if menu == 0:
            display_text(win, 352, 160, "Space Invaders by PlaceHolderHere", WHITE)

            if controls_Button.draw(win):
                menu = 1

            if play_Button.draw(win):
                menu = 2

        elif menu == 1:
            display_text(win, 352, 224, "Controls:", WHITE)
            display_text(win, 352, 288, "A: Left", WHITE)
            display_text(win, 352, 352, "S: Right", WHITE)
            display_text(win, 352, 416, "Space: Shoot", WHITE)
            display_text(win, 352, 480, "Escape: Main Menu", WHITE)

            if main_menu_Button.draw(win):
                menu = 0

        # Main Game
        elif menu == 2:
            if paused > 0 and player.lives >= 0:
                # PLAYER
                if player.alive:
                    player.blit(win)
                    player.move()

                    if player.x < 0:
                        player.x = 0

                    if player.x > 640:
                        player.x = 640

                    # live icons
                    for i in range(player.lives):
                        win.blit(LIVES_ICON, (656 - (i*32), 16))

                    # Player Bullet
                    for bullet_index, bullet in enumerate(player.bullets):
                        if bullet.collision(pygame.Rect(0, -20, 700, -50)):
                            player.bullets.pop(bullet_index)
                            break

                        for alien_list in aliens:
                            for alien_index, alien in enumerate(alien_list):
                                if bullet.collision(pygame.Rect(alien.x, alien.y, alien.size, alien.size)):
                                    player.bullets.pop(bullet_index)
                                    alien_list.pop(alien_index)
                                    alien_explode_SFX.play()

                                    player_score += 100
                                    break

                        for fortress in fortresses:
                            for fortress_index, fortress_block in enumerate(fortress):
                                if bullet.collision(pygame.Rect(fortress_block.x, fortress_block.y, fortress_block.size, fortress_block.size)):
                                    fortress.pop(fortress_index)
                                    player.bullets.pop(bullet_index)

                                    fortress_hit_SFX.play()
                                    break

                        bullet.blit(win)
                        bullet.move()

                # Player Respawn
                elif player.alive is False:
                    for alien_list in aliens:
                        for i, alien in enumerate(alien_list):
                            CLOCK.tick(10)
                            win.fill(BLACK)
                            alien.bullets.clear()
                            if i % 2 == 0:
                                player.blit(win)

                            pygame.display.update()

                    player.x = 100
                    player.alive = True

                # ALIENS
                num_aliens = 0
                for alien_list in aliens:
                    num_aliens += len(alien_list)

                for alien_list in aliens:
                    for alien in alien_list:
                        if alien.y > 420:
                            player.lives = -1
                            player_explode_SFX.play()
                            break

                        if alien.x > 640:
                            for alien_list2 in aliens:
                                for alien2 in alien_list2:
                                    alien2.y += 40
                                    alien2.change_X *= -1
                                    alien2.x -= ALIEN_SPEED
                            for alien3 in aliens[0]:
                                alien3.movement_timer = 0
                                alien3.x -= ALIEN_SPEED

                        if alien.x < 0:
                            for alien_list2 in aliens:
                                for alien2 in alien_list2:
                                    alien2.y += 40
                                    alien2.change_X *= -1
                                    alien2.x += ALIEN_SPEED
                            for alien3 in aliens[0]:
                                alien3.movement_timer = 0
                                alien3.x += ALIEN_SPEED

                        alien.blit(win)
                        alien.move((ALIEN_MOVEMENT_SPEED - ((DIFFICULTY * difficulty_calculator(wave_number, DIFFICULTY_CAP, DIFFICULTY)))) + (num_aliens * 6))

                        # Shoot
                        if randint(1, 2000) <= (difficulty_calculator(wave_number, DIFFICULTY_CAP, DIFFICULTY)):
                            alien.shoot()
                            alien_fire_SFX.play()

                        # Alien Bullet
                        for bullet_index, bullet in enumerate(alien.bullets):
                            bullet.blit(win)
                            bullet.move()

                            if bullet.collision(pygame.Rect(player.x, player.y, player.size, player.size)) and player.alive:
                                alien.bullets.pop(bullet_index)
                                player.alive = False
                                player.lives -= 1
                                player_explode_SFX.play()
                                break

                            for fortress in fortresses:
                                for fortress_index, fortress_block in enumerate(fortress):
                                    if bullet.collision(pygame.Rect(fortress_block.x, fortress_block.y, fortress_block.size,fortress_block.size)):
                                        fortress.pop(fortress_index)
                                        alien.bullets.pop(bullet_index)
                                        fortress_hit_SFX.play()
                                        break

                # FORTRESS
                for fortress in fortresses:
                    for fortress_block in fortress:
                        fortress_block.blit(win)

                # Score Display
                display_text(win, 352, 20, str(player_score), WHITE)

                # NEXT WAVE
                if num_aliens == 0:
                    player.bullets.clear()
                    player.x = 0
                    fortresses = [fortress_init(100, 500, 8, WHITE), fortress_init(300, 500, 8, WHITE),fortress_init(500, 500, 8, WHITE)]
                    aliens = alien_init(68, 72, SPRITE_SIZE, ALIEN_SPEED)
                    wave_number += 1

                    for i in range(20):
                        CLOCK.tick(10)
                        win.fill(BLACK)
                        if i % 2 == 0:
                            player.blit(win)

                            for alien_list in aliens:
                                for alien in alien_list:
                                    alien.blit(win)

                            for fortress in fortresses:
                                for fortress_block in fortress:
                                    fortress_block.blit(win)

                        pygame.display.update()

            # Pause Display
            if paused < 0 and player.lives >= 0:
                if resume_Button.draw(win):
                    paused *= -1

                if restart_Button.draw(win):
                    player = Player(0, 630, SPRITE_SIZE, 0, pygame.image.load("Player.png"))
                    aliens = alien_init(68, 72, SPRITE_SIZE, ALIEN_SPEED)
                    fortresses = [fortress_init(100, 500, 8, WHITE), fortress_init(300, 500, 8, WHITE), fortress_init(500, 500, 8, WHITE)]
                    wave_number = 1
                    player_score = 0
                    paused *= -1

                if quit_Button.draw(win):
                    running = False

            # Lose Screen
            if player.lives < 0:
                display_text(win, 352, 280, f"final score: {player_score}", WHITE)

                if retry_Button.draw(win):
                    player = Player(0, 630, SPRITE_SIZE, 0, pygame.image.load("Player.png"))
                    aliens = alien_init(68, 72, SPRITE_SIZE, ALIEN_SPEED)
                    fortresses = [fortress_init(100, 500, 8, WHITE), fortress_init(300, 500, 8, WHITE), fortress_init(500, 500, 8, WHITE)]
                    wave_number = 1
                    player_score = 0
                    paused *= -1

                if quit_Button.draw(win):
                    running = False

        # Update Display
        pygame.display.update()

if __name__ == "__main__":
    main()
