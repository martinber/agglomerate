import agglomerate.main.algorithm
from agglomerate.main.math import Vector2
import copy


class InlineAlgorithm(agglomerate.main.algorithm.Algorithm):
    """
    Simple packing algorithm that places sprites in a horizontal row

    Places sprites in the given order (from sprites list), one by one, from
    left to right.
    """
    supports = {
                "rotation": False,
                "cropping": False,
                "padding": False,

                "auto_size": True,
                "auto_square_size": False,
                "auto_power_of_two_size": False,
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
            # make a copy otherwise all positions end pointing to the same
            # object
            s.position = copy.copy(next_sprite_position)
            # set the next sprite position
            next_sprite_position.x += s.size.x
            # check if this one is the highest sprite
            if s.size.y > highest_height:
                highest_height = s.size.y

        if settings.size.x == "auto":
            settings.size.x = next_sprite_position.x
        elif next_sprite_position.x > settings.size.x:
            raise agglomerate.main.algorithm.AlgorithmOutOfSpaceException(
                    "Given width it's too small")

        if settings.size.y == "auto":
            settings.size.y= highest_height
        elif highest_height > settings.size.y:
            raise agglomerate.main.algorithm.AlgorithmOutOfSpaceException(
                    "Given height it's too low")


algorithm_class = InlineAlgorithm
