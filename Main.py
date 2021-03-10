import pygame
import json
import random
from pygame.locals import *
from Objects import *
from Imports import *


RUNNING = True

# HA HA j'ai encore tout rework

pygame.init()


def create_room(game, xOFFSET, yOFFSET, room):
    """Fonction qui génrère la map a chaque début de niveau"""

    first = True

    TOPLEFT = 0
    BOTTOMRIGHT = 0
    game.num_of_rooms += 1
    #room_door = []

    for row, tiles in enumerate(room.data):

        # La ça regarde chaque ligne de la map pour la construire la map de base
        # Dès qu'il trouve un trou (D) il vas se relancer jusqu'a qu'il n'y ait plus de trous

        for col, tile in enumerate(tiles):

            # Selon le char il spawn le bon truc

            if tile == "D":
                door = Door(game, col + xOFFSET, row +
                            yOFFSET, 32, 32, game.num_of_rooms)
                game.floor.append(None)
                Door_holder(game, col + xOFFSET, row + yOFFSET, 32, 32)
                # En général chaque entitée spawnable est construite comme ça de base: Machin(la classe game, pos x, pos y, sprite (ou longueur largeur si ya pas de sprite))
                # Les offset en gros c'est que on prend la position sur la map (a partir de 0,0) + le décalage pour pas faire tt sur la mêm pièce
            if tile == "1":
                wall = Wall(game, col + xOFFSET, row + yOFFSET, 32, 32)
                if first:
                    TOPLEFT = (wall.rect.topleft[0], wall.rect.topleft[1])
                    BOTTOMRIGHT = (
                        wall.rect.bottomleft[0] + (16 * 32), wall.rect.topleft[1] + (16 * 32))
                    first = False

            if tile == "A":
                Room_Marker(game, col + xOFFSET, row + yOFFSET, 32, 32)

            if tile == "W":
                if not game.has_warp_spawned:
                    Portal(game, col + xOFFSET, row + yOFFSET, 'a', False)
                    game.has_warp_spawned = True

    room_x = xOFFSET
    room_y = yOFFSET

    test_xoffset = 8
    test_yoffset = 8

    total_ennemies = 0
    # En gros on regarde si on est pas dans la pièce se spawn, puis on met entre 1 a 3 slimes
    num_of_ennemies = random.randint(1, 3)
    if game.num_of_rooms != 1:
        for i in range(num_of_ennemies):
            Slime(game, random.randint(TOPLEFT[0] + game.settings["TILESIZE"], BOTTOMRIGHT[0] - 2 * game.settings["TILESIZE"]), random.randint(
                TOPLEFT[1] + game.settings["TILESIZE"], BOTTOMRIGHT[1] - 2 * game.settings["TILESIZE"]), game.player, 2, 1, game.num_of_rooms)
            total_ennemies += 1

    game.floor[game.num_of_rooms] = {
        "number": game.num_of_rooms,
        "coords": (TOPLEFT, BOTTOMRIGHT),
        "Ennemies": total_ennemies
    }

    # La les collisions au milieu des pièces testent pour voir si y a un pièce ou ça veut en faire une autre
    # Si oui, ben pas de pièce, si non ben une pièce

    # Chaque pièce est dans une liste avec des entrées pour la pièce qui en a besoin
    # EX: une pièce avec une ouverture vers le haut va prendre un pièce random dans la liste des pièces avec une ouverture vers le bas et boum

    if "up" in room.type:
        test_cube = Room_DETECT(
            game, room_x + test_xoffset, room_y - test_yoffset, 32, 32)
        hit = pygame.sprite.spritecollide(test_cube, game.RoomMarkers, False)
        if not hit:
            num = random.randint(0, len(game.need_down_opening) - 1)
            create_room(game, room_x, room_y - 15, game.need_down_opening[num])
    if "down" in room.type:
        test_cube = Room_DETECT(
            game, room_x + test_xoffset, room_y + (3*test_yoffset) - 1, 32, 32)
        hit = pygame.sprite.spritecollide(test_cube, game.RoomMarkers, False)
        if not hit:
            num = random.randint(0, len(game.need_up_opening) - 1)
            create_room(game, room_x, room_y + 15, game.need_up_opening[num])
    if "left" in room.type:
        test_cube = Room_DETECT(
            game, room_x - test_xoffset, room_y + test_yoffset, 32, 32)
        hit = pygame.sprite.spritecollide(test_cube, game.RoomMarkers, False)
        if not hit:
            num = random.randint(0, len(game.need_right_opening) - 1)
            create_room(game, room_x - 15, room_y,
                        game.need_right_opening[num])
    if "right" in room.type:
        test_cube = Room_DETECT(
            game, room_x + (3*test_xoffset) - 1, room_y + test_yoffset, 32, 32)
        hit = pygame.sprite.spritecollide(test_cube, game.RoomMarkers, False)
        if not hit:
            num = random.randint(0, len(game.need_left_opening) - 1)
            create_room(game, room_x + 15, room_y, game.need_left_opening[num])


