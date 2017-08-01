import pyglet
from base.saves.assets import AssetManager


class Scene:
    def __init__(self, name, z_index):
        self.z_index = z_index
        self.name = name

    def render(self):
        pass

    def update(self):
        pass

    def full_activate(self):
        pass

    def activate(self):
        pass

    def on_mouse_down(self, btn, x, y):
        pass

    def on_mouse_up(self, btn, x, y):
        pass

    def on_mouse_drag(self, btn, it, pt):
        pass

    def on_mouse_move(self, x, y):
        pass

    def on_mouse_hold(self, btn):
        pass

    def on_keyboard_down(self, key, modifiers):
        pass

    def on_keyboard_up(self, key, modifiers):
        pass

    def on_keyboard_hold(self, key, modifiers):
        pass

    def unload(self):
        pass

    def full_unload(self):
        pass


class SceneManager(Scene):
    def __init__(self, name, z_index):
        super().__init__(name, z_index)
        self.scenes = list()

    def render(self):
        for s in self.scenes:
            s.render()

    def update(self):
        for s in self.scenes:
            s.update()

    def activate(self):
        for s in self.scenes:
            s.activate()

    def full_activate(self):
        for s in self.scenes:
            s.full_activate()

    def on_mouse_down(self, btn, x, y):
        for s in self.scenes:
            s.on_mouse_down(btn, x, y)

    def on_mouse_up(self, btn, x, y):
        for s in self.scenes:
            s.on_mouse_up(btn, x, y)

    def on_mouse_drag(self, btn, it, pt):
        for s in self.scenes:
            s.on_mouse_drag(btn, it, pt)

    def on_mouse_move(self, x, y):
        for s in self.scenes:
            s.on_mouse_move(x, y)

    def on_mouse_hold(self, btn):
        for s in self.scenes:
            s.on_mouse_move(btn)

    def on_keyboard_down(self, key, modifiers):
        for s in self.scenes:
            s.on_keyboard_down(key, modifiers)

    def on_keyboard_up(self, key, modifiers):
        for s in self.scenes:
            s.on_keyboard_up(key, modifiers)

    def on_keyboard_hold(self, key, modifiers):
        for s in self.scenes:
            s.on_keyboard_hold(key, modifiers)

    def unload(self):
        for s in self.scenes:
            s.unload()

    def full_unload(self):
        for s in self.scenes:
            s.full_unload()

    def get(self, name):
        for s in self.scenes:
            if s.name == name:
                return s
        return None

    def add(self, scene):
        self.scenes.append(scene)
        self.scenes.sort(key=lambda x: x.z_index, reverse=True)

    def __getitem__(self, item):
        return self.get(item)

    def remove(self, name):
        self.scenes.remove(self.get(name))

    def __str__(self):
        scenes = self.scenes
        scenes.reverse()
        s = "SceneManager{"
        for scene in scenes:
            s += f"SceneManager(\"{scene.name}\"), "
        return s[:-2] + "}"

