class Singleton:
    def __init__(self, cls):
        self._wrapped = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self._wrapped(*args, **kwargs)
        return self._instance


def singleton(cls):
    return Singleton(cls)
