import algorithm

class Simple(algorithm.Algorithm):
    """
    A simple packing algorithm. Supports automatic sizing of the sheet

    Places sprites from large to small, one by one.
    Defines a bounding box, the sheet size, if the sprite already fits in the
    already defined bounding box we place it almost anywhere, if the sprite
    doesn't fit in the bounding box we place it in a way that extends the
    bounding box area as little as possible
    """
    supports_rotation = False
    supports_sheet_size_selection = True

    def pack(self, sprites, settings):

        # Dimensions of the occupied rectangle, the bounding box
        sheet_size = (0, 0)

        # Sort the sprite list from the largest to the smallest
        sort_sprites(sprites)

        for s in sprites:
            if fits_in_sheet(s):
                place_sprite_in_free_space(s)

            else:
                place_sprite_extending_sheet(s)

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

        def fits_in_sheet(s):
            """
            Returns if the given sprite fits in the sheet without extending it.
            """
            fits = True

            # Check if the sprite fits in the sheet alone
            if s.size[0] > sheet_size[0] or s.size[1] > sheet_size[1]:
                fits = False

            else:
                placed = get_placed_sprites()

        def get_free_position(s):
            """
            Returns a free position where to put the sprite
            """

        def get_placed_sprites()
            return [s for s in sprites if s.position]

        def sort_sprites():
            """
            Sorts sprites from largest to smallest (by area).
            """
            sprites.sort(key=lambda s: get_area(s.size), reverse=True)

        def get_area(size):
            """
            Returns the area from the given size tuple.
            """
            w, h = size
            return w * h



algorithm.register_algorithm("simple", Simple)
