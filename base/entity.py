import base.lib


class EntityStore:
    def __init__(self):
        self._entities = dict()

    def _gen_uuid(self, str_entity):
        for x in range(100):
            uuid = base.lib.generate_token(8)
            if uuid not in self._entities:
                return uuid
        raise RuntimeError(f"Could not create a uuid for entity \"{str_entity}\"")

    def add(self, entity, uuid=None):
        if uuid is None:
            uuid = self._gen_uuid(str(entity))
        self._entities[uuid] = entity

    def get(self, uuid):
        return self._entities[uuid]


class Entity:
    def __init__(self):
        self.uuid = base.lib.generate_token(8)