# Cannon sim 
# by Elijah Medrano
# 1/14/22
# Shoot down the paratroopers
# I wrote this game using only functinos instead of classes and learned to use "init()" 
# functions to set initial values to allow for iterative changes in the game loop

# SEE def.images() TO SET CORRECT DIRECTORY

import pygame as pg
from math import sin, asin, cos, sqrt
from random import randrange

pg.init()
display_w = 500
display_h = 600
window = pg.display.set_mode((display_w, display_h))
pg.display.flip()


def text():
  font = pg.font.Font('freesansbold.ttf', 32)
  level = 'Level ' + str(level_init.level)
  text.level = font.render(level, True, colors.black)
  score = 'Score: ' + str(level_init.score)
  text.score = font.render(score, True, colors.black)
  text.shoot = font.render('shoot: 1', True, colors.black)
  text.restart = font.render('restart: esc', True, colors.black)


def images():
  images.cloud = pg.image.load('cloud.png')
  images.cloud_w = 100
  images.cloud = pg.transform.scale(images.cloud, (images.cloud_w, 100))
  
  images.soldier = pg.image.load('soldier.png')


def colors():
  colors.black = (0, 0, 0)
  colors.white = (255, 255, 255)
  colors.sky_blue = (135,206,235)
  colors.dirt_brown = (150,90,62)
  colors.cannon_green = (0, 100, 0)
  colors.gun_gray = (128,128,128)
  colors.bullet_yellow = (250,218,94)


def level_init():
  level_init.score = 0
  level_init.level = 0


def infantry():
  pass


def trooper_init():
  trooper_init.min_vel = 10
  trooper_init.max_vel = 20
  trooper_init.troopers = [] 
  for _ in [*range(0, 5)]:  # create _ troopers
    trooper_init.troopers.append([randrange(0, display_w, 20), 0, 
                                  randrange(trooper_init.min_vel, 
                                            trooper_init.max_vel, 2)])  # x, y, y_vel


def cloud_init():
  cloud_init.clouds = []
  for _ in [*range(0, 2)]:  # create _ clouds
    cloud_init.clouds.append([randrange(0, display_w, 400), 
                              randrange(20, 400, 20), 
                              randrange(30, 50, 10)])  # x, y, vel


def artillery_init():
  artillery_init.shells = []
  artillery_init.shell_size = 5
  artillery_init.vel = 0.001


def bullet_init():
  bullet_init.bullets = []
  bullet_init.size = 4
  bullet_init.vel = 0.01
  bullet_init.m_x = 0
  bullet_init.m_y = 0


def cannon():  # position cannon and gun
  # set cannon dimensions
  cannon.w = 50
  cannon.h = 20
  cannon.gun_start_point = [0, 0]
  cannon.gun_endpoint = [0, 0]
  gun_length = 30
  
  # place cannon
  cannon.x = display_w / 2 - cannon.w / 2
  cannon.y =  display_h - cannon.h
  
  # set the gun start point in the top center of the cannon
  cannon.gun_start_point[0] = cannon.x + cannon.w / 2
  cannon.gun_start_point[1] = cannon.y
  
  # get distance from gun start point to mouse position
  mouse_pos = pg.mouse.get_pos()
  distance = sqrt((mouse_pos[0] - cannon.gun_start_point[0]) ** 2 + (mouse_pos[1] - 
                   cannon.gun_start_point[1]) ** 2)
  
  # using that distance calculate the angle between the line orthogonal to the center of the cannon 
  # and the gun line from the gun start position to the mouse position
  if distance > 0:
    cannon.theta = asin(abs(mouse_pos[0] - cannon.gun_start_point[0]) / distance)
  else:
    cannon.theta = 1.57  # pi / 2
  
  # find the lengths of the sides of the similar triangle created by the hypotenuse of length gun_length 
  # on the gun line
  x = gun_length * sin(cannon.theta)
  y = gun_length * cos(cannon.theta)
  
  # add the x and y values to the coordinate gun_start_point to get the coordinates of gun_endpoint
  if mouse_pos[0] >= cannon.gun_start_point[0]:
    cannon.gun_endpoint[0] = cannon.gun_start_point[0] + x
  elif mouse_pos[0] < cannon.gun_start_point[0]:
    cannon.gun_endpoint[0] = cannon.gun_start_point[0] - x
  
  cannon.gun_endpoint[1] = cannon.gun_start_point[1] - y


def draw():  # draw all objects
  # draw text
  window.blit(text.level, (0, 0))
  window.blit(text.score, (0, 30))
  window.blit(text.shoot, (0, display_h - 30))
  window.blit(text.restart, (0, display_h - 60))
  
  # draw paratroopers
  trooper_i = 0
  for trooper in trooper_init.troopers:
    if trooper[1] + 20 < display_h:  # if not on ground
      trooper[1] += trooper[2] / 1000  # move trooper in y direction
    window.blit(images.soldier, (trooper[0], trooper[1]))  # draw
    for bullet in bullet_init.bullets:  # pop if shot
      if trooper[0] < bullet[0] < trooper[0] + 20 and trooper[1] < bullet[1] < trooper[1] + 20:  # hitbox
        trooper_init.troopers.pop(trooper_i)  # pop
        trooper_init.troopers.append([randrange(0, display_w, 20), 0, 
                                      randrange(trooper_init.min_vel, 
                                                trooper_init.max_vel, 2)])  # x, y, x_v, y_v
        level_init.score += 1  # count kills
        if level_init.score % 10 == 0:  # level up
          level_init.level += 1
          trooper_init.min_vel += 10  # increase vel
          trooper_init.max_vel += 10
    trooper_i += 1    
  
  # draw clouds
  cloud_i = 0
  for cloud in cloud_init.clouds:
    cloud[0] += cloud[2] / 1000  # move cloud
    window.blit(images.cloud, (cloud[0], cloud[1]))  # draw
    if cloud[0] > display_w / 3 and len(cloud_init.clouds) < 3:  # append new cloud x, y, vel
      cloud_init.clouds.append([0 - images.cloud_w, randrange(20, 400, 20), randrange(30, 50, 10)])  
    if cloud[0] > display_w:  # pop cloud if leaves display
      cloud_init.clouds.pop(cloud_i)
    cloud_i += 1
  
  # draw ground
  pg.draw.line(window, colors.dirt_brown, (0, display_h), (display_w, display_h), 10)  
  
  # draw cannon
  pg.draw.rect(window, colors.cannon_green, (cannon.x, cannon.y, cannon.w, cannon.h))  
  
  # draw gun
  pg.draw.line(window, colors.gun_gray, cannon.gun_start_point, cannon.gun_endpoint, 3)  
  
  # draw bullets
  bullet_i = 0
  for bullet in bullet_init.bullets:
    bullet[0] += bullet_init.vel * bullet[2]  # update bullet x pos; bullet[2] = x slope comp
    bullet[1] -= bullet_init.vel * bullet[3]  # update bullet y pos; bullet[3] = y slope comp
    pg.draw.circle(window, colors.bullet_yellow, (int(bullet[0]), int(bullet[1])), bullet_init.size)  
    # pop bullets if they leave display
    if bullet[0] < 0:  
      bullet_init.bullets.pop(bullet_i)
    elif bullet[0] > display_w:
      bullet_init.bullets.pop(bullet_i)
    elif bullet[1] < 0:  
      bullet_init.bullets.pop(bullet_i)
    bullet_i += 1

  # draw artillery
    

def main():
  # Initialize
  images()
  colors()
  level_init()
  cloud_init()
  bullet_init()
  artillery_init()
  trooper_init()
  
  # Game loop
  while 1:
    # setup
    cannon()
    text()
    
    # check keystrokes
    keys = pg.key.get_pressed()
    
    # operate on keystrokes
    for event in pg.event.get():
      if event.type == pg.QUIT:
        quit()
        
      if event.type == pg.KEYUP:
        # append bullet: x, y, x slope comp, y slope comp
        if keys[pg.K_1] and len(bullet_init.bullets) < 5:  # shoot 50 cal
          bullet_init.bullets.append([cannon.gun_endpoint[0], cannon.gun_endpoint[1], 
                                      cannon.gun_endpoint[0] - cannon.gun_start_point[0],
                                      cannon.gun_start_point[1] - cannon.gun_endpoint[1]])
                                      
        if keys[pg.K_2] and len(artillery_init.shells) < 2:  # shoot artillery
          # append shell: x, y, theta
          artillery_init.shells.append([cannon.gun_endpoint[0], cannon.gun_endpoint[1], cannon.theta])
        
        if keys[pg.K_ESCAPE]:  # restart
          trooper_init.troopers.clear()
          trooper_init()
          level_init.score = 0
          level_init.level = 0
    
    # draw all objects
    draw()
    
    # update and refresh window
    pg.display.update()
    window.fill(colors.sky_blue)
  

if __name__ == '__main__':
  main()
