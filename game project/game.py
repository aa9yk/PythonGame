import pygame
import gamebox
import random

WIDTH = 800
HEIGHT = 600
camera = gamebox.Camera(WIDTH, HEIGHT)
sheet = gamebox.load_sprite_sheet("scoobysprite.png", 1, 16)
ground = gamebox.from_color(-100, 600, "blue", 1000000000, 50)
frame = 0
scooby = gamebox.from_image(80, 200, sheet[frame])
walls = []
for x in range(0, 20000, 450):
    walls.append(gamebox.from_color(x, 250, "green", random.randint(100, 300), 20))
for x in range(0, 20000, 350):
    walls.append(gamebox.from_color(x, 400, "green", random.randint(100, 300), 20))
for x in range(0, 20000, 550):
    walls.append(gamebox.from_color(x, 100, "green", random.randint(100, 300), 20))
snacks = []
for x in range(0, 20000, 900):
    snacks.append(gamebox.from_image(x, 220, "snack.png"))
for x in range(0, 20000, 1050):
    snacks.append(gamebox.from_image(x, 370, "snack.png"))
for x in range(0, 20000, 1650):
    snacks.append(gamebox.from_image(x, 70, "snack.png"))
boxes = []
for x in range(0, 20000, 2250):
    boxes.append(gamebox.from_image(x, 220, "box.png"))
for x in range(0, 20000, 3500):
    boxes.append(gamebox.from_image(x, 370, "box.png"))
for x in range(0, 20000, 4400):
    boxes.append(gamebox.from_image(x, 70, "box.png"))
enemies = []
for x in range(0, 20000, 1800):
    enemies.append(gamebox.from_image(x, 200, 'ghost.png'))
for x in range(0, 20000, 700):
    enemies.append(gamebox.from_image(x, 350, 'ghost.png'))
for x in range(0, 20000, 3850):
    enemies.append(gamebox.from_image(x, 50, 'ghost.png'))
BOUNDS_ACTION = "remove"
BOUNDS_ACTION2 = "bounce"
health = 3
direction = 0
direction_x = 1
direction_y = 1
timer = 1800
counter = 0
score = 0
game_over = True
scooby.yspeed = 0


def tick(keys):
    global game_over
    if game_over is False:
        global frame
        global direction
        global counter
        global score
        global health
        global timer
        global direction_x
        global direction_y
        if pygame.K_RIGHT in keys:
            scooby.x += 12
        if pygame.K_LEFT in keys:
            scooby.x -= 12
        if pygame.K_UP in keys:
            scooby.y -= 22
        scooby.yspeed += 1
        scooby.y += scooby.yspeed
        timer -= 1
        seconds = str(int((timer / ticks_per_second))).zfill(3)
        frame += 1
        counter += 1
        if frame == 10:
            frame = 0
        if counter % 2 == 0:
            scooby.image = sheet[frame + direction * 20]
        camera.clear("black")
        camera.draw(scooby)
        camera.x += 5
        for enemy in enemies:
            enemy.xspeed = 1
            enemy.x += enemy.xspeed
            if enemy.touches(scooby):
                if BOUNDS_ACTION == "remove":
                    enemy.x = 0
                    health -= 1
            camera.draw(enemy)
        camera.draw(ground)
        for snack in snacks:
            if scooby.touches(snack):
                score += 1
                if BOUNDS_ACTION == "remove":
                    snack.x = 0
            camera.draw(snack)
        for box in boxes:
            if scooby.touches(box):
                score += 5
                if BOUNDS_ACTION == "remove":
                    box.x = 0
            camera.draw(box)
        for wall in walls:
            if scooby.bottom_touches(wall):
                scooby.yspeed = 0
            if scooby.touches(wall):
                scooby.move_to_stop_overlapping(wall)
            camera.draw(wall)
        timer_box = gamebox.from_text(camera.x, 30, "Timer: " + str(seconds), "arial", 18, "white")
        health_box = gamebox.from_text(camera.x + 350, 30, "Health: " + str(health), "arial", 18, "white")
        score_box = gamebox.from_text(camera.x - 350, 30, "Score: " + str(score), "arial", 18, "white")
        camera.draw(timer_box)
        camera.draw(health_box)
        camera.draw(score_box)
        if health == 0 or timer == 0 or scooby.touches(ground):
            gamebox.pause()
            game_over_text = gamebox.from_text(camera.x, 300, "GAME OVER", "arial", 65, "red", True)
            camera.draw(game_over_text)
            final_score = gamebox.from_text(camera.x, 350, "SCORE: " + str(score), "arial", 36, "red", True)
            camera.draw(final_score)
        elif scooby.x >= camera.x + 400 or scooby.x <= camera.x - 400 or scooby.y <= 0:
            gamebox.pause()
            game_over_text = gamebox.from_text(camera.x, 300, "GAME OVER", "arial", 65, "red", True)
            camera.draw(game_over_text)
            final_score = gamebox.from_text(camera.x, 350, "SCORE: " + str(score), "arial", 36, "red", True)
            camera.draw(final_score)
    else:
        if pygame.K_SPACE in keys:
            game_over = False
            scooby.x = camera.x
            health = 3
            score = 0
            timer = 1800
            scooby.y = 30
        camera.clear("black")
        instructions1 = "Ruh-roh, you're Scooby Doo & you want your scooby snacks! 1 snack = 1 point, 1 box = 5 points."
        instructions2 = "But there are monsters on the loose, so beware. One touch = one life lost."
        instructions3 = "Don't fall off the ledges into the water and be sure to stay on the screen. Otherwise, the game will end."
        instructions4 = "Left = left-arrow key, Right = right-arrow key, Jump = up-arrow key."
        instructions5 = "Press space to start."
        instructions = "INSTRUCTIONS:"
        rules_box1 = gamebox.from_text(camera.x, 380, instructions1, "arial", 12, "blue")
        camera.draw(rules_box1)
        rules_box2 = gamebox.from_text(camera.x, 410, instructions2, "arial", 12, "blue")
        camera.draw(rules_box2)
        rules_box3 = gamebox.from_text(camera.x, 440, instructions3, "arial", 12, "blue")
        camera.draw(rules_box3)
        rules_box4 = gamebox.from_text(camera.x, 470, instructions4, "arial", 12, "blue")
        camera.draw(rules_box4)
        rules_box5a = gamebox.from_text(camera.x, 500, instructions5, "arial", 24, "blue")
        camera.draw(rules_box5a)
        rules_box5 = gamebox.from_text(camera.x, 350, instructions, "arial", 12, "blue", bold=True)
        camera.draw(rules_box5)
        name_box1 = gamebox.from_text(camera.x, 180, "The Creators:", "arial", 12, "white", bold=True)
        camera.draw(name_box1)
        name_box2 = gamebox.from_text(camera.x, 200, "Arshiya Ansari (aa9yk)", "arial", 12, "white")
        camera.draw(name_box2)
        name_box3 = gamebox.from_text(camera.x, 220, "Rex Focht (rwf2cb)", "arial", 12, "white")
        camera.draw(name_box3)
        game_name = gamebox.from_image(camera.x, 70, 'scoobyjump.png')
        camera.draw(game_name)
    camera.display()


ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)


