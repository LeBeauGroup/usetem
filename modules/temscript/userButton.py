class UserButton():

    def __int__(self, button):
        self.button = button

    def name(self):
        return self.button.Name

    def label(self):
        return self.button.Label

    def assignmentName(self, name=None):

        if name is None:
            return self.button.Assignment
        else:
            self.button.Assignment = name
