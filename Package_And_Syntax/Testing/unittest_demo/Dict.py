class Dict(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("Dict object has not attribute {}".format(key))

    def __setattr__(self, key, value):
        self[key] = value

