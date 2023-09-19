class Colors:
    # [empty, i, j, l, o, s, t, z]
    black = (20, 30, 40)
    cyan = (1, 237, 250)
    blue = (0, 119, 211)
    orange = (255, 145, 12)
    yellow = (254, 251, 52)
    green = (83, 213, 63)
    purple = (120, 37, 111)
    red = (253, 63, 89)
    transparent_cyan = (1, 237, 250, 50)
    transparent_blue = (0, 119, 211, 50)
    transparent_orange = (255, 145, 12, 50)
    transparent_yellow = (254, 251, 52, 50)
    transparent_green = (83, 213, 63, 50)
    transparent_purple = (120, 37, 111, 50)
    transparent_red = (253, 63, 89, 50)
    transparent_color = (211, 211, 211)
    white = (255, 255, 255, 50)
    dark_blue = (64, 64, 64)
    light_blue = (59, 85, 162)

    # Called on class instead of instance of itself
    @classmethod
    def get_colors(colors):
        return [colors.black, colors.cyan, colors.blue, colors.orange, colors.yellow, colors.green, colors.purple, colors.red,
                    colors.transparent_color]