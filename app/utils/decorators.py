import json


def to_json(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def to_json_str(self):
    return json.dumps(to_json(self))


def add_json_exporter_to_sqlalchemy_model(cls):
    setattr(cls, "to_json", to_json)
    return cls


def add_json_str_exporter_to_sqlalchemy_model(cls):
    setattr(cls, "to_json_str", to_json_str)
    return cls
