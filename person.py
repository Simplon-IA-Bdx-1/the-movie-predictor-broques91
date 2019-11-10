class Person:

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

        self.id = None

    def __repr__(self):
        return "#{}: {} {}".format(self.id, self.firstname, self.lastname)