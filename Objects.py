import pygame
import random
from pygame.locals import *
from Imports import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, image, chosen_character):
        self.groups = game.allsprites, game.Players
        pygame.sprite.Sprite.__init__(self, self.groups)
        '''
        image = pygame.Surface((32,32))
        image.fill((255,255,255))
        '''
        self.image = image
        self.rect = self.image.get_rect()

        self.speed = game.settings["Player speed"]
        self.HP = game.settings["Player HP"]
        self.Max_HP = game.settings["Player HP"]
        self.hurt_timer = int(game.settings["Hurt Timer"])
    
        self.x = x * 32
        self.y = y * 32

        self.move_x = 0
        self.move_y = 0

        self.width = width
        self.height = height
        
        self.current_weapon = None
        self.chosen_character = chosen_character
        
        self.idle_left = []
        self.idle_right = []
        self.walk_right = []
        self.walk_left = []

        self.sens = "right"

        self.animation_timer = 0

        self.game = game


    def get_keys(self):
        self.move_x, self.move_y = 0, 0
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.move_y -= self.speed
            if self.sens == "right":
                self.Animate(self.walk_right, 15)
            else:
                self.Animate(self.walk_left, 15)
        if key[pygame.K_s]:
            self.move_y += self.speed
            if self.sens == "right":
                self.Animate(self.walk_right, 15)
            else:
                self.Animate(self.walk_left, 15)
        if key[pygame.K_a]:
            self.move_x -= self.speed
            self.sens = "left"
            self.Animate(self.walk_left, 15)
        if key[pygame.K_d]:
            self.move_x += self.speed
            self.sens = "right"
            self.Animate(self.walk_right, 15)

        if self.move_x != 0 and self.move_y != 0:
            self.move_x = self.move_x * 0.7
            self.move_y = self.move_y * 0.7
        
        if self.move_x == 0 and self.move_y == 0:
            if self.sens == "right":
                self .Animate(self.idle_right, 15)
            else:
                self.Animate(self.idle_left, 15)

    def collide_walls(self, direction):
        
        if direction == 'x':
            hit = pygame.sprite.spritecollide(self, self.game.Walls, False)
            if hit:
                if self.move_x > 0:
                    self.x = hit[0].rect.left - self.rect.width
                if self.move_x < 0:
                    self.x = hit[0].rect.right
                
                self.move_x = 0
                self.rect.x = self.x

        if direction == 'y':
            hit = pygame.sprite.spritecollide(self, self.game.Walls, False)
            if hit:
                if self.move_y > 0:
                    self.y = hit[0].rect.top - self.height
                if self.move_y < 0:
                    self.y = hit[0].rect.bottom

                self.move_y = 0
                self.rect.y = self.y

    def Animate(self, images, speed):
        total_anim_speed = speed * len(images)

        if self.game.animation_assigned:
            if self.animation_timer < total_anim_speed:
                self.image = images[int(self.animation_timer/speed)]
                self.animation_timer += 1
            else:
                self.animation_timer = 0

    def update(self):
        self.get_keys()
        self.x += self.move_x
        self.y += self.move_y
        self.rect.x = self.x
        self.collide_walls('x')
        self.rect.y = self.y
        self.collide_walls('y')
        
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            
        else:
            hit_ennemi = pygame.sprite.spritecollide(self, self.game.Ennemies, False)
            hit_boss = pygame.sprite.spritecollide(self, self.game.Bosses, False)
            if hit_ennemi or hit_boss:
                for enn in hit_ennemi or hit_boss:
                    if self.HP - enn.damage <= 0:
                        self.HP = 0
                    else:
                        self.HP -= enn.damage
                    self.hurt_timer = self.game.settings["Hurt Timer"]


        if self.HP > self.Max_HP:
            self.HP -= 1
        
    

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.allsprites, game.Walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        image = pygame.Surface((32,32))
        image.fill((255,255,255))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * game.settings["TILESIZE"]
        self.rect.y = y * game.settings["TILESIZE"]


