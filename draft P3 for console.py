#! /usr/bin/env python3
# coding:utf-8

from random import randrange




class MazeBoard:

    """ class defining the structure of maze, based on a list form.
        The MazeBoard object has only two args :
            - maze size : maze is square of size*size. Here, size is constant
            - the structure itself, which is composed of "size" lines of "size" sprites """

    def __init__(self):
        self.size = 15
        self.structure = None

    def get_maze_structure(self, maze_file):

        """ func grabbing the maze structure from a file in local directory """
        
        with open(maze_file, "r") as structure_reader:
            return structure_reader.read().splitlines()


    def show_maze(self, *chars_and_items):

        """ func charged to print the initial gameboard filled with items and characters at their
            correct position """
        
        for num_y, line in enumerate(self.structure):
            line_to_print = line
            for char_or_item in chars_and_items:
                if char_or_item.state == True and char_or_item.position[0] == num_y:
                    line_to_print = line_to_print[:char_or_item.position[1]] + char_or_item.sprite_rep + line_to_print[char_or_item.position[1]+1:]
            print(line_to_print)
            


    def __getitem__(self, index_pos):

        """ special method __getitem__ edited to drive MazeBoard objects' handling handier, by letting
            express the object position in regular 2D indexing notation, directly from the object
            itself : object[y, x] """
        
        if len(index_pos) == 2:
            return self.structure[index_pos[0]][index_pos[1]]
        else:
            return self.structure[index_pos]






class MacGyver:

    """ class dedicated to the MacGyver charactern whom attributes are :
            - position : expressed in a two elements list
            - inventory : expressed in a four keys dictionnary, whose values are bool objects
            - state : alive or dead, True or False, 0 or 1 = a boolean attribute too
            - sprite_rep : the graphic representation on game """


    def __init__(self):
        self.position = [1, 1]
        self.inventory = {"ether_bottle" : False, "needle" : False, "plastic_tube" : False, "syringe" : False}
        self.state = True
        self.sprite_rep = "M"






    def move(self, maze_structure, items_pos_list, enemy, *items):

        """ this func expects a user's move input, before sending it to another function dedicated to
            the management and dealing of this input. After getting back the result, this func
            returns it in a coordinates form, ie a two elements list """
        
        move_submit = False
        while move_submit != True:
            move = input("Use Z/Q/S/D keys to submit a move, then hit \"Enter\" : ")
            if move.lower() in ["z", "q", "s", "d"]:
                move_submit = True
    

                

        verified_move = self.check_move(maze_structure, move, items_pos_list, enemy, *items)
        return list(verified_move)








    def check_move(self, maze_structure, move_to_check, items_pos_list, enemy, *items):

        """ this func is a kind of dealing and and management center of the user's desired move set in
            "move" func. It checks every possible situation the input could possibly put MacGyver on, and either
            deals it itself if the move can or can't be done whithout any specific event, or delegates it to a
            more specific function if needed """
        
        
        if move_to_check.lower() == "z":
            potential_move = [self.position[0] - 1, self.position[1]]
            if maze_structure[potential_move[0], potential_move[1]] == "O":
                return potential_move
            elif potential_move == enemy.position:
                self.get_watchman_off_or_get_killed(enemy)
                return potential_move
            elif potential_move in items_pos_list:
                return self.pick_item(potential_move, items_pos_list, *items)
            elif maze_structure[potential_move[0], potential_move[1]] == "." :
                return potential_move
            else:
                print("Come on Mac...don't you see you can't move over there ?")
                return self.position

        elif move_to_check.lower() == "s":
            potential_move = [self.position[0] + 1, self.position[1]]
            if maze_structure[potential_move[0], potential_move[1]] == "O":
                return potential_move
            elif potential_move == enemy.position:
                self.get_watchman_off_or_get_killed(enemy)
                return potential_move
            elif potential_move in items_pos_list:
                return self.pick_item(potential_move, items_pos_list, *items)
            elif maze_structure[potential_move[0], potential_move[1]] == ".":
                return potential_move
            else:
                print("Come on Mac...don't you see you can't move over there ?")
                return self.position

        elif move_to_check.lower() == "q":
            potential_move = [self.position[0], self.position[1] - 1]
            if maze_structure[potential_move[0], potential_move[1]] == "O":
                return potential_move
            elif potential_move == enemy.position:
                self.get_watchman_off_or_get_killed(enemy)
                return potential_move
            elif potential_move in items_pos_list:
                return self.pick_item(potential_move, items_pos_list, *items)
            elif maze_structure[potential_move[0], potential_move[1]] == ".":
                return potential_move
            else:
                print("Come on Mac...don't you see you can't move over there ?")
                return self.position

        else:
            potential_move = [self.position[0], self.position[1] + 1]
            if maze_structure[potential_move[0], potential_move[1]] == "O":
                return potential_move
            elif potential_move == enemy.position:
                self.get_watchman_off_or_get_killed(enemy)
                return potential_move
            elif potential_move in items_pos_list:
                return self.pick_item(potential_move, items_pos_list, *items)
            elif maze_structure[potential_move[0], potential_move[1]] == ".":
                return potential_move
            else:
                print("Come on Mac...don't you see you can't move over there ?")
                return self.position



    def pick_item(self, move_on_item, items_pos_list, *items):

        """ Not designed to be called in main(), this func manages the situation of MacGyver
            moving on an item spot, and by the way picking it up. As Items class objects
            attributes edition is not available from here, it calls a dedicated instance method
            of this last class to deal with the particular item's state concerned.

            This function also has an automatic processing of Mac's inventory that generates
            the item "syringe" when the three required items, ie  the 3 Items class objects,
            are all picked up """
        
        item_counter = 0
        for item in items:
            if move_on_item == item.position:
                item.disappear()
                print(item.state) # just a test print, will be removed
                self.inventory[item.name] = True
                print(self.inventory[item.name]) #just a test print, will be removed

            if self.inventory[item.name] == True:
                item_counter += 1

        if item_counter == 3:
            self.inventory["syringe"] = True
            for item in items:
                self.inventory[item.name] = False

        
        return move_on_item
            


    def get_watchman_off_or_get_killed(self, enemy):

        """ at any moment of the game, Mac can try to pass through the watchman : this
            func determines the result of the try regarding to Mac's inventory
            As others, this func is not designed to be called in main() """
        
        if self.inventory["syringe"] == True:
            enemy.state = False
        else:
            self.state = False
        

            


