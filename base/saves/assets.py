from os.path import join as path_join


class AssetManager:
    BASE = "ext"
    SAVES = path_join(BASE, "saves")
    ASSETS = path_join(BASE, "assets")
    MAPS = "maps"

    @staticmethod
    def get_asset(*args):
        return path_join(AssetManager.ASSETS, *args)

    @staticmethod
    def get_saves(*args):
        return path_join(AssetManager.SAVES, *args)

    @staticmethod
    def get_map(*args):
        return path_join(AssetManager.MAPS, *args)