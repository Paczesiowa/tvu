import sys


class TVUModule(object):

    def __init__(self, name):
        self.__name__ = name
        import _tvu
        self.TVU = _tvu.TVU
        self._validate_and_unify = _tvu.validate_and_unify

    def __call__(self, **kwargs):
        return self._validate_and_unify(**kwargs)


sys.modules[__name__] = TVUModule(__name__)
