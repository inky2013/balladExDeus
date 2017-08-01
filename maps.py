import pyglet
import balladexdeus
from base.scene import Scene
from base.saves.assets import AssetManager
from base.lib.importer import get_attr


class Arrow:
    def __init__(self, image_obj, target, animate, x, y, orientation):
        self.sprite = pyglet.sprite.Sprite(image_obj)
        self.sprite.set_position(x, y)
        self.sprite.rotation = orientation
        self.target, self.animate = target, animate
        self.sprite.color = balladexdeus.Game.instance.config["maps"]["arrow"]["colour"]
        self.sprite.scale = balladexdeus.Game.instance.config["maps"]["arrow"]["scale"]

    def click(self):
        balladexdeus.Game.instance.switch_scene("main", self.target(), self.animate)

    def draw(self):
        self.sprite.draw()


class MapScene(Scene):
    def __init__(self, name, z_index, json):
        super().__init__(name, z_index)
        assert json is not None  # Crash if json not found
        get_img = AssetManager.get_asset
        map_img = pyglet.image.load(get_img(json['map']))
        arrow = pyglet.image.load(get_img("map/arrow.png"))
        self.background_sprite = pyglet.sprite.Sprite(map_img)
        self.arrows = list()

        for item in json["arrows"]:
            if item["type"] == "map":
                target = lambda: MapLoader.get_map(item["target"])
            elif item["type"] == "object":
                target = lambda: get_attr(item["target"])
            else:
                raise RuntimeError("Invalid \"type\" attribute for map")
            self.arrows.append(Arrow(arrow, target, item.get("animation", "fade"), int(item["x"]), int(item["y"]), int(item.get("orientation", 0))))


    @staticmethod
    def is_arrow_in_bounds(x, y, sprite):
        return (sprite.x-((sprite.width*1)/1) < x <= sprite.x+((sprite.width*1)/1)) and (sprite.y-((sprite.height*1)/1) < y <= sprite.y+((sprite.height*1)/1))

    def render(self):
        self.background_sprite.draw()
        for i in self.arrows:
            i.draw()

    def on_mouse_up(self, btn, x, y):
        for arrow in self.arrows:
            if self.is_arrow_in_bounds(x, y, arrow.sprite):
                arrow.click()
                break


    def on_mouse_move(self, x, y):
        for arrow in self.arrows:
            if self.is_arrow_in_bounds(x, y, arrow.sprite):
                arrow.sprite.color = balladexdeus.Game.instance.config["maps"]["arrow"]["hover"]
            else:
                arrow.sprite.color = balladexdeus.Game.instance.config["maps"]["arrow"]["colour"]


class MapLoader:
    maps = dict()
    @staticmethod
    def get_map(name):
        return MapLoader.maps[name]

    @staticmethod
    def load_map(name, obj):
        MapLoader.maps[name] = obj

    @staticmethod
    def prep(name):
        MapLoader.maps[name] = None

