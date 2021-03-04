import pygame
from pygame.locals import *

bullet = pygame.image.load("Sprites/Weapons/bullet.png")

quit_button = pygame.image.load("Sprites/UI/quit_button.png")
start_button = pygame.image.load("Sprites/UI/start_button.png")

Red = pygame.Surface((32, 32))
Red.fill((255, 0, 0))

Green = pygame.Surface((32, 32))
Green.fill((0, 255, 0))

slime_0 = pygame.image.load("Sprites/Characters/Ennemies/Slime/slime_0.png")
slime_1 = pygame.image.load("Sprites/Characters/Ennemies/Slime/slime_1.png")
slime_2 = pygame.image.load("Sprites/Characters/Ennemies/Slime/slime_2.png")
slime_3 = pygame.image.load("Sprites/Characters/Ennemies/Slime/slime_3.png")

slime_walk = [slime_0, slime_1, slime_2, slime_3]


Red_portrait = pygame.image.load("Sprites/Player portraits/Red.png")
Green_portrait = pygame.image.load("Sprites/Player portraits/Green.png")
Witch_portrait = pygame.image.load("Sprites/Player portraits/Witch.png")

heart_container = pygame.image.load("Sprites/UI/heart_container.png")
left_heart = pygame.image.load("Sprites/UI/heart_left_half.png")
right_heart = pygame.image.load("Sprites/UI/heart_right_half.png")

heart_pickup = pygame.image.load("Sprites/Pickups/Heart.png")
ammo1_pickup = pygame.image.load("Sprites/Pickups/Ammo.png")
ammo2_pickup = pygame.image.load("Sprites/Pickups/Ammo_2.png")

weapon_holder = pygame.image.load("Sprites/UI/weapon_holder_UI.png")