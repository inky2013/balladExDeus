DEFAULT_GAME_CONFIG = {
    "window": {
        "width": 1024,
        "height": 768
    },
    "handlers": {
        #"save-handler": "base.saves.gamedata.CompressedDataLoader"
        "save-handler": "base.saves.gamedata.JSONLoader"
    },
    "fps": 60,
    "max_fps": 60,
    "maps": {
        "arrow": {
            "colour": [204, 204, 0],
            "hover": [70,130,180]
        }
    }
}