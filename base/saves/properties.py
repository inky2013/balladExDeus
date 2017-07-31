class PropertiesLoader:
    def __init__(self):
        self.loaded = None

    def load_file(self=None, _file=None):
        file = _file
        if _file is None:
            file = self
        with open(file) as f:
            txt = [i.split("=") for i in [i for i in f.read().split("\n") if not i.startswith("#")]]
        loaded = dict()
        for i in txt:
            loaded[i[0]] = i[1]
        if _file is not None:
            self.loaded = loaded
        return loaded

    def save_file(self, location):
        f = open(location, "w+")
        for k in self.loaded:
            f.write(k+"="+self.loaded[k])
        f.close()