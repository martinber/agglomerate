from agglomerate.main.algorithms import algorithm
from agglomerate.main.misc.vector2 import Vector2
import copy


class InlineAlgorithm(algorithm.Algorithm):
    """
    Simple packing algorithm that places sprites in a horizontal row

    Places sprites in the given order (from sprites list), one by one, from
    left to right.
    """
    supports = {
                "rotation": False,
                "cropping": False,
                "padding": False,

                "auto_sheet_size": True,
                "auto_square_sheet_size": False,
                "auto_power_of_two_sheet_size": False,
               }

    def pack(self, sprites, settings):
        # determines where to place the next sprite top-left corner, the X
        # value is the previous X value plus the width of the placed sprite
        # the Y value is always zero
        next_sprite_position = Vector2(0, 0)

        # largest sprite height, so at the end if the sheet height is "auto",
        # we set the sheet height to this value
        highest_height = 0

        for s in sprites:
            # place sprite, I want to assign s.position the VALUE of
            # next_sprite_position, I dont want both to be the same object
            # I need to make a copy? sounds simple but can't think of a better
            # way to assign the next_sprite_position's VALUE
            s.position = copy.copy(next_sprite_position)
            # set the next sprite position
            next_sprite_position.x += s.size.x
            # check if this one is the highest sprite
            if s.size.y > highest_height:
                highest_height = s.size.y

        if settings.sheet_size.x == "auto":
            settings.sheet_size.x = next_sprite_position.x
        elif next_sprite_position.x > settings.sheet_size.x:
            raise algorithm.AlgorithmOutOfSpaceException(
                    "Given width it's too small")

        if settings.sheet_size.y == "auto":
            settings.sheet_size.y= highest_height
        elif highest_height > settings.sheet_size.y:
            raise algorithm.AlgorithmOutOfSpaceException(
                    "Given height it's too low")

algorithm.register_algorithm("inline", InlineAlgorithm)
