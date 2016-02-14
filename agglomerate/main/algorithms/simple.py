import algorithm

class Simple(algorithm.Algorithm):
    """
    A simple algorithm
    """
    supports_rotation = False
    supports_sheet_size_selection = False

    def pack(self, sprites, settings):
        for i, s in enumerate(sprites):
            s.position = (i * 10, 0)


algorithm.register_algorithm("simple", Simple)
