import sys


class TVUModule(object):

    def __init__(self):
        import tvu_worker
        self.TVU = tvu_worker.TVU

    def __call__(self, **kwargs):
        import tvu_worker
        return tvu_worker.validate_and_unify(**kwargs)


sys.modules[__name__] = TVUModule()
