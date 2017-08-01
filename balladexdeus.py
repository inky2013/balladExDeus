import pyglet
import base
import defaults
from pyglet.window import mouse
from time import sleep
import tilemaps

class Game:
    instance = None

    def __init__(self):
        Game.instance = self
        print("RUN")
        self.config = base.saves.gamedata.JSONLoader().load_and_fill_missing(base.saves.assets.AssetManager.get_saves("config.json"), defaults.DEFAULT_GAME_CONFIG)
        self.window = pyglet.window.Window(width=self.config["window"]["width"], height=self.config["window"]["height"])
        self.party = list()
        self.save_handler = base.lib.importer.get_attr(self.config["handlers"]["save-handler"])
        self.scene_stack = base.scene.SceneManager("_stack", 0)
        self.states = dict()
        self._mouse_pos = (0, 0)

    def switch_scene(self, layer, target, animation_name):
        if isinstance(layer, str):
            layer = [layer]

        stack = self.scene_stack

        for l in layer:
            stack = stack.get(l)

        stack.unload()
        self.scene_stack.get("_animation_layer").get("BlackOverlayLayer").alpha = 255
        stack.full_unload()
        stack.scenes = list()
        stack.add(target)



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
            self.scene_stack.on_mouse_move(x, y)
            self._mouse_pos = (x, y)

        @self.window.event
        def on_key_press(symbol, modifiers):
            self.scene_stack.on_keyboard_down(symbol, modifiers)

        @self.window.event
        def on_key_release(symbol, modifiers):
            self.scene_stack.on_keyboard_up(symbol, modifiers)

        @self.window.event
        def draw():
            pass
            render(None)

        def update(i):
            self.scene_stack.update()

        def render(i):
            self.window.clear()
            self.scene_stack.render()
            return
            cumulative = -33
            y = 0
            for i in range(len(tilemaps._SEQ)):
                cumulative += 33
                if cumulative+33 > self.window.width:
                    cumulative = 0
                    y += 33
                label = pyglet.text.Label(text=str(i))
                label.x, label.y, label.color = cumulative, y, (255, 0, 255, 255)
                tilemaps._SEQ[i].blit(cumulative, y)
                label.draw()

        pyglet.clock.schedule_interval(update, 1.0 / float(self.config["fps"]))
        pyglet.clock.schedule_interval(render, 1.0 / float(self.config["fps"]))
        pyglet.clock.set_fps_limit(int(self.config["max_fps"]))

        pyglet.app.run()

class BlackOverlayLayer(base.scene.Scene):
    def __init__(self):
        super().__init__("BlackOverlayLayer", 1)
        self.alpha = 0

    def draw(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2f', [0, 0, 0, Game.instance.config["window"]["height"],
                                      Game.instance.config["window"]["width"],
                                      Game.instance.config["window"]["height"],
                                      Game.instance.config["window"]["width"], 0]),
                             ('c4B',
                              (0, 0, 0, self.alpha, 0, 0, 0, self.alpha, 0, 0, 0, self.alpha, 0, 0, 0, self.alpha)))
