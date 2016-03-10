import agglomerate.main.items


class Parameters(agglomerate.main.items.Group):
    """
    Contains everything that the packer needs to work, i.e. the sprites
    organized in groups, and the settings for the sheet.

    Has a items list and the sheet settings. This is like a group class but
    with an extended settings (SheetSettings instead Settings) and a different
    name. Also the type attribute is "parameters", "group" or None

    Example tree::

        parameters
        ├─ items (list)
        |  ├─ group1
        |  |  ├─ items (list)
        |  |  └─ settings
        |  ├─ group2
        |  |  ├─ items (list)
        |  |  └─ settings
        |  ├─ sprite1
        |  ├─ sprite2
        |  └─ ...
        |
        └─ settings
    """
    def __init__(self, items, settings):
        super().__init__(items, settings)

        self.position = agglomerate.main.math.Vector2(0, 0)
        self.size = settings.size
        self.rotated = False

        self.type = "parameters"
