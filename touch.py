class Touch(object):

    # Requires the touch identifier
    def __init__(self, identifier):
        self.identifier = identifier
        self.xPos = None
        self.yPos = None

    def needs_x(self):
        return self.xPos is None

    def needs_y(self):
        return self.yPos is None

    def is_ready(self):
        return self.xPos is not None and self.yPos is not None
