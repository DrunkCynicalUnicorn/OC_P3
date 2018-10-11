SPRITE_SIZE = 40
NUM_SPRITE = 15

WINDOW_WIDTH = SPRITE_SIZE * NUM_SPRITE
WINDOW_HEIGHT = WINDOW_WIDTH + SPRITE_SIZE

maze_structure = "maze_structure.txt"

mac_sprite = "player.png"
guardian_sprite = "guardian.png"
blood_sprite = "blood.png"

wall_sprite = "wall.png"
floor_sprite = "floor.png"
start_sprite = "start.png"
exit_sprite = "exit_stairs.png"
bottom_frame_sprite = "bottom_frame_sprite.png"

tube_sprite = "tube.png"
needle_sprite = "needle.png"
ether_sprite = "ether.png"

tube_icon = "tube_icon.png"
needle_icon = "needle_icon.jpg"
ether_icon = "ether_icon.png"
syringe_icon = "syringe_icon.png"

victory = "victory_picture.jpeg"


def pix_coor_converter(coor):
    return coor * SPRITE_SIZE
