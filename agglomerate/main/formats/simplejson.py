from agglomerate.main.formats import format
import json
from agglomerate.main.misc.vector2 import Vector2


class SimpleJSON(format.Format):
    """
    A simple JSON output
    """
    #supports_rotation = False
    supports = {
                "rotation": True,
                "cropping": False,
               }

    def generate(self, sprites, settings):
        # list (array) of sprites that will be converted to json
        sprite_array = []

        for s in sprites:
            # dict (object) that represents a sprite
            sprite_object = {
                "name": s.name,
                "x": s.position.x,
                "y": s.position.y,
                "w": s.size.x,
                "h": s.size.y,
                "rotated": s.rotated
            }
            sprite_array.append(sprite_object)

        # Dump the array into a json string, indented by 4 spaces
        return json.dumps(sprite_array, indent=4)


format.register_format("simplejson", SimpleJSON)
