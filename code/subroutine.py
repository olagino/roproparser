class Subroutine(object):
    """This class describes a subroutine. It takes a tuple of input-arguments as an input and returns a tuple of outputs"""
    def __init__(self, inTup):
        self.inTup = inTup
        self.name = ""
        self.objects = []
        self.connections = []

    def newObject(self, type, settings):
        pass
