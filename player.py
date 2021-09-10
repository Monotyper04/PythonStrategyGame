class Player():
    Name = ""
    Color = ""
    Money = 0
    Resources = {}

    def __init__(self, name, color, money, res):
        self.Name, self.Color, self.Money, self.Resources = name, color, money, res
