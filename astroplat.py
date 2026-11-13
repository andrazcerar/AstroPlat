import os
import random
import math
import pygame
import sys
import time

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


pygame.init()
pygame.display.set_caption("AstroPlat")

SIRINA, VISINA = 1920, 1080
fps = 80
PLAYER_VEL = 4
window = pygame.display.set_mode((SIRINA, VISINA))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font_path = resource_path("assets/font.ttf")
if os.path.exists(font_path):
    font = pygame.font.Font(font_path, 36)
else:
    font = pygame.font.SysFont("arial", 36)

easter_egg_active = False
q_counter = 0
e_counter = 0
fpress = False
EASY_LEVEL_FOR_EASTER = 21

show_tutorial = True


def show_tutorial_screen():
    tutorial_running = True
    clock = pygame.time.Clock()

    BG_COLOR = (25, 25, 50)
    TEXT_COLOR = (255, 255, 255)  # VSE BESEDILO BELO
    HIGHLIGHT_COLOR = (255, 255, 255)  # Tudi naslov bel

    controls = [
        ("A / D", "Move left / right"),
        ("SPACE", "Jump"),
        ("ESC", "Pause"),
        ("DODGE OBSTACLES"),
        ("FRUIT GIVES YOU HEALTH")
    ]

    try:
        bg_image = pygame.image.load(resource_path("assets/Background/gamebackground.png")).convert()
        bg_image = pygame.transform.scale(bg_image, (SIRINA, VISINA))
    except:
        bg_image = None

    while tutorial_running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    tutorial_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                tutorial_running = False

        if bg_image:
            window.blit(bg_image, (0, 0))
        else:
            window.fill(BG_COLOR)

        title_font = pygame.font.Font(font_path, 72) if os.path.exists(font_path) else pygame.font.SysFont("arial", 72)
        title = title_font.render("ASTROPLAT", True, HIGHLIGHT_COLOR)
        window.blit(title, (SIRINA // 2 - title.get_width() // 2, 80))

        subtitle = font.render("TUTORIAL", True, TEXT_COLOR)
        window.blit(subtitle, (SIRINA // 2 - subtitle.get_width() // 2, 180))

        control_section_y = 280
        controls_title = font.render("CONTROLS:", True, TEXT_COLOR)
        window.blit(controls_title, (SIRINA // 2 - controls_title.get_width() // 2, control_section_y))

        control_y = control_section_y + 60

        for i, item in enumerate(controls):
            if isinstance(item, tuple):
                key, description = item
                # VSE BELO - odstranil row_color razlikovanje
                key_text = font.render(f"{key}", True, TEXT_COLOR)
                window.blit(key_text, (SIRINA // 2 - 250, control_y))
                desc_text = font.render(f"{description}", True, TEXT_COLOR)
                window.blit(desc_text, (SIRINA // 2 + 20, control_y))
                control_y += 55
            else:
                text = font.render(item, True, TEXT_COLOR)
                window.blit(text, (SIRINA // 2 - text.get_width() // 2, control_y))
                control_y += 55

        continue_y = VISINA - 120
        continue_text = font.render("Press SPACE, ESC or click to start game", True, (144, 238, 144))
        window.blit(continue_text, (SIRINA // 2 - continue_text.get_width() // 2, continue_y))

        pygame.display.flip()


def show_easter_egg_unlocked():
    clock = pygame.time.Clock()
    try:
        bg_image = pygame.image.load(resource_path("assets/Background/gameover.png"))
    except:
        bg_image = pygame.Surface((SIRINA, VISINA))
        bg_image.fill((0, 50, 0))

    password = "Q15E15GESLO"

    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.blit(bg_image, (0, 0))
        draw_text("CONGRATULATIONS!", font, (255, 215, 0), window, SIRINA / 2, VISINA / 4)
        draw_text("EASTER EGG UNLOCKED", font, (255, 255, 0), window, SIRINA / 2, VISINA / 4 + 80)
        draw_text(f"PASSWORD FOR PODATKI.ZIP: {password}", font, (50, 200, 50), window, SIRINA / 2, VISINA / 2)

        button_continue = pygame.Surface((430, 50), pygame.SRCALPHA)
        button_continue.fill((255, 255, 255, 0))
        window.blit(button_continue, (SIRINA / 2 - 210, VISINA / 2 + 100))

        draw_text("Continue Game", font, (255, 255, 255), window, SIRINA / 2, VISINA / 2 + 100)

        mouse_pos = pygame.mouse.get_pos()

        if pygame.Rect(SIRINA / 2 - 210, VISINA / 2 + 100, 430, 50).collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                return

        pygame.display.update()


def check_easter_egg_activation(event, difficulty_level):
    global q_counter, e_counter, fpress, easter_egg_active

    if difficulty_level < EASY_LEVEL_FOR_EASTER:
        return False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            q_counter += 1
        elif event.key == pygame.K_e:
            e_counter += 1
        elif event.key == pygame.K_f:
            fpress = True

    if q_counter >= 15 and e_counter >= 15 and fpress and not easter_egg_active:
        easter_egg_active = True
        return True

    return False


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    try:
        path = resource_path(os.path.join("assets", dir1, dir2))
        images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        all_sprites = {}

        for image in images:
            sprite_sheet = pygame.image.load(os.path.join(path, image)).convert_alpha()
            sprites = []
            for i in range(sprite_sheet.get_width() // width):
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * width, 0, width, height)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pygame.transform.scale2x(surface))

            if direction:
                all_sprites[image.replace(".png", "") + "_right"] = sprites
                all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
            else:
                all_sprites[image.replace(".png", "")] = sprites
        return all_sprites
    except Exception:
        return {}


try:
    background_image = pygame.image.load(resource_path("assets/Background/gamebackground.png")).convert()
    background_image = pygame.transform.scale(background_image, (SIRINA, VISINA))
except:
    background_image = pygame.Surface((SIRINA, VISINA))
    background_image.fill((0, 0, 0))

ENABLE_SPIKE = True
ENABLE_SAW = True
ENABLE_BALL = True


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 255)
    GRAVITY = 3
    SPRITES = load_sprite_sheets("MainCharacters", "VirtualGuy", 32, 32, True)
    ANIMATION_DELAY = 4

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        if "idle_left" in self.SPRITES:
            self.mask = pygame.mask.from_surface(self.SPRITES["idle_left"][0])
        else:
            self.mask = pygame.Mask((width, height))
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hp = 1000
        self.max_hp = 1000
        self.reduce_hp_flag = False
        self.cooldown_timer = 0
        self.max_shield = 3000
        self.shield = 0

    def restorehp(self):
        self.shield = 0
        self.hp = 1000

    def restoreposition(self):
        self.rect = pygame.Rect(1020, -65, 50, 50)

    def jump(self):
        self.y_vel = -self.GRAVITY * 3
        self.animation_count = 0
        self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def handle_vertical_collision(self, objects, dy):
        collided_objects = []
        for obj in objects:
            if pygame.sprite.collide_mask(self, obj):
                if dy > 0:
                    self.rect.bottom = obj.rect.top
                    self.landed()
                elif dy < 0:
                    self.rect.top = obj.rect.bottom
                    self.hit_head()
                collided_objects.append(obj)
        return collided_objects

    def handle_move(self, objects):
        keys = pygame.key.get_pressed()
        self.x_vel = 0
        if keys[pygame.K_a]:
            if self.rect.left > 0 - 15:
                self.move_left(PLAYER_VEL)
        if keys[pygame.K_d]:
            if self.rect.right < SIRINA + 15:
                self.move_right(PLAYER_VEL)
        if self.rect.top > VISINA:
            self.rect.top = -self.rect.height
        elif self.rect.bottom < -self.rect.height:
            self.rect.bottom = VISINA

    def draw_health_bar(self, surface, x, y):
        health_bar_width = 500  # POVEČANO za besedilo
        health_bar_height = 40
        health_bar_color = (230, 187, 173)
        border_color = (0, 0, 0)
        border_width = 2

        shield_bar_width = 500  # POVEČANO za besedilo
        shield_bar_height = 40
        shield_bar_color = (173, 216, 230)

        health_percentage = self.hp / self.max_hp
        shield_percentage = self.shield / self.max_shield

        health_fill_width = int(health_percentage * health_bar_width)
        shield_fill_width = int(shield_percentage * shield_bar_width)

        # Preveri če je izven zaslona
        if x < 0:
            x = 20  # Minimalni padding

        # Health bar
        health_border_rect = pygame.Rect(x, y, health_bar_width, health_bar_height)
        pygame.draw.rect(surface, border_color, health_border_rect, border_width)

        # Fill bar (ne gre čez rob)
        fill_width = max(0, health_fill_width - border_width * 2)
        if fill_width > 0:
            health_fill_rect = pygame.Rect(x + border_width, y + border_width,
                                           fill_width, health_bar_height - border_width * 2)
            pygame.draw.rect(surface, health_bar_color, health_fill_rect)

        # Shield bar
        shield_x = x + (health_bar_width - shield_bar_width) // 2
        shield_y = y + health_bar_height + 5
        shield_border_rect = pygame.Rect(shield_x, shield_y, shield_bar_width, shield_bar_height)
        pygame.draw.rect(surface, border_color, shield_border_rect, border_width)

        # Shield fill (ne gre čez rob)
        shield_fill_width_calc = max(0, shield_fill_width - border_width * 2)
        if shield_fill_width_calc > 0:
            shield_fill_rect = pygame.Rect(shield_x + border_width, shield_y + border_width,
                                           shield_fill_width_calc, shield_bar_height - border_width * 2)
            pygame.draw.rect(surface, shield_bar_color, shield_fill_rect)

        # HP text - CENTRIRANO v health bar
        hp_text = font.render(f"HP: {int(self.hp)}/{self.max_hp}", True, (238, 75, 43))
        hp_text_rect = hp_text.get_rect(center=(x + health_bar_width // 2, y + health_bar_height // 2))
        surface.blit(hp_text, hp_text_rect)

        # Shield text - CENTRIRANO v shield bar
        shield_text = font.render(f"SHD: {int(self.shield)}/{self.max_shield}", True, (0, 0, 139))
        shield_text_rect = shield_text.get_rect(center=(shield_x + shield_bar_width // 2,
                                                        shield_y + shield_bar_height // 2))
        surface.blit(shield_text, shield_text_rect)

    def loop(self, fps):
        max_fall_speed = 13
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)

        if self.y_vel > max_fall_speed:
            self.y_vel = max_fall_speed

        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel += -1

    def reduce_hp(self, amount):
        self.reduce_hp_flag = True
        self.cooldown_timer = 7 * self.ANIMATION_DELAY

        if amount < 0:
            if self.hp < self.max_hp:
                self.hp += -amount
                if self.hp > self.max_hp:
                    self.hp = self.max_hp
                excess_healing = max(0, self.hp + amount - self.max_hp)
                if excess_healing > 0:
                    self.hp += excess_healing
                    self.shield = min(self.max_shield, self.shield + excess_healing)
            elif self.shield < self.max_shield:
                self.shield = min(self.max_shield, self.shield - amount)
        else:
            if self.shield > 0:
                if self.shield >= amount:
                    self.shield -= amount
                else:
                    remaining_damage = amount - self.shield
                    self.shield = 0
                    self.hp -= remaining_damage
                    if self.hp < 0:
                        self.hp = 0
            else:
                self.hp -= amount
                if self.hp < 0:
                    self.hp = 0

    def is_alive(self):
        return self.hp > 0

    def update_sprite(self):
        keys = pygame.key.get_pressed()
        sprite_sheet = "idle"
        if self.reduce_hp_flag:
            sprite_sheet = "hit"
            self.reduce_hp_flag = False
        elif self.cooldown_timer > 0:
            sprite_sheet = "hit"
            self.cooldown_timer -= 1
        elif keys[pygame.K_SPACE]:
            sprite_sheet = "double_jump"
        elif self.y_vel > 1:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        if sprite_sheet_name in self.SPRITES:
            sprites = self.SPRITES[sprite_sheet_name]
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
            self.sprite = sprites[sprite_index]
        else:
            self.sprite = pygame.Surface((self.rect.width, self.rect.height))
            self.sprite.fill((255, 0, 255))

        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, velocity_x, velocity_y, movement_type, damage, animation_steps,
                 animation_cooldown):
        super().__init__()
        try:
            self.original_image = pygame.image.load(resource_path(image_path)).convert_alpha()
        except:
            self.original_image = pygame.Surface((width, height))
            self.original_image.fill((255, 0, 0))

        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.movement_type = movement_type
        self.damage = damage
        self.animation_steps = animation_steps
        self.animation_cooldown = animation_cooldown
        self.animation_list = []
        self.frame = 0
        self.time = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_listcreate()

    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.original_image, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image

    def animation_listcreate(self):
        for x in range(self.animation_steps):
            self.animation_list.append(self.get_image(x, self.rect.width, self.rect.height, 2, BLACK))

    def update(self, fps):
        self.rect.x -= self.velocity_x

        if self.movement_type == "sinus":
            self.time += 1 / fps
            vertical_displacement = 10 * math.sin(2 * math.pi * 1 * self.time)
            self.rect.y += vertical_displacement

            if self.rect.top > VISINA:
                self.rect.top = -self.rect.height
            elif self.rect.bottom < -self.rect.height:
                self.rect.bottom = VISINA

        elif self.movement_type == "diagonal":
            self.rect.y -= self.velocity_y

            if self.rect.top > VISINA:
                self.rect.bottom = 0
            elif self.rect.bottom < 0:
                self.rect.top = VISINA

        elif self.movement_type == "cosine":
            self.time += 1 / fps
            horizontal_displacement = 10 * math.cos(2 * math.pi * 1 * self.time)
            self.rect.x += horizontal_displacement
            self.rect.y -= self.velocity_y

            if self.rect.top > VISINA:
                self.rect.top = -self.rect.height
            elif self.rect.bottom < -self.rect.height:
                self.rect.bottom = VISINA

        elif self.movement_type == "vertical":
            self.rect.y += self.velocity_y
            if self.rect.top < 0 or self.rect.bottom > VISINA:
                self.velocity_y = -self.velocity_y

        elif self.movement_type == "random":
            self.rect.x += random.choice([-1, 1]) * self.velocity_x
            self.rect.y += random.choice([-1, 1]) * self.velocity_y
            if self.rect.left < 0 or self.rect.right > SIRINA:
                self.velocity_x = -self.velocity_x
            if self.rect.top < 0 or self.rect.bottom > VISINA:
                self.velocity_y = -self.velocity_y

        elif self.movement_type == "figure_eight":
            radius = 500
            angle_speed = 2
            self.time += 1 / fps
            angle = self.time * angle_speed
            center_x = SIRINA // 2
            center_y = VISINA // 2
            self.rect.centerx = center_x + radius * math.sin(angle)
            self.rect.centery = center_y + radius * math.sin(2 * angle)

        if self.rect.right < 0:
            self.kill()

        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_cooldown:
            self.last_update = now
            self.frame = (self.frame + 1) % len(self.animation_list)
            original_size = self.original_image.get_size()
            target_size = (self.rect.width, self.rect.height)
            self.image = pygame.transform.scale(self.animation_list[self.frame], target_size)

def create_obstacles(difficulty_level):
    obstacles = pygame.sprite.Group()

    spawn = True
    while spawn:
        # Spiked Ball
        if random.randint(1, 500) >= 500 - difficulty_level and ENABLE_BALL:
            x = SIRINA
            y = random.randint(-10, VISINA)
            width = 32
            height = 32
            image_path = "assets/Traps/Spiked Ball/Spiked ball.png"
            velocity_x = 5
            velocity_y = 0
            movement_type = ""
            damage = 70
            animation_steps = 8
            animation_cooldown = 50
            # Pass animation_list and frame here
            spiked_ball = Obstacle(x, y, width, height, image_path, velocity_x, velocity_y, movement_type, damage, animation_steps, animation_cooldown)
            obstacles.add(spiked_ball)
      # Saw
        if random.randint(1, 1000) >= 1000 - difficulty_level and ENABLE_SAW and difficulty_level % 3 == 0:
            x = SIRINA
            y = random.randint(-10, VISINA)
            width = 38
            height = 38
            image_path = "assets/Traps/Saw/Idle.png"
            velocity_x = 10
            velocity_y = 10
            movement_type = "diagonal"
            damage = 100
            animation_steps = 8
            animation_cooldown = 20
            # Pass animation_list and frame here
            saw = Obstacle(x, y, width, height, image_path, velocity_x, velocity_y, movement_type, damage, animation_steps, animation_cooldown)
            obstacles.add(saw)
        # Spike Head
        if random.randint(1,10000) >= 9950 - difficulty_level and ENABLE_SPIKE:
            x = random.randint(SIRINA, SIRINA + 1000)
            y = random.randint(0, VISINA + 300)
            width = 54
            height = 52
            image_path = "assets/Traps/Spike Head/Blink.png"
            velocity_x = 7
            velocity_y = 10
            movement_type = "sinus"
            damage = 120
            animation_steps = 4
            animation_cooldown = 100
            spike_head = Obstacle(x, y, width, height, image_path, velocity_x, velocity_y, movement_type, damage, animation_steps, animation_cooldown)
            obstacles.add(spike_head)

        if random.randint(1, 10000) >= 9950 - difficulty_level and ENABLE_SPIKE and difficulty_level % 5 == 0:
            x = random.randint(SIRINA, SIRINA + 1000)
            y = random.randint(0, VISINA + 300)
            width = 54
            height = 52
            image_path = "assets/Traps/Spike Head/Blink.png"
            velocity_x = 9
            velocity_y = 13
            movement_type = "cosine"
            damage = 320
            animation_steps = 4
            animation_cooldown = 100
            spike_head = Obstacle(x, y, width, height, image_path, velocity_x, velocity_y, movement_type, damage, animation_steps, animation_cooldown)

            obstacles.add(spike_head)

        if random.randint(1, 500) >= 500 - difficulty_level and ENABLE_BALL and difficulty_level % 10 == 0:
            x = SIRINA
            y = random.randint(-10, VISINA)
            width = 32
            height = 32
            image_path = "assets/Traps/Spiked Ball/Spiked ball.png"
            velocity_x = 1
            velocity_y = 1
            movement_type = "figure_eight"
            damage = 70
            animation_steps = 8
            animation_cooldown = 50
            # Pass animation_list and frame here
            spiked_ball = Obstacle(x, y, width, height, image_path, velocity_x, velocity_y, movement_type, damage, animation_steps, animation_cooldown)
            obstacles.add(spiked_ball)

        if random.randint(1, 500) >= 500 - difficulty_level and ENABLE_BALL and difficulty_level % 10 == 0:
            x = SIRINA
            y = random.randint(-10, VISINA)
            width = 32
            height = 32
            image_path = "assets/Traps/Spiked Ball/Spiked ball.png"
            velocity_x = 1
            velocity_y = 1
            movement_type = "figure_eight"
            damage = 70
            animation_steps = 8
            animation_cooldown = 50
            # Pass animation_list and frame here
            spiked_ball = Obstacle(x, y, width, height, image_path, velocity_x, velocity_y, movement_type, damage, animation_steps, animation_cooldown)
            obstacles.add(spiked_ball)

        if random.randint(1, 10000) >= 9999 - difficulty_level and not (
                difficulty_level % 10 == 0) or difficulty_level % 49 == 0:
            x = random.randint(SIRINA, SIRINA + 1000)
            y = random.randint(0, VISINA + 300)
            width = 32
            height = 32
            image_path = "assets/Items/Fruits/Strawberry.png"
            velocity_x = 20
            velocity_y = 20
            movement_type = "figure_eight"
            damage = -300
            animation_steps = 17
            animation_cooldown = 50
            strawberry = Obstacle(x, y, width, height, image_path, velocity_x, velocity_y, movement_type, damage, animation_steps, animation_cooldown)

            obstacles.add(strawberry)

        if random.randint(1, 10000) >= 9999:
            x = random.randint(SIRINA, SIRINA + 1000)
            y = random.randint(0, VISINA + 300)
            width = 32
            height = 32
            image_path = "assets/Items/Fruits/Melon.png"
            velocity_x = 15
            velocity_y = 1
            movement_type = "cosine"
            damage = -800
            animation_steps = 17
            animation_cooldown = 50
            melon = Obstacle(x, y, width, height, image_path, velocity_x, velocity_y, movement_type, damage,animation_steps, animation_cooldown)

            obstacles.add(melon)
        yield obstacles
def render_game(window, player, obstacles, grace_period_text_shown, paused, difficulty_level):
    window.fill((0, 0, 0))
    window.blit(background_image, (0, 0))
    player.draw(window)
    player.draw_health_bar(window, 20, 20)

    for obstacle in obstacles:
        obstacle_image = obstacle.animation_list[obstacle.frame]
        window.blit(obstacle_image, obstacle.rect)

    if grace_period_text_shown:
        grace_period_font = font
        grace_period_text = grace_period_font.render(f"DIFFICULTY INCREASED, LEVEL: {difficulty_level}", True, (255, 255, 255))
        window.blit(grace_period_text, (SIRINA // 2 - grace_period_text.get_width() // 2, 150))

    if paused:
        dim_surface = pygame.Surface((SIRINA, VISINA))
        dim_surface.set_alpha(128)
        dim_surface.fill((0, 0, 0))
        window.blit(dim_surface, (0, 0))

        pause_font = font
        pause_text_line1 = "GAME IS PAUSED"
        pause_text_line2 = "PRESS SPACE TO CONTINUE"
        pause_text = pause_font.render(pause_text_line1, True, (255, 255, 255))
        pause_text2 = pause_font.render(pause_text_line2, True, (255, 255, 255))
        window.blit(pause_text, (SIRINA // 2 - pause_text.get_width() // 2, 300))
        window.blit(pause_text2, (SIRINA // 2 - pause_text2.get_width() // 2, 500))

    level_text = font.render(f"LEVEL: {int(difficulty_level)}", True, WHITE)
    level_rect = level_text.get_rect(topright=(SIRINA - 20, 20))
    window.blit(level_text, level_rect)

    if difficulty_level >= EASY_LEVEL_FOR_EASTER and not easter_egg_active:
        egg_font = pygame.font.Font(font_path, 24) if os.path.exists(font_path) else pygame.font.SysFont("arial", 24)
        egg_text = egg_font.render(f"Q:{q_counter} E:{e_counter}", True, (255, 255, 0))
        window.blit(egg_text, (SIRINA - 300, 80))

    pygame.display.update()


def game(window):
    while True:  # Add an outer loop to restart the game
        global show_tutorial, q_counter, e_counter, easter_egg_active

        clock = pygame.time.Clock()
        original_time = time.time()
        player = Player(SIRINA // 2, -65, 50, 50)

        difficulty_level = 1
        last_difficulty_increase = time.time()

        obstacles_group_generator = create_obstacles(difficulty_level)
        obstacles_group = next(obstacles_group_generator)

        grace_period_active = False
        grace_period_duration = 6
        grace_period_end_time = 0
        grace_period_text_shown = False
        grace_period_text_delay = 3
        grace_period_text_start_time = 0
        paused = False
        pause_start_time = 0
        paused_time = 0

        run = True
        while run:
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if paused:
                            paused = False
                            paused_time += time.time() - pause_start_time
                        else:
                            player.jump()
                    elif event.key == pygame.K_ESCAPE:
                        if not paused:
                            pause_start_time = time.time()
                            paused = True
                    elif difficulty_level >= EASY_LEVEL_FOR_EASTER:
                        if check_easter_egg_activation(event, difficulty_level):
                            show_easter_egg_unlocked()
                            easter_egg_active = False
                            q_counter = 0
                            e_counter = 0

            if not paused:
                current_time = time.time() - paused_time
                elapsed_time_since_last_increase = current_time - last_difficulty_increase

                if elapsed_time_since_last_increase >= 7.5 + grace_period_duration and not grace_period_active:
                    difficulty_level += 2
                    last_difficulty_increase = current_time
                    grace_period_active = True
                    grace_period_end_time = current_time + grace_period_duration
                    grace_period_text_start_time = current_time + grace_period_text_delay
                    obstacles_group_generator = create_obstacles(difficulty_level)

                if grace_period_active and current_time >= grace_period_end_time:
                    grace_period_active = False
                    grace_period_text_shown = False

                if grace_period_active and current_time >= grace_period_text_start_time and not grace_period_text_shown:
                    grace_period_text_shown = True

                if not grace_period_active:
                    obstacles_group = next(obstacles_group_generator)

                collisions = pygame.sprite.spritecollide(player, obstacles_group, False, pygame.sprite.collide_mask)
                for obstacle in collisions:
                    player.reduce_hp(obstacle.damage)
                    obstacle.kill()

                if not player.is_alive():
                    score = difficulty_level

                    # Call game_over and check if player wants to restart
                    restart = game_over(window, score)
                    if restart:
                        break  # Break out of inner game loop to restart
                    else:
                        run = False
                        break

                player.loop(fps)
                player.handle_move(obstacles_group)
                obstacles_group.update(fps)

            render_game(window, player, obstacles_group, grace_period_text_shown, paused, difficulty_level)

        if not run:  # If run is False, break out of outer loop too
            break

def game_over(window, score):
    clock = pygame.time.Clock()
    try:
        bg_image = pygame.image.load(resource_path("assets/Background/gameover.png"))
    except:
        bg_image = pygame.Surface((SIRINA, VISINA))
        bg_image.fill((50, 0, 0))

    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.blit(bg_image, (0, 0))
        draw_text("GAME OVER", font, WHITE, window, SIRINA / 2, VISINA / 4)
        draw_text(f"DIFFICULTY LEVEL REACHED: {score}", font, WHITE, window, SIRINA / 2, VISINA / 4 + 80)

        button_start = pygame.Surface((430, 50), pygame.SRCALPHA)
        button_start.fill((255, 255, 255, 0))
        button_quit = pygame.Surface((430, 50), pygame.SRCALPHA)
        button_quit.fill((255, 255, 255, 0))

        window.blit(button_start, (SIRINA / 2 - 210, VISINA / 2 - 30))
        window.blit(button_quit, (SIRINA / 2 - 210, VISINA / 2 + 50))

        draw_text("Play Again", font, (255, 255, 255), window, SIRINA / 2, VISINA / 2)
        draw_text("Quit Game", font, (255, 255, 255), window, SIRINA / 2, VISINA / 2 + 80)

        mouse_pos = pygame.mouse.get_pos()

        if pygame.Rect(SIRINA / 2 - 210, VISINA / 2 - 30, 430, 50).collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                return True  # Vrne True za novo igro

        if pygame.Rect(SIRINA / 2 - 210, VISINA / 2 + 50, 430, 50).collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def main_menu():
    clock = pygame.time.Clock()
    try:
        background_image = pygame.image.load(resource_path("assets/Background/mainmenu.png"))
    except:
        background_image = pygame.Surface((SIRINA, VISINA))
        background_image.fill((25, 25, 50))

    # Add a variable to track if we just returned from tutorial
    just_returned_from_tutorial = False

    while True:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                # Reset the flag when mouse button is released
                just_returned_from_tutorial = False

        window.blit(background_image, (0, 0))
        draw_text("ASTROPLAT", font, WHITE, window, SIRINA / 2, VISINA / 9)

        button_start = pygame.Surface((430, 50), pygame.SRCALPHA)
        button_start.fill((255, 255, 255, 0))
        button_tutorial = pygame.Surface((430, 50), pygame.SRCALPHA)
        button_tutorial.fill((255, 255, 255, 0))
        button_quit = pygame.Surface((430, 50), pygame.SRCALPHA)
        button_quit.fill((255, 255, 255, 0))

        window.blit(button_start, (SIRINA / 2 - 210, VISINA / 2 - 30))
        window.blit(button_tutorial, (SIRINA / 2 - 210, VISINA / 2 + 50))
        window.blit(button_quit, (SIRINA / 2 - 210, VISINA / 2 + 130))

        draw_text("Play Game", font, WHITE, window, SIRINA / 2, VISINA / 2)
        draw_text("Show Tutorial", font, WHITE, window, SIRINA / 2, VISINA / 2 + 80)
        draw_text("Quit Game", font, BLACK, window, SIRINA / 2, VISINA / 2 + 160)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if pygame.Rect(SIRINA / 2 - 210, VISINA / 2 - 30, 430, 50).collidepoint(mouse_pos):
            if mouse_pressed and not just_returned_from_tutorial:
                return True

        if pygame.Rect(SIRINA / 2 - 210, VISINA / 2 + 50, 430, 50).collidepoint(mouse_pos):
            if mouse_pressed and not just_returned_from_tutorial:
                global show_tutorial
                show_tutorial = True
                show_tutorial_screen()
                # Set flag to prevent immediate re-entry
                just_returned_from_tutorial = True

        if pygame.Rect(SIRINA / 2 - 210, VISINA / 2 + 130, 430, 50).collidepoint(mouse_pos):
            if mouse_pressed and not just_returned_from_tutorial:
                pygame.quit()
                sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    running = True
    while running:
        if main_menu():
            game(window)  # game() now has its own restart loop