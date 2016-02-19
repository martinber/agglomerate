import algorithm
from main.classes import Vector2

class BinaryTreeAlgorithm(algorithm.Algorithm):
    """
    Simple packing based on the binary tree algorithm

    Places sprites from large to small, one by one.
    http://codeincomplete.com/posts/2011/5/7/bin_packing/
    """
    supports_rotation = False
    supports_sheet_size_selection = True

    def pack(self, sprites, settings):

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

        def place_sprite_in_free_space(sprite, root_node):
            """
            Tries to place the sprite in a free node
            """
            free_node = root_node.find_space(sprite.size)
            if free_node:
                # Place the sprite
                sprite.position = free_node.position
                # Mark the node as used and split the free space in two more
                # nodes
                free_node.split(sprite.size)
                print("Placed in")
                print(sprite.position)
                return True
            else:
                return False

        def place_sprite_extending_sheet(sprite, root_node):
            """
            Extends the sheet trying to make the sheet squared, places the
            sprite and returns the new root_node
            """
            # Size defined by the user
            given_sheet_size = settings.output_sheet_size

            sprite_fits_extending_below = (sprite.size.x <= root_node.size.x)
            sprite_fits_extending_right = (sprite.size.y <= root_node.size.y)

            can_extend_below = (given_sheet_size.x == "auto" and
                                sprite_fits_extending_below)

            can_extend_right = (given_sheet_size.y == "auto" and
                                sprite_fits_extending_right)

            should_extend_below = (can_extend_below and
                    root_node.size.x >= root_node.size.y + sprite.size.y)
            should_extend_right = (can_extend_right and
                    root_node.size.y >= root_node.size.x + sprite.size.x)

            print(should_extend_below)
            print(should_extend_right)

            if should_extend_below:
                new_root = extend_below(root_node, sprite.size.y)
                # Place the sprite
                sprite.position = new_root.down.position
                # Mark the node as used and split the free space in two more
                # nodes
                new_root.down.split(sprite.size)
                print("Extending below")
                return new_root

            elif should_extend_right:
                new_root = extend_right(root_node, sprite.size.x)
                # Place the sprite
                sprite.position = new_root.right.position
                # Mark the node as used and split the free space in two more
                # nodes
                new_root.right.split(sprite.size)
                print("Extending right")
                return new_root

            elif can_extend_below:
                new_root = extend_below(root_node, sprite.size.y)
                # Place the sprite
                sprite.position = new_root.down.position
                # Mark the node as used and split the free space in two more
                # nodes
                new_root.down.split(sprite.size)
                print("Extending below")
                return new_root

            elif can_extend_right:
                new_root = extend_right(root_node, sprite.size.x)
                # Place the sprite
                sprite.position = new_root.right.position
                # Mark the node as used and split the free space in two more
                # nodes
                new_root.right.split(sprite.size)
                print("Extending right")
                return new_root

        def extend_below(root_node, amount):
            """
            Extends the root node by an amount, actually creates a new
            root_node with the old root_node as a child. And returns the new
            root_node
            """
            new_root = Node((0, 0),
                            (root_node.size.x, root_node.size.y + amount))
            new_root.used = True

            new_root.right = root_node
            new_root.down = Node((0, root_node.size.y),
                                  (root_node.size.x, amount))

            return new_root

        def extend_right(root_node, amount):
            """
            Extends the root node by an amount. Actually creates a new
            root_node with the old root_node as a child, and returns the new
            root_node
            """
            new_root = Node((0, 0),
                            (root_node.size.x + amount, root_node.size.y))
            new_root.used = True

            new_root.down = root_node
            new_root.right = Node((root_node.size.x, 0),
                                  (amount, root_node.size.y))

            return new_root

        def sort_sprites(sprites):
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

        def fits(size1, size2):
            """
            Checks if size1 fits inside size2
            """
            return size1.x <= size2.x and size1.y <= size2.y

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
                Creates a node, specifying position and size tuples (later
                they are converted to classes.Vector2
                """
                # Means that already contains a sprite but also means that
                # contains child nodes
                self.used = False
                # Right node
                self.right = None
                # Left node
                self.down = None
                # Rectangle data
                x, y = position
                w, h = size
                self.position = Vector2(x, y)
                self.size = Vector2(w, h)

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

                self_x = self.position.x
                self_y = self.position.y
                self_w = self.size.x
                self_h = self.size.y
                used_w = used_space.x
                used_h = used_space.y

                self.right = Node((self_x + used_w, self_y),
                                  (self_w - used_w, used_h))

                self.down = Node((self_x, self_y + used_h),
                                 (self_w, self_h - used_h))

        # Sort the sprite list from the largest to the smallest
        sort_sprites(sprites)

        # Create root node in (0, 0) with the size of the first sprite
        root_node = Node((0, 0), sprites[0].size)

        for s in sprites:
            print("Choosing a new sprite")
            # Try to place it in free space, else extend the sheet
            if not place_sprite_in_free_space(s, root_node):
                print("Cant fit sprite, extending sheet")
                root_node = place_sprite_extending_sheet(s, root_node)

        # Update settings
        settings.output_sheet_size = root_node.size

algorithm.register_algorithm("binarytree", BinaryTreeAlgorithm)
