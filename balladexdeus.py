import pyglet
import base
import defaults
from pyglet.window import mouse
import maps
from time import sleep
import glob

class Game:
    instance = None

    def __init__(self):
        Game.instance = self
        self.config = base.saves.gamedata.JSONLoader().load_and_fill_missing(base.saves.assets.AssetManager.get_saves("config.json"), defaults.DEFAULT_GAME_CONFIG)
        self.window = pyglet.window.Window(width=self.config["window"]["width"], height=self.config["window"]["height"])
        self.party = list()
        self.save_handler = base.lib.importer.get_attr(self.config["handlers"]["save-handler"])
        self.scene_stack = base.scene.SceneManager("_stack", 0)
        self.states = dict()
        self._mouse_pos = (0, 0)


    def switch_scene(self, layer, target, animation_name):
        if animation_name == "fade":
            self.scene_stack[layer].unload()
            self.scene_stack["_animation_layer"].get("black_overlay").sprite.alpha = 1
            self.scene_stack[layer].full_unload()
            self.scene_stack[layer] = target
            self.scene_stack[layer].activate()
            sleep(1)
            self.scene_stack["_animation_layer"].get("black_overlay").sprite.alpha = 0
            self.scene_stack[layer].full_activate()



    def clear_scene(self, target=None):
        if target is None:
            self.scene_stack = list()
            return
        for i in self.scene_stack:
            if i.type == target:
                self.scene_stack.remove(i)

    def start(self):

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            self.scene_stack.on_mouse_down(button, x, y)

        @self.window.event
        def on_mouse_release(x, y, button, modifiers):
            self.scene_stack.on_mouse_up(button, x, y)

        @self.window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            button = None
            if buttons & mouse.LEFT:
                button = mouse.LEFT
            elif buttons & mouse.RIGHT:
                button = mouse.RIGHT
            elif buttons & mouse.MIDDLE:
                button = mouse.MIDDLE
            self.scene_stack.on_mouse_drag(button, (x, y), (dx, dy))

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            self.scene_stack.on_mouse_move(dx, dy)
            self._mouse_pos = (dx, dy)

        @self.window.event
        def on_key_press(symbol, modifiers):
            self.scene_stack.on_keyboard_down(symbol, modifiers)

        @self.window.event
        def on_key_release(symbol, modifiers):
            self.scene_stack.on_keyboard_up(symbol, modifiers)

        @self.window.event
        def draw():
            self.window.clear()
            render(None)

        def update(i):
            self.scene_stack.update()

        def render(i):
            self.scene_stack.render()

        pyglet.clock.schedule_interval(update, 1.0 / float(self.config["fps"]))
        pyglet.clock.schedule_interval(render, 1.0 / float(self.config["fps"]))
        pyglet.clock.set_fps_limit(int(self.config["max_fps"]))

        pyglet.app.run()

class BlackOverlayLayer(base.scene.Scene):
    def __init__(self):
        super().__init__("BlackOverlayLayer", 1)
        self.draw = lambda x: pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                                               ('v2f', [0, 0, 0, Game.instance.config["window"]["height"],
                                                        Game.instance.config["window"]["width"],
                                                        Game.instance.config["window"]["height"],
                                                        Game.instance.config["window"]["width"], 0]))


game = Game()


if __name__ == "__main__":

    for filename in glob.iglob('maps/**/*.json', recursive=True):
        name = "/".join(filename.replace("\\", "/").replace(".json", "").split("/")[1:])
        maps.MapLoader.load_map(name, maps.MapScene(name=name, z_index=0, json=base.saves.gamedata.JSONLoader().load(base.saves.assets.AssetManager.get_map(name+".json"), None)))

    Game.instance.scene_stack.add(
        base.scene.SceneManager("main", 1)
    )
    Game.instance.scene_stack.add(
        base.scene.SceneManager("overlay", 2)
    )
    Game.instance.scene_stack.add(
        base.scene.SceneManager("overlay_layer_2", 3)
    )
    Game.instance.scene_stack.add(
        base.scene.SceneManager("gui", 4)
    )
    Game.instance.scene_stack.add(
        base.scene.SceneManager("_animation_layer", 5)
    )

    Game.instance.scene_stack["main"].add(
        maps.MapLoader.get_map("ateltown/ateltown1")
    )
    Game.instance.start()
