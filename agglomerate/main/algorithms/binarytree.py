import algorithm

class BinaryTreeAlgorithm(algorithm.Algorithm):
    """
    Simple packing based on the binary tree algorithm

    Places sprites from large to small, one by one.
    http://codeincomplete.com/posts/2011/5/7/bin_packing/
    """
    supports_rotation = False
    supports_sheet_size_selection = True

    def pack(self, sprites, settings):
        # Sort the sprite list from the largest to the smallest
        sort_sprites(sprites)

        # Create root node in (0, 0) with the size of the first sprite
        root_node = Node((0, 0), sprites[0].size)

        for s in sprites:
            # Try to place it in free space, else extend the sheet
            if place_sprite_in_free_space(s):
                pass
            else:
                place_sprite_extending_sheet(s)

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

        def place_sprite_in_free_space(s)
            """
            Tries to place the sprite in a free node
            """
            free_node = root_node.find_space(s.size)
            if free_node:
                # Place the sprite
                s.position = free_node.position
                # Mark the node as used and split the free space in two more
                # nodes
                free_node.split()
                return True
            else:
                return False

        def sort_sprites():
            """
            Sorts sprites from largest to smallest (by longest side).
            """
            sprites.sort(key=lambda s: max(s.size), reverse=True)

        def get_area(size):
            """
            Returns the area from the given size tuple.
            """
            w, h = size
            return w * h

        def fits(size1, size2)
            """
            Checks if size1 fits inside size2
            """
            return size1[0] <= size2[0] and size1[1] <= size2[1]

# -----------------------------------------------------------------------------
# Binary tree implementation
# -----------------------------------------------------------------------------

        class Node:
            """
            Node of a binary tree, it's also a rectangle so also has
            dimensions.
            """
            def __init__(self, position, size):
                """
                Creates a node, specifying position and size tuples
                """
                # Means that already contains a sprite but also means that
                # contains child nodes
                self.used = False
                # Right node
                self.right = None
                # Left node
                self.down = None
                # Rectangle data
                self.position = position
                self.size = size

            def find_space(self, s):
                """
                Recurses child nodes until it finds a free node larger than the
                given size

                Returns the node or False
                """
                result = False

                # Check if this node already has a sprite
                if self.used:
                    # Check recursively if the right node is free
                    result = self.right.find_space(s)
                    if not result:
                        # Else check recursively the down node
                        result = self.down.find_space(s)

                    return result

                # If this node is free check if the given size fits here
                elif fits(s, self.size):
                    return self

                else:
                    return False

            def split(self, used_space):
                """
                Mark the node as used and split the remaining space in two
                nodes

                The used space is a size tuple, represents a rectangle placed
                on the minimal x and minimal y position
                """
                self.used = True

                self_x = self.position[0]
                self_y = self.position[1]
                self_w = self.size[0]
                self_h = self.size[1]
                used_w = used_space[0]
                used_h = used_space[1]

                self.right = Node((self_x + used_w, self_y),
                                  (self_w - used_w, used_h))

                self.down = Node((self_x, self_y + used_h),
                                 (self_w, self_h - used_h))
