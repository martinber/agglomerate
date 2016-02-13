import format

class SimpleJSON(format.Format):
    """
    A simple JSON output
    """
    supports_rotation = False

    def generate(self, sprites, settings):
        return "Prueba"

format.register_format("simplejson", SimpleJSON)