class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, room):
        self.groups = game.allsprites, game.Doors, game.Walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        image = pygame.Surface((32,32))
        image.fill((255,255,255))
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x * game.settings["TILESIZE"]
        self.y = y * game.settings["TILESIZE"]

        self.rect.x = self.x
        self.rect.y = self.y
        
        self.closing_timer = 15

        self.room = room
        self.game = game

    def update(self):
        if self.game.current_room == self.room and self.game.floor[self.room]["Ennemies"] > 0:
            
            if self.closing_timer < 0:
                self.rect.x = self.x
                self.rect.y = self.y
            else:
                self.closing_timer -= 1
        else:
            self.rect.x = 3000000
            self.rect.y = 3000000

        hit = pygame.sprite.spritecollide(self.game.player, self.game.Door_holders, False)
        if hit:
            self.rect.x = 3000000
            self.rect.y = 3000000
        
        
class Door_holder(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups =  game.Door_holders
        pygame.sprite.Sprite.__init__(self, self.groups)
        image = pygame.Surface((32,32))
        image.fill((0,0,0))
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x * game.settings["TILESIZE"]
        self.y = y * game.settings["TILESIZE"]

        self.rect.x = self.x
        self.rect.y = self.y


class Room_DETECT(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.allsprites, game.RoomFinders
        pygame.sprite.Sprite.__init__(self, self.groups)
        image = pygame.Surface((32,32))
        image.fill((0,0,0))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * game.settings["TILESIZE"]
        self.rect.y = y * game.settings["TILESIZE"]


class Room_Marker(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.allsprites, game.RoomMarkers
        pygame.sprite.Sprite.__init__(self, self.groups)
        image = pygame.Surface((32,32))
        image.fill((0,0,0))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * game.settings["TILESIZE"]
        self.rect.y = y * game.settings["TILESIZE"]


class MAP:
    def __init__(self, game, file, type):
        self.data = []
        with open(file, 'rt') as f:
            for line in f:
                self.data.append(line)

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = (self.tilewidth - 1) * game.settings["TILESIZE"]
        self.height = self.tileheight * game.settings["TILESIZE"]

        self.type = type


class Camera:
    def __init__(self, game, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.game = game
        self.X = 0
        self.Y = 0
    
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x =  - target.rect.x + int(self.game.settings["Screen width"]/2)
        y = - target.rect.y + int(self.game.settings["Screen height"]/2)
        
        self.X = x
        self.Y = y
        
        self.camera = pygame.Rect(x, y, self.width, self.height)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, sprite, health):
        self.groups = game.allsprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.image.load(game.Weapons[game.player.current_weapon.name]["Projectile Image"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = health
        self.alive_time = 60

        self.damage = game.Weapons[game.player.current_weapon.name]["Damage"]

        self.game = game

        pos = pygame.mouse.get_pos()
        pos = [pos[0] - self.game.camera.X, pos[1] - self.game.camera.Y]

        self.distance_x = pos[0] - self.game.player.current_weapon.shoot_point[0]
        self.distance_y = pos[1] - self.game.player.current_weapon.shoot_point[1]

    def update(self):
        
        hit_wall = pygame.sprite.spritecollide(self, self.game.Walls, False)
        if hit_wall:
            self.kill()
        if self.health > 0:
            self.rect.center = (self.rect.center[0] + self.distance_x * 0.1, self.rect.center[1] + self.distance_y * 0.1)
            self.health -= 1
        if self.alive_time > 0:
            self.alive_time -= 1
        else:
            self.kill()

        hit_ennemies = pygame.sprite.spritecollide(self, self.game.Ennemies, False)
        if hit_ennemies:
            for ennemi in hit_ennemies:
                if ennemi.Angery_time <= 0:
                    ennemi.hp -= self.damage
                self.kill()

       
class Slime(pygame.sprite.Sprite):
    def __init__(self, game, x, y, target, hp, damage, room):
        self.groups = game.allsprites, game.Ennemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x #* game.settings["TILESIZE"]
        self.y = y #* game.settings["TILESIZE"]

        num = random.randint(0, 3)
        self.image = slime_walk[num]
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.room = room
        self.target = target
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.game = game

        self.Angery_time = 15

        self.animation_timer = 0

    def update(self):
        
        
        if  self.Angery_time <= 0 and self.game.current_room == self.room:
                
            if self.target.rect.center[0] > self.rect.center[0]:
                self.rect.x += 2
            if self.target.rect.center[0] < self.rect.center[0]:
                self.rect.x -= 2

            if self.target.rect.center[1] > self.rect.center[1]:
                self.rect.y += 2
            if self.target.rect.center[1] < self.rect.center[1]:
                self.rect.y -= 2 

            self.Animate(slime_walk, 15)
        
        else:
            self.Angery_time -= 1
            self.hp = self.max_hp

        if self.hp <= 0:
            self.game.floor[self.room]["Ennemies"] -= 1
            
            num = random.randint(1, 50)
            if num >= 1 and num <= 10:
                Pickup(self.game, self.rect.x, self.rect.y, heart_pickup, "Health")
            
            if num > 10 and num <= 20:
                Pickup(self.game, self.rect.x, self.rect.y, ammo1_pickup, "Ammo 1")

            if num >= 45:
                Pickup(self.game, self.rect.x, self.rect.y, ammo2_pickup, "Ammo 2")
            
            self.kill()


    def Animate(self, images, speed):
        total_anim_speed = speed * len(images)

        if self.game.animation_assigned:
            if self.animation_timer < total_anim_speed:
                self.image = images[int(self.animation_timer/speed)]
                self.animation_timer += 1
            else:
                self.animation_timer = 0


class Boss_slime(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image, travel_points, hp, damage):
        self.groups = game.allsprites, game.Bosses, game.Ennemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

        self.is_at = 0

        self.hp = hp
        self.damage = damage

        self.Angery_time = 0

        self.travel_points = travel_points

    def update(self):

        if self.travel_points[self.is_at][0] > self.rect.center[0]:
            self.rect.x += 2
        if self.travel_points[self.is_at][0] < self.rect.center[0]:
            self.rect.x -= 2
        
        if self.travel_points[self.is_at][1] > self.rect.center[1]:
            self.rect.y += 2
        if self.travel_points[self.is_at][1] < self.rect.center[1]:
            self.rect.y -= 2

        hit = pygame.sprite.spritecollide(self.game.player, self.game.Bosses, False)

        if hit:
            if self.Angery_time >= 15:
                self.game.player.HP -= self.damage
                self.Angery_time = 0

        if self.hp <= 0:
            Portal(self.game, self.rect.x / 32 , self.rect.y / 32, 'a', False)
            self.kill()



        if self.travel_points[self.is_at][0] + 5 > self.rect.center[0] and self.travel_points[self.is_at][0] - 5 < self.rect.center[0]:
            if self.travel_points[self.is_at][1] + 5 > self.rect.center[1] and self.travel_points[self.is_at][1] - 5 < self.rect.center[1]:
                if self.is_at < len(self.travel_points) - 1:
                    self.is_at += 1
                else:
                    self.is_at = 0


class Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y, sprite, function, need_argument = None, argument = None):
        self.groups = game.Menu_UI
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = sprite
        self.rect = self.image.get_rect()
        #self.rect.x = x
        #self.rect.y = y

        self.rect.center = x, y

        self.x = x
        self.y = y

        self.width = self.image.get_rect()
        self.height = self.image.get_height()

        self.need_argument = need_argument or False
        self.argument = argument

        self.function = function
        self.game = game

    def update(self):
        click = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        
        if pos[0] > self.rect.left and pos[0] < self.rect.right:
            if pos[1] < self.rect.bottom and pos[1] > self.rect.top:
                if click == (1,0,0):
                    
                    if self.need_argument:
                        self.function(self.argument)
                    else:
                        self.function()
                pygame.draw.rect(self.game.screen, (255,255,255), (self.rect), 5)

                
class Heart_half(pygame.sprite.Sprite):
    def __init__(self, game, x, y, health, sprite):
        self.groups = game.UI
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = health

        self.x = x
        self.y = y

        self.game = game

    def update(self):
        if self.game.player.HP < self.health + 1 :
            self.rect.y = - 100
        else:
            self.rect.y = self.y


class Heart_container(pygame.sprite.Sprite):
    def __init__(self, game, x, y, sprite):
        self.groups = game.UI
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Portal(pygame.sprite.Sprite):
    def __init__(self, game, x, y, sprite, next_floor):
        self.groups = game.allsprites, game.Portals
        pygame.sprite.Sprite.__init__(self, self.groups)

        image = pygame.Surface((64,64))
        image.fill((0,0,100))
        
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = x * game.settings["TILESIZE"]
        self.rect.y = y * game.settings["TILESIZE"]

        self.next_floor = next_floor

        self.game = game

    def update(self):
        hit = pygame.sprite.spritecollide(self.game.player, self.game.Portals, False)
        if hit:
            self.game.boss_warp = not self.game.boss_warp
            self.game.has_warp_spawned = False
            if self.game.in_boss_room:
                self.game.in_boss_room = False
            else:
                self.game.finished_floors += 1
            self.game.restart_game()


class Pickup(pygame.sprite.Sprite):
    def __init__(self, game, x, y, sprite, type):
        self.groups = game.allsprites, game.Pickups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type

        self.game = game
    
    def update(self):
        hit = pygame.sprite.spritecollide(self.game.player, self.game.Pickups, False)
        if hit:
            for sprite in hit:
                if sprite.type == "Health":
                    self.game.player.HP += 1
                    sprite.kill()
                
                if sprite.type == "Ammo 1":
                    self.game.player.current_weapon.ammo = self.game.player.current_weapon.max_ammo
                    sprite.kill()

                if sprite.type == "Ammo 2":
                    for weapon in self.game.weapon_inventory:
                        weapon.ammo += 25
                    sprite.kill()


class Weapon_distance(pygame.sprite.Sprite):
    def __init__(self, game, holder, weapon):
        self.groups = game.allsprites, game.WEAPONS
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load(game.Weapons[weapon]["Image"])
        self.rect = self.image.get_rect()

        self.name = game.Weapons[weapon]["Name"]
        self.ammo = game.Weapons[weapon]["Ammo"]
        self.max_ammo = game.Weapons[weapon]["Ammo"]

        self.rect.topleft = holder.rect.topright 
        self.shoot_point = 0

        self.side = 0 #0 droite et 1 gauche
        self.lastside = self.side
        self.holder = holder
        
        self.game = game
    
    def update(self):
        
        pos = pygame.mouse.get_pos()

        if self.game.Weapons[self.name]["Name"] == self.game.weapon_inventory[self.game.weapon_inventory_spot].name:

            if pos[0] - self.game.camera.X > self.holder.rect.x:
                self.rect.topleft = self.holder.rect.midright
                self.shoot_point = self.rect.topright
                self.side = 0
            else:
                self.rect.topright = self.holder.rect.midleft
                self.shoot_point = self.rect.topleft
                self.side = 1

            if self.lastside != self.side:
                self.lastside = self.side
                self.image = pygame.transform.flip(self.image, True, False)

        else:
            self.rect.x = 300000
            self.rect.y = 300000

        if self.ammo > self.max_ammo:
            self.ammo = self.max_ammo


class Weapon_UI(pygame.sprite.Sprite):
    def __init__(self, game, x, y, sprite):
        self.groups = game.UI
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = sprite

        self.x = x 
        self.y = y

        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def update(self):
        self.rect.center = self.x, self.y


class Chest(pygame.sprite.Sprite):
    def __init__(self, game, x, y, loot, rarety, images):
        self.groups = game.allsprites, game.Chests
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()

        self.rect.x = self.x * game.settings["TILESIZE"]
        self.rect.y = self.y * game.settings["TILESIZE"]

        self.Opened = False

        self.game = game

    def update(self):
        key = pygame.key.get_pressed()

        hit = pygame.sprite.spritecollide(self.game.player, self.game.Chests, False)
        if hit:
            for chest in hit:
                if key[pygame.K_e] and not self.Opened:
                    self.Opened = True
                    self.image = self.images[1]


class key_pop_up(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image, key, radius):
        self.groups = game.allsprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y

        self.image = image
        self.rect = self.image.get_rect()
        self.key = key
        self.radius = radius

        self.rect.x = self.x
        self.rect.y = self.y

        self.game = game

    def update(self):
        if self.game.player.x > self.radius[0] and self.game.player.x < self.radius[1] and self.game.player.y > self.radius[2] and self.game.player.y < self.radius[3]:
            pass
        else:
            self.kill()
        
        