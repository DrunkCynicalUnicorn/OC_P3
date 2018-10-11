from constants import *
import pygame
from pygame.locals import *
from random import randrange


class Maze:

    def __init__(self):
        self.size = NUM_SPRITE
        self.structure = self.get_maze_structure(maze_structure)

        self.wall_sprite = pygame.image.load(wall_sprite).convert_alpha()
        self.floor_sprite = pygame.image.load(floor_sprite).convert_alpha()
        self.start_sprite = pygame.image.load(start_sprite).convert_alpha()
        self.exit_sprite = pygame.image.load(exit_sprite).convert_alpha()

        self.death_position = None
        self.death_sprite = pygame.image.load(blood_sprite).convert_alpha()

        self.border_sprite = \
            pygame.image.load(bottom_frame_sprite).convert_alpha()
        self.tube_icon = pygame.image.load(tube_icon).convert_alpha()
        self.needle_icon = pygame.image.load(needle_icon).convert_alpha()
        self.ether_icon = pygame.image.load(ether_icon)
        self.syringe_icon = pygame.image.load(syringe_icon).convert_alpha()

    def __getitem__(self, index_pos):

        """ special method __getitem__ edited to drive MazeBoard objects'
        handling handier, by letting express the object position in
        regular 2D indexing notation, directly from the object itself :
        object[y, x] becomes equivalent to object.structure[x][y] """

        if len(index_pos) == 2:
            return self.structure[index_pos[0]][index_pos[1]]
        else:
            return self.structure[index_pos]

    def get_maze_structure(self, maze_file):

        """ func grabbing the maze structure from a file in local directory """

        with open(maze_file, "r") as structure_reader:
            return structure_reader.read().splitlines()

    def display_maze(self, window, *chars_and_items):
        for y, line in enumerate(self.structure):
            for x, char in enumerate(line):
                if char == "w":
                    window.blit(self.wall_sprite, (pix_coor_converter(x),
                                                   pix_coor_converter(y)))
                elif char == "." or char == "O":
                    window.blit(self.floor_sprite, (pix_coor_converter(x),
                                                    pix_coor_converter(y)))
                    if char == "O":
                        window.blit(self.exit_sprite, (pix_coor_converter(x),
                                                       pix_coor_converter(y)))
                else:
                    window.blit(self.start_sprite, (pix_coor_converter(x),
                                                    pix_coor_converter(y)))

        for char_or_item in chars_and_items:
            if char_or_item.state:
                window.blit(char_or_item.sprite,
                            ((pix_coor_converter(char_or_item.position[1]),
                              pix_coor_converter(char_or_item.position[0]))))

        if self.death_position is not None:
                window.blit(self.death_sprite,
                            (pix_coor_converter(self.death_position[1]),
                             pix_coor_converter(self.death_position[0])))

    def display_border(self, window, hero, *items, activate=True):
        for i in range(0, WINDOW_WIDTH, SPRITE_SIZE):
            window.blit(self.border_sprite, (i, WINDOW_HEIGHT - SPRITE_SIZE))

        if activate:
            for item in items:
                if not item.state:
                    if item.name == "needle":
                        window.blit(self.needle_icon, (0,
                                                       NUM_SPRITE *
                                                       SPRITE_SIZE))
                    elif item.name == "plastic_tube":
                        window.blit(self.tube_icon, (SPRITE_SIZE,
                                                     NUM_SPRITE *
                                                     SPRITE_SIZE))
                    else:
                        window.blit(self.ether_icon, (SPRITE_SIZE*2,
                                                      NUM_SPRITE *
                                                      SPRITE_SIZE))

            if hero.inventory["syringe"]:
                window.blit(self.syringe_icon, (SPRITE_SIZE*7,
                                                NUM_SPRITE * SPRITE_SIZE))


class Character:

    def __init__(self):
        self.position = [NUM_SPRITE - 2, NUM_SPRITE - 2]
        self.sprite = pygame.image.load(guardian_sprite).convert_alpha()
        self.state = True


class MacGyver:

    def __init__(self):
        self.position = [1, 1]
        self.sprite = pygame.image.load(mac_sprite).convert_alpha()
        self.state = True
        self.inventory = {"ether_bottle": False, "needle": False,
                          "plastic_tube": False, "syringe": False}

    def move(self, direction, maze_structure, items_position_list,
             enemy, *items):
        if direction == "right":
            desired_move = [self.position[0], self.position[1] + 1]
        elif direction == "left":
            desired_move = [self.position[0], self.position[1] - 1]
        elif direction == "up":
            desired_move = [self.position[0] - 1, self.position[1]]
        else:
            desired_move = [self.position[0] + 1, self.position[1]]

        if maze_structure[desired_move[0], desired_move[1]] in ["O", "S", "."]:
            if desired_move in items_position_list:
                self.pick_item(desired_move, items_position_list, *items)
            elif desired_move == enemy.position:
                self.get_guardian_off_or_get_killed(enemy, maze_structure)
            return desired_move
        else:
            return self.position

    def pick_item(self, move_on_item, items_position_list, *items):

        """ Not designed to be called in main(), this func manages the situation
        of MacGyver moving on an item spot, and by the way picking it up.
        As Items class objects attributes edition is not available from here,
        it calls a dedicated instance method of this last class to deal with
        the particular item's state concerned.

        This function also has an automatic processing of Mac's inventory
        that generates the item "syringe" when the three required items,
        ie  the 3 Items class objects are all picked up """

        item_counter = 0
        for item in items:
            if move_on_item == item.position:
                item.actualize_picked_item()
                self.inventory[item.name] = True
            if self.inventory[item.name]:
                item_counter += 1

        if item_counter == 3:
            self.inventory["syringe"] = True
            for item in items:
                self.inventory[item.name] = False

    def get_guardian_off_or_get_killed(self, enemy, maze_structure):

        """ at any moment of the game, Mac can try to pass through the watchman : this
            func determines the result of the try regarding to Mac's inventory
            As others, this func is not designed to be called in main() """

        if self.inventory["syringe"]:
            enemy.state = False
        else:
            self.state = False
            maze_structure.death_position = self.position


class Items:

    items_position_list = list()

    def __init__(self, name, sprite_name):
        self.name = name
        self.sprite = pygame.image.load(sprite_name).convert_alpha()
        self.state = True
        self.position = None

    def random_pop(self, maze_structure, hero, guardian):

        """ func determining an appropriate spot to randomly generate
        items on ground """

        spot_found = False
        while not spot_found:
            y_pos = randrange(1, maze_structure.size - 1)
            x_pos = randrange(1, maze_structure.size - 1)
            if maze_structure[y_pos, x_pos] == "." \
                    and [y_pos, x_pos] not in \
                    Items.items_position_list \
                    and [y_pos, x_pos] not in \
                    [hero.position, guardian.position]:
                Items.items_position_list.append([y_pos, x_pos])
                spot_found = True
        return [y_pos, x_pos]

    def actualize_picked_item(self):

        """ not designed to be called in game, but only by the Mac's
        class method "pick_item", this func handle the state change
        of items when they are picked up, and removes their coordinates
        from the class var list which contains all coordinates """

        self.state = False
        Items.items_position_list.remove(self.position)
