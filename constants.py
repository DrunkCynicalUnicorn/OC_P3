SPRITE_SIZE = 40
NUM_SPRITE = 15

WINDOW_WIDTH = SPRITE_SIZE * NUM_SPRITE
WINDOW_HEIGHT = WINDOW_WIDTH + SPRITE_SIZE

maze_structure = "maze_structure.txt"

mac_sprite = "resources/player.png"
guardian_sprite = "resources/guardian.png"
blood_sprite = "resources/blood.png"

wall_sprite = "resources/wall.png"
floor_sprite = "resources/floor.png"
start_sprite = "resources/start.png"
exit_sprite = "resources/exit_stairs.png"
bottom_frame_sprite = "resources/bottom_frame_sprite.png"

tube_sprite = "resources/tube.png"
needle_sprite = "resources/needle.png"
ether_sprite = "resources/ether.png"

tube_icon = "resources/tube_icon.png"
needle_icon = "resources/needle_icon.jpg"
ether_icon = "resources/ether_icon.png"
syringe_icon = "resources/syringe_icon.png"

victory = "resources/victory_picture.jpeg"


def pix_coor_converter(coor):

    """ this function is a converter from indexes to
    pixels coordinates, based on the size of a sprite
    """

    return coor * SPRITE_SIZE
