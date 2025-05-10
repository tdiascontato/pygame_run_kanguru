import pgzrun
import random
import pygame
from pygame import Rect
from pgzero.actor import Actor


pygame.mixer.init()

die_sound = pygame.mixer.Sound('music/die.mp3')

WIDTH = 800
HEIGHT = 600
TILE_SIZE = 64
SPEED = 3

class Character:
    def __init__(self, name, pos, frames_left, frames_right=None):
        self.frames_left = frames_left
        self.frames_right = frames_right or frames_left
        self.direction = 'left'
        self.frames = self.frames_left
        self.frame_index = 0
        self.animation_timer = 0
        self.actor = Actor(self.frames[0], pos)

    def set_direction(self, direction):
        if direction not in ('left', 'right'):
            return
        self.direction = direction
        self.frames = self.frames_left if direction == 'left' else self.frames_right
        self.frame_index = 0
        self.actor.image = self.frames[self.frame_index]

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.actor.image = self.frames[self.frame_index]

    def stay_in_bounds(self):
        self.actor.x = max(0, min(WIDTH, self.actor.x))
        self.actor.y = max(0, min(HEIGHT, self.actor.y))


class Hero(Character):
    def __init__(self, pos):
        left = [f'hero_{i}' for i in range(4)]
        right = ['hero_right']
        super().__init__('hero', pos, left, right)
        self.dx = 0
        self.dy = 0

    def update(self):
        self.actor.x += self.dx
        self.actor.y += self.dy
        self.stay_in_bounds()

        if self.dx != 0 or self.dy != 0:
            if self.dx > 0:
                self.set_direction('right')
            elif self.dx < 0:
                self.set_direction('left')
            if len(self.frames) > 1:
                self.animate()
        else:
            self.frame_index = 0
            self.actor.image = self.frames[0]


class Enemy(Character):
    def __init__(self, pos):
        left = [f'enemy_{i}' for i in range(4)]
        right = ['enemy_right']
        super().__init__('enemy', pos, left, right)
        self.dx = random.choice([-2, 2])
        self.dy = random.choice([-2, 2])

    def update(self):
        self.actor.x += self.dx
        self.actor.y += self.dy

        if self.actor.left < 0 or self.actor.right > WIDTH:
            self.dx *= -1
            self.set_direction('right' if self.dx > 0 else 'left')
        if self.actor.top < 0 or self.actor.bottom > HEIGHT:
            self.dy *= -1

        self.stay_in_bounds()
        self.animate()


hero = Hero((400, 300))
enemies = []
game_state = "menu"
music_on = True

def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        hero.actor.draw()
        for e in enemies:
            e.actor.draw()

def draw_menu():
    screen.draw.text("Fuja Kanguru!", center=(400, 100), fontsize=60)
    draw_button("Start", 200, (129,253,167))
    draw_button("Music: "+("On" if music_on else "Off"), 275, (247,128,8))
    draw_button("Quit", 350, (255,0,0))

def draw_button(text, y, color):
    btn = Rect((300, y, 200, 50))
    screen.draw.filled_rect(btn, color)
    screen.draw.text(text, center=btn.center, color=(0,0,0))

def update():
    if game_state == "game":
        hero.update()
        for e in enemies:
            e.update()
            if e.actor.colliderect(hero.actor):
                reset_game()
                break

def on_mouse_down(pos):
    global game_state, music_on, enemies
    if game_state == "menu":
        if 300 <= pos[0] <= 500:
            if 200 <= pos[1] <= 250:
                enemies = [Enemy((random.randint(50, 750), random.randint(50, 550))) for _ in range(4)]
                hero.actor.pos = (400, 300)
                hero.dx = 0
                hero.dy = 0
                game_state = "game"
            elif 275 <= pos[1] <= 325:
                music_on = not music_on
                music.play('theme') if music_on else music.stop()
            elif 350 <= pos[1] <= 400:
                quit()

def on_key_down(key):
    if game_state == "game":
        if key == keys.LEFT:
            hero.dx = -SPEED
        elif key == keys.RIGHT:
            hero.dx = SPEED
        elif key == keys.UP:
            hero.dy = -SPEED
        elif key == keys.DOWN:
            hero.dy = SPEED

def on_key_up(key):
    if game_state == "game":
        if key == keys.LEFT or key == keys.RIGHT:
            hero.dx = 0
        elif key == keys.UP or key == keys.DOWN:
            hero.dy = 0

def reset_game():
    die_sound.play()
    music.stop()           
    global game_state
    game_state = "menu"
    music.play('theme')
    hero.actor.pos = (400, 300)
    hero.dx = 0
    hero.dy = 0

music.play('theme')
pgzrun.go()