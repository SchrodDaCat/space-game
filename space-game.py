import pgzrun
import random

WIDTH = 500
HEIGHT = 600
score = 0
lives = 10
vel = (0, -500)
vel2 = (0, 50)
vel3 = (0, 100)
vel4 = (0, 150)
MOVE_DISTANCE = 5
space = 25
game_over = False
ship = Actor("ship")
ship.pos = 250, HEIGHT - 100
projectile_list = []
object_list = []
enemy_list = []
enemy_projectile_list = []
was_keyboard_space = False

def draw():
    screen.clear()

    for object in object_list:
        object.draw()

    for projectile in projectile_list:
        projectile.draw()

    for enemy in enemy_list:
        enemy.draw()

    for enemy_projectile in enemy_projectile_list:
        enemy_projectile.draw()

    ship.draw()

    screen.draw.text("score: " + str(score), color="white", topright=(475, 25))
    screen.draw.text("lives: " + str(lives), color="red", topleft=(25, 25))

    if game_over == True:
        screen.draw.text("Game Over", (200, 300), color=(255, 255, 255), fontsize=60)
        screen.draw.text("Final Score: " + str(score), (200, 350), color=(255, 0, 0), fontsize=30)

def update(dt):
    global score, lives, game_over, projectile_list, was_keyboard_space, projectile_pos, object_list, object_pos, enemy_list, enemy_projectile_list

    if keyboard.right:
        ship.x += MOVE_DISTANCE
        if ship.x > WIDTH-space:
            ship.x = WIDTH-space
    if keyboard.left:
        ship.x -= MOVE_DISTANCE
        if ship.x < space:
            ship.x = space
    if keyboard.down:
        ship.y += MOVE_DISTANCE
        if ship.y > HEIGHT-space:
            ship.y = HEIGHT-space
    if keyboard.up:
        ship.y -= MOVE_DISTANCE
        if ship.y < space:
            ship.y = space
    if keyboard.space and not was_keyboard_space:
        projectile = Actor("projectile")
        projectile.pos = ship.x, ship.y
        projectile_list.append(projectile)
    was_keyboard_space = keyboard.space
    for projectile in projectile_list:
        projectile.pos = (projectile.pos[0] + vel[0] * dt, projectile.pos[1] + vel[1] * dt)
    projectile_list = [p for p in projectile_list if p.y > 0]

    if random.random() < 0.02:
        enemy = Actor("enemy")
        enemy.pos = random.random() * WIDTH, 0
        enemy_list.append(enemy)
        enemy_projectile = Actor("enemy_projectile")
        enemy_projectile.pos = enemy.pos
        enemy_projectile_list.append(enemy_projectile)

    if random.random() < 0.002:
        object = Actor("object")
        object.pos = random.random() * WIDTH, 0
        object_list.append(object)

    for object in object_list:
        object.pos = (object.pos[0] + vel2[0] * dt, object.pos[1] + vel2[1] * dt)
    object_list = [b for b in object_list if b.y < 800]

    for enemy in enemy_list:
        enemy.pos = (enemy.pos[0] + vel3[0] * dt, enemy.pos[1] + vel3[1] * dt)
    enemy_list = [e for e in enemy_list if e.y < 800]

    for enemy_projectile in enemy_projectile_list:
        enemy_projectile.pos = (enemy_projectile.pos[0] + vel4[0] * dt, enemy_projectile.pos[1] + vel4[1] * dt)
    enemy_projectile_list = [e2 for e2 in enemy_projectile_list if e2.y < 800]

    for enemy in enemy_list:
        projectile_index = enemy.collidelist(projectile_list)
        if projectile_index >= 0:
            if game_over == False:
                score = score + 1
            enemy_list.remove(enemy)

    for enemy_projectile_ in enemy_projectile_list:
        enemy_projectile_index = ship.collidelist(enemy_projectile_list)
        if enemy_projectile_index >= 0:
            if game_over == False:
                lives = lives - 1
            del enemy_projectile_list[enemy_projectile_index]

    if lives == 0:
        game_over = True

pgzrun.go()
