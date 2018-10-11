from classes import *
from constants import *
import pygame
import sys


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

victory_picture = pygame.image.load(victory).convert()

pygame.key.set_repeat(200, 200)


def main():

    maze = Maze()

    hero = MacGyver()
    guardian = Character()

    needle = Items("needle", needle_sprite)
    plastic_tube = Items("plastic_tube", tube_sprite)
    ether_bottle = Items("ether_bottle", ether_sprite)
    needle.position = needle.random_pop(maze, hero, guardian)
    plastic_tube.position = plastic_tube.random_pop(maze, hero, guardian)
    ether_bottle.position = ether_bottle.random_pop(maze, hero, guardian)

    maze.display_maze(window, guardian, hero, needle, plastic_tube,
                      ether_bottle)
    pygame.display.flip()

    game = True
    while game:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    hero.position = hero.move("left", maze,
                                              Items.items_position_list, guardian,
                                              needle, plastic_tube, ether_bottle)
                if event.key == K_RIGHT:
                    hero.position = hero.move("right", maze,
                                              Items.items_position_list, guardian,
                                              needle, plastic_tube, ether_bottle)
                if event.key == K_UP:
                    hero.position = hero.move("up", maze, Items.items_position_list, guardian, needle, plastic_tube, ether_bottle)
                if event.key == K_DOWN:
                    hero.position = hero.move("down", maze, Items.items_position_list, guardian, needle, plastic_tube, ether_bottle)

            if event.type == QUIT:
                sys.exit()
        maze.display_maze(window, guardian, hero, needle, plastic_tube, ether_bottle)
        maze.display_border(window, hero, needle, plastic_tube, ether_bottle)
        pygame.display.flip()

        if maze[hero.position[0], hero.position[1]] == "O" or not hero.state:
            game = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_q:
                sys.exit()
            if event.type == KEYDOWN:
                main()

        if hero.state:
            window.blit(victory_picture, (0, 0))
            maze.display_border(window, hero, activate=False)
            pygame.display.flip()
        else:
            maze.display_maze(window, guardian, hero,
                              needle, plastic_tube, ether_bottle)
            pygame.display.flip()


main()
