# Barna Alimu, kyb2rw
import pygame
import gamebox
import random

camera = gamebox.Camera(800,600)
p = gamebox.from_color(200, 400, "light green", 25, 25)

acc = 0
block_velocity = 10
p_velocity = 5 + acc
p_speed = 14
p_score = 0
game_end = False

p.xspeed = 0
p.yspeed = p_velocity

height = 600

blocks = [
    gamebox.from_color(100, 100, "pink", 1000, 20),
]


trigger = gamebox.from_color(0, -10, "green", 1600, 20)
game_over = gamebox.from_text(400, 300, "Game Over!", 100, "Black", bold=True)


def create_block():
    global height
    global p_score
    ran = random.randint(1, 14) *100
    height += 100
    gap = ran
    if height % 200 == 0:
        blocks.append(gamebox.from_color(0, height, "magenta", gap, 25))
        blocks.append(gamebox.from_color(gap/2 + 875, height, "magenta", 1600, 25))
    else:
        blocks.append(gamebox.from_color(0, height, "white", gap, 25))
        blocks.append(gamebox.from_color(gap / 2 + 875, height, "white", 1600, 25))

def tick(keys):
    global game_end
    global p_speed
    global p_score
    global acc

    game_over.y += 5


    # ------- INPUT ---------
    if pygame.K_LEFT in keys:
        p.x -= p_speed

    if pygame.K_RIGHT in keys:
        p.x += p_speed
    camera.move(0, 5)
    trigger.move(0,5)

    if p.x > 800:
        p.x = 790
    if p.x < 0:
        p.x = 10

    p.move_speed()


    # -----movement logic & acceleration-------
    for block in blocks:
        if p.touches(block, 1):
            p.move_to_stop_overlapping(block)
            acc = 0
        else:
            if acc < 6:
                acc += .02
            p.yspeed = 5 + acc


    #-------scoring ---------
    if camera.y % 150 == 0:
        p_score += 1

    #-------game end logic-------
    if p.touches(trigger):
        game_end = True

    # ----------draw background------#
    camera.clear("pink")
    # draw all the blocks
    for block in blocks:
        camera.draw(block)
        if block.touches(trigger):
            create_block()


    # -------Draw the player and trigger------#
    camera.draw(gamebox.from_text(400, 300, "Game Start!", 100, "white", bold=False))
    camera.draw(p)
    camera.draw(trigger)
    camera.draw(gamebox.from_text(80, camera.y + 250 , "score: " + str(p_score) + " secs", 30, "red", bold=False))
    camera.display()


    if game_end:
        camera.clear("pink")
        camera.draw(gamebox.from_text(400, camera.y, "Game Over!", 100, "Black", bold=False))
        camera.draw(gamebox.from_text(400, camera.y + 150, "I SURVIVED " + str(p_score) + " SECONDS!", 60, "white", bold=False))
        gamebox.pause()
    camera.display()

ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)