class Watchman:

    """ class defining the attributes of the watchman. No methods here, while all has been handled in
        Mac's class, and only three attributes :
            - position, expressed in a two elements list ([y_pos, x_pos])
            - state : True or False, awake or asleep
            - sprite_rep : the graphic reprensentation of the object on game """
    
    def __init__(self):
        self.position = [13, 13]
        self.state = True
        self.sprite_rep = "K"







class Items:
    
    """ class defining the items MacGyver can collect.
        Items' attributes are :
            - name : must be the same that the object's name (is only useful for
                       automatic updates of Mac's inventory)
            - sprite_rep : the symbol chosen to stand for the object on game
            - state : item's state, ie "still on the ground"(1) or "already picked up"(0)
            - position : a 2 elements list, y_position and x_position """

    
    items_pos_list = [] # !!! think about upgrading the random pop function so it could take all class' objects
                        # !!! in args, generate position directly on this class var, and attribute each of
                        # !!! the three random position to an item in the same func
                        # !!! = one single line in main function could solve what is now done now in three 
                        
    
    def __init__(self, name, sprite_rep):
        self.name = name
        self.sprite_rep = sprite_rep
        self.state = True
        self.position = list()

    def random_pop(self, maze_structure, hero, watchman):

        """ func determining an appropriate spot to randomly generate items on ground """
        
        spot_found = False
        while spot_found != True:
            y_pos = randrange(1, maze_structure.size - 1) 
            x_pos = randrange(1, maze_structure.size - 1)
            if maze_structure[y_pos, x_pos] == "." and [y_pos, x_pos] not in Items.items_pos_list and [y_pos, x_pos] not in [hero.position, watchman.position]: 
                Items.items_pos_list.append([y_pos, x_pos])
                spot_found = True
        return [y_pos, x_pos]

            
        
    def disappear(self):

        """ not designed to be called in game, but only by the Mac's class method "pick_item",
            this func handle the state change of items when they are picked up, and removes
            their coordinates from the class var list which contains all coordinates """
        
        self.state = False
        Items.items_pos_list.remove(self.position)







def main():

    # maze board initialization
    maze = MazeBoard()
    maze.structure = maze.get_maze_structure("maze_structure.txt")
    print(maze[maze.size-2, maze.size-1]) # just a test to try the __get__item feature that allows to write maze coordinates in a handy way, with double indexing in one list directly on the class object

    # characters initialization
    hero = MacGyver()
    watchman = Watchman()


    # items initialization 
    ether_bottle = Items("ether_bottle", "b")
    needle = Items("needle", "n")
    plastic_tube = Items("plastic_tube", "p")
    ether_bottle.position = ether_bottle.random_pop(maze, hero, watchman)
    needle.position = needle.random_pop(maze, hero, watchman)
    plastic_tube.position = plastic_tube.random_pop(maze, hero, watchman)



    # tests the classes architecture in game situation
    play = True
    while play:
        print(Items.items_pos_list) # tests Items class' "disappear" func
        print(hero.inventory.items()) # tests hero's inventory updating 
        maze.show_maze(hero, watchman, ether_bottle, needle, plastic_tube)
        hero.position = hero.move(maze, Items.items_pos_list, watchman, ether_bottle, needle, plastic_tube)

        if hero.state != True: ### JUST A QUICK WAY TO CUT THE LOOP => have to improve the game end for the real implementation
            print("Sorry, watchman, who are a bit nervous at the time, shot you in the head".capitalize().center(60))
            play = False
        elif maze[hero.position[0], hero.position[1]] == "O":
            print("Congrats !!! You got out of the maze Mac".capitalize().center(60))
            play = False

    input()

    
            
            

    


if __name__ == "__main__":
    main()
