import json
from base64 import b64encode, b64decode


class JSONLoader:
    @staticmethod
    def _save(d):
        return json.dumps(d)

    @staticmethod
    def _load(j):
        return json.loads(j)

    @staticmethod
    def load(path, default):
        try:
            with open(path) as f:
                return JSONLoader._load(f.read())
        except FileNotFoundError:
            return default

    @staticmethod
    def save(path, d):
        f = open(path, "w+")
        f.write(JSONLoader._save(d))
        f.close()

    @staticmethod
    def load_and_fill_missing(path, default, *args):
        print(path)
        print(default)
        for d in args:
            default.update(d)
        default.update(JSONLoader.load(path, default))
        return default

class CompressedDataLoader(JSONLoader):
    @staticmethod
    def _save(d):
        return b64encode(super()._save(d))

    @staticmethod
    def _load(j):
        return b64decode(super()._load(j))



