import sys


class TVUModule(object):

    def __init__(self, name):
        self.__name__ = name

        import _tvu
        import tvus

        self.tvus = tvus

        self.TVU = _tvu.TVU
        self.EnumTVU = _tvu.EnumTVU

        self.instance = _tvu.instance
        self.nullable = _tvu.nullable

        self._validate_and_unify = _tvu.validate_and_unify

    def __call__(self, **kwargs):
        return self._validate_and_unify(**kwargs)


sys.modules[__name__] = TVUModule(__name__)
