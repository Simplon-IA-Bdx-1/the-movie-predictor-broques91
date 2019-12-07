class Company:

    def __init__(self, name):

        self.name = name
        self.id = None

    def __repr__(self):
        return "#{}: {}".format(self.id, self.name)