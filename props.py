class classproperty(object):

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)

    def __set__(self, owner_cls, value):
        if self.fset is None:
            raise AttributeError("setter not implemented")
        self.fset(owner_cls, value)

    def setter(self, fset):
        return classproperty(self.fget, fset)