def create_boss_room(game, room):
    # Même chause que au dessus mais pour la salle du boss
    for row, tiles in enumerate(room.data):
        for col, tile in enumerate(tiles):

            if tile == "1":
                Wall(game, col, row, 32, 32)

            if tile == "W":
                if not game.has_warp_spawned:
                    #Portal(game, col, row , 'a', False)
                    #game.has_warp_spawned = True
                    pass

                Boss_slime(game, col, row, slime_0, [
                           (250, 250), (500, 250)], 10, 2)

    game.in_boss_room = True


class Game:
    def __init__(self):
        # Surtout de la déclaration de variable
        with open("Settings.json", "r") as f:
            self.settings = json.load(f)

        with open("Weapons.json", "r") as f:
            self.Weapons = json.load(f)

        with open("character_data.json", "r") as f:
            self.Characters = json.load(f)

        # Création de la fenêtre
        self.screen = pygame.display.set_mode(
            (self.settings["Screen width"], self.settings["Screen height"]))
        pygame.display.set_caption("Dumgeone advemture")
        self.playing = True
        self.clock = pygame.time.Clock()

        self.IN_MENU = False
        self.start_shown = False
        self.FONT = pygame.font.Font(None, 24)
        self.on_doorstep = False

        self.chosen_character = 0
        self.animation_assigned = False
        self.character_selected = False
        self.weapon_equiped = False
        self.in_boss_room = False

        self.floor = []
        self.finished_floors = 0
        self.num_of_rooms = 0
        self.current_room = 0
        self.current_menu = None

        self.boss_warp = False
        self.has_warp_spawned = False

        self.weapon_inventory = []
        self.weapon_inventory_name = []
        self.weapon_inventory_spot = 0

        self.allsprites = pygame.sprite.Group()
        self.UI = pygame.sprite.Group()
        self.Menu_UI = pygame.sprite.Group()
        self.Walls = pygame.sprite.Group()
        self.Doors = pygame.sprite.Group()
        self.RoomMarkers = pygame.sprite.Group()
        self.RoomFinders = pygame.sprite.Group()
        self.Ennemies = pygame.sprite.Group()
        self.Players = pygame.sprite.Group()
        self.Door_holders = pygame.sprite.Group()
        self.Portals = pygame.sprite.Group()
        self.Pickups = pygame.sprite.Group()
        self.Chests = pygame.sprite.Group()
        self.WEAPONS = pygame.sprite.Group()
        self.Bosses = pygame.sprite.Group()

        self.load_maps()

    def load_maps(self):

        # Déclaration de variables
        self.start_map = MAP(self, "ROOM TEMPLATES/Start.txt",
                             ["up", "down", "left", "right"])
        self.top_map = MAP(self, "ROOM TEMPLATES/T.txt", [])
        self.bottom_map = MAP(self, "ROOM TEMPLATES/D.txt", [])
        self.right_map = MAP(self, "ROOM TEMPLATES/R.txt", [])
        self.left_map = MAP(self, "ROOM TEMPLATES/L.txt", [])
        self.top_right_map = MAP(
            self, "ROOM TEMPLATES/TR.txt", ["up", "right"])
        self.top_left_map = MAP(self, "ROOM TEMPLATES/TL.txt", ["up", "left"])
        self.bottom_right_map = MAP(
            self, "ROOM TEMPLATES/DR.txt", ["down", "right"])
        self.bottom_left_map = MAP(
            self, "ROOM TEMPLATES/DL.txt", ["down", "left"])
        self.top_bottom_map = MAP(
            self, "ROOM TEMPLATES/DT.txt", ["down", "up"])
        self.left_right_map = MAP(
            self, "ROOM TEMPLATES/LR.txt", ["left", "right"])
        self.boss_map = MAP(self, "ROOM TEMPLATES/Boss.txt", [])

        self.need_up_opening = [
            self.top_map, self.top_left_map, self.top_right_map, self.top_bottom_map]
        self.need_down_opening = [
            self.bottom_map, self.bottom_left_map, self.bottom_right_map, self.top_bottom_map]
        self.need_left_opening = [
            self.left_map, self.bottom_left_map, self.top_left_map, self.left_right_map]
        self.need_right_opening = [
            self.right_map, self.top_right_map, self.bottom_right_map, self.left_right_map]

        self.new()

    def new(self):

        self.XOFFSET = 0
        self.YOFFSET = 0
        # Si le prochain étage est censé être un boss, ben boss time
        if self.boss_warp:
            create_boss_room(self, self.boss_map)

        # On spawn le joueur
        self.player = Player(self, 5, 5, 32, 32, Red, None)

        if self.chosen_character != 0:
            self.player.chosen_character = self.chosen_character

        # Si c'est pas un boss ben on génère un étage normal
        if not self.boss_warp:
            create_room(self, self.XOFFSET, self.YOFFSET, self.start_map)

        # On enlève les obj de la génération de la map
        for sprites in self.RoomMarkers:
            sprites.kill()
        for sprites in self.RoomFinders:
            sprites.kill()

        #ennemi_test = Slime(self, 8, 8, self.player, 3, 1, self.num_of_rooms)
        # Spawn de la cam
        self.camera = Camera(self, self.start_map.width, self.start_map.height)
        # Spawn de la vie
        for i in range(int(self.settings["Player HP"])):
            if i % 2 != 0:
                Heart_half(self, 990 - (i - 1) * 16, 15, i - 1, right_heart)
            else:
                Heart_half(self, 990 - i * 16, 15, i + 1, left_heart)

        for i in range(int(self.settings["Player HP"] / 2)):
            Heart_container(self, 990 - i * 32, 15, heart_container)

        if not self.boss_warp and not self.start_shown:

            self.start_shown = True
            self.IN_MENU = True
            self.current_menu = "Start"

        # Sah on file un
        if self.finished_floors == 0:
            """
            self.test_weapon1 = Weapon_distance(self, self.player, "Wand")
            self.test_weapon2 = Weapon_distance(self, self.player, "Test_1")
            self.test_weapon3 = Weapon_distance(self, self.player, "Test_2")

            self.weapon_inventory.append(self.test_weapon1)
            self.weapon_inventory.append(self.test_weapon2)
            self.weapon_inventory.append(self.test_weapon3)

            self.weapon_inventory_name.append(self.test_weapon1.name)
            self.weapon_inventory_name.append(self.test_weapon2.name)
            self.weapon_inventory_name.append(self.test_weapon3.name)


            self.weapon_bg = Weapon_UI(self, 925, 700, weapon_holder)
            self.weapon_UI = Weapon_UI(self, 900, 700, pygame.image.load(self.Weapons[self.weapon_inventory[self.weapon_inventory_spot].name]["Icon"]))
            """
        else:
            for weapon in self.weapon_inventory:
                weapon.holder = self.player
            self.assign_animations()

        for weapon in self.weapon_inventory:
            weapon.holder = self.player

        self.run()

    def equip_weapons(self):
        # C'est dans le nom
        if not self.weapon_equiped:
            for wep in self.chosen_character["Base weapons"]:
                weapon = Weapon_distance(self, self.player, wep)
                self.weapon_inventory.append(weapon)
            self.weapon_bg = Weapon_UI(self, 925, 700, weapon_holder)
            self.weapon_UI = Weapon_UI(self, 900, 700, pygame.image.load(
                self.Weapons[self.weapon_inventory[self.weapon_inventory_spot].name]["Icon"]))
            self.player.current_weapon = self.weapon_inventory[self.weapon_inventory_spot]
            print("done")
            self.weapon_equiped = True
        self.assign_animations()

    def assign_animations(self):
        # Selon le perso choisi on dit au prog c'es quoi ces animations
        if not self.animation_assigned:

            for image in self.chosen_character["Sprites"]["Walk right"]:
                img = pygame.image.load(image)
                self.player.walk_right.append(img)
            for image in self.chosen_character["Sprites"]["Walk left"]:
                img = pygame.image.load(image)
                self.player.walk_left.append(img)
            for image in self.chosen_character["Sprites"]["Idle right"]:
                img = pygame.image.load(image)
                self.player.idle_right.append(img)
            for image in self.chosen_character["Sprites"]["Idle left"]:
                img = pygame.image.load(image)
                self.player.idle_left.append(img)

            print("done")
            self.animation_assigned = True
            self.IN_MENU = False

    def run(self):
        # la game loop
        if self.playing:
            self.clock.tick(60)
            if not self.IN_MENU:
                self.update()
            self.draw()
            self.events()

    def events(self):
        for event in pygame.event.get():
            # Pour pouvoir fermer la fenêtre
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.IN_MENU = not self.IN_MENU
                    self.current_menu = "Pause"
                if event.key == pygame.K_r:
                    self.restart_game()
            # Pour faire pew pew
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.IN_MENU:
                    if self.player.current_weapon.ammo > 0:
                        Projectile(
                            self, self.player.current_weapon.shoot_point[0], self.player.current_weapon.shoot_point[1], bullet, 60)
                        self.player.current_weapon.ammo -= 1
                # Scroll up ou down jsp
                if event.button == 4:

                    self.weapon_inventory_spot += 1
                    if self.weapon_inventory_spot > len(self.weapon_inventory) - 1:
                        self.weapon_inventory_spot = 0

                # Scroll up ou down jsp
                if event.button == 5:
                    self.weapon_inventory_spot -= 1
                    if self.weapon_inventory_spot < 0:
                        self.weapon_inventory_spot = len(
                            self.weapon_inventory) - 1

    def update(self):

        # Execute tt les fonctions update des obj
        self.allsprites.update()

        try:
            self.player.current_weapon.update()
        except:
            pass
        self.camera.update(self.player)
        self.UI.update()
        # Pour savoir dans quelle pièce on est
        for room in self.floor:
            if room != None:
                if self.player.x < room["coords"][1][0] and self.player.y < room["coords"][1][1]:
                    if self.player.x > room["coords"][0][0] and self.player.y > room["coords"][0][1]:
                        self.current_room = room["number"]

        if not self.IN_MENU:
            for sprite in self.Menu_UI:
                sprite.kill()

        if self.start_shown and not self.character_selected:
            self.IN_MENU = True

        if self.player.HP <= 0:
            self.start_shown = False
            self.restart_game()

        try:
            self.player.current_weapon = self.weapon_inventory[self.weapon_inventory_spot]
            self.weapon_UI.image = pygame.image.load(
                self.Weapons[self.weapon_inventory[self.weapon_inventory_spot].name]["Icon"])
        except:
            pass

    def draw_menus(self):
        # C'est dans le titre
        self.screen.fill((0, 0, 0))

        if self.current_menu == "Pause":
            self.draw_pause_menu()

        if self.current_menu == "Start":
            self.draw_start_menu()

        if self.current_menu == "Choose":
            self.draw_character_selection_menu()

        self.Menu_UI.update()
        self.Menu_UI.draw(self.screen)
        pygame.display.flip()

    def draw_pause_menu(self):
        # C'est dans le titre
        Pause_Text = self.FONT.render('PAUSE', True, (255, 255, 255))
        self.screen.blit(
            Pause_Text, (int(512 - (self.FONT.size('PAUSE')[0] / 2)), 64))

        quit = Button(self, 900, 720, quit_button, self.quit)

    def draw_start_menu(self):
        # C'est dans le titre
        start = Button(self, 512, 350, start_button, self.start_game)

        quit = Button(self, 512, 500, quit_button, self.quit)

    def draw_character_selection_menu(self):
        # C'est dans le titre
        #RED = Button(self, 350, 350, Red_portrait, self.choose_character, need_argument = True, argument=self.Characters["Red Test"])
        WITCH = Button(self, 350, 350, Witch_portrait, self.choose_character,
                       need_argument=True, argument=self.Characters["Witch"])
        GREEN = Button(self, 650, 350, Green_portrait, self.choose_character,
                       need_argument=True, argument=self.Characters["Green Test"])

    def start_game(self):
        # C'est dans le titre
        self.start_shown = True
        self.IN_MENU = False
        self.current_menu = "Choose"

    def choose_character(self, character):
        # C'est dans le titre
        self.chosen_character = character
        self.player.image = pygame.image.load(character["Sprites"]["base"])
        self.player.chosen_character = character
        self.character_selected = True
        self.equip_weapons()

    def restart_game(self):
        for sprite in self.allsprites:
            if sprite not in self.weapon_inventory:
                sprite.kill()
        for weapon in self.weapon_inventory:
            weapon.ammo = weapon.max_ammo

        if self.finished_floors == 0:
            self.character_selected = False
        self.animation_assigned = False

        self.load_maps()

    def draw_stats(self):
        # C'est dans le titre
        try:

            room = self.FONT.render(
                "Room: " + str(self.current_room), True, (255, 255, 255))
            HP = self.FONT.render(
                "HP: " + str(self.player.HP), True, (222, 255, 255))
            timer = self.FONT.render(
                "Timer: " + str(self.player.hurt_timer), True, (255, 255, 255))
            fps = self.FONT.render(
                "FPS:" + str(self.clock.get_fps()), True, (255, 255, 255))
            total_rooms = self.FONT.render(
                "nb of rooms: " + str(self.num_of_rooms), True, (255, 255, 255))
            ennemies_in_room = self.FONT.render(
                "Ennemies: " + str(self.floor[self.current_room]["Ennemies"]), True, (255, 255, 255))
            total_weapons = self.FONT.render(
                "Total weapons: " + str(len(self.weapon_inventory)), True, (255, 255, 255))
            score = self.FONT.render(
                "Score: " + str(self.finished_floors), True, (255, 255, 255))

            self.screen.blit(room, (15, 15))
            self.screen.blit(HP, (15, 30))
            self.screen.blit(timer, (15, 45))
            self.screen.blit(fps, (15, 60))
            self.screen.blit(total_rooms, (15, 75))
            self.screen.blit(ennemies_in_room, (15, 90))
            self.screen.blit(total_weapons, (15, 105))
            self.screen.blit(score, (15, 120))

        except:
            pass

    def draw(self):
        # En gros draw c'es afficher les trucs a l'écran
        if self.IN_MENU:
            self.draw_menus()
        else:
            self.screen.fill((0, 0, 0))
            for sprite in self.allsprites:
                self.screen.blit(sprite.image, self.camera.apply(sprite))

            self.UI.draw(self.screen)

            ammo = self.FONT.render(str(self.player.current_weapon.ammo) + " / " + str(
                self.player.current_weapon.max_ammo), True, (255, 255, 255))
            self.screen.blit(ammo, (927, 725))

            self.draw_stats()
            pygame.display.flip()

    def quit(self):
        pygame.quit()


game = Game()

while RUNNING:
    game.run()
