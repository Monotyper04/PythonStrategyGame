class Units():
    Num = 0
    Owner = None

    def __init__(self, num, owner):
        self.Num, self.Owner = num, owner

    def Clone(self, orig):
        Units(copy.Num, copy.Owner )