
import math
from units import Units
from random import randint
from settings import Settings


cellCanv = None
OnClickFunc = None

class Cell():
    Units = None
    PosX = 0
    PosY = 0
    ScreenSize = 0
    Resources = None
    Obj = None
    NameText = None
    UnitsCount = None
    ArrayPos = ()


    def __init__(self, units, posx, posy, scrSz, res, arrpos):
        self.Units, self.PosX, self.PosY, self.Resources, self.ArrayPos = units, posx, posy, res, arrpos
        hs = scrSz/2 #half size
        qs = scrSz/4 #quarter size
        self.Obj = cellCanv.create_polygon( (posx, posy-hs),
                                            (posx+hs, posy-qs), (posx+hs, posy+qs),
                                            (posx, posy+hs),
                                            (posx-hs, posy+qs), (posx-hs, posy-qs),
                                            (posx, posy-hs),fill="gray",outline='black')
        self.NameText = cellCanv.create_text(posx,posy-10)
        self.UnitsCount = cellCanv.create_text(posx,posy+10)
        cellCanv.tag_bind(self.Obj, "<Button-1>", self.OnClick)
        cellCanv.tag_bind(self.NameText, "<Button-1>", self.OnClick)
        cellCanv.tag_bind(self.UnitsCount, "<Button-1>", self.OnClick)

    def OnClick(self, event):
        OnClickFunc(self)

    def ReloadText(self):
        if not self.Units == None:
            cellCanv.itemconfig(self.Obj, fill=self.Units.Owner.Color)
            cellCanv.itemconfig(self.NameText, text=self.Units.Owner.Name)
            cellCanv.itemconfig(self.UnitsCount, text=str(self.Units.Num))
        else:
            cellCanv.itemconfig(self.Obj, fill="gray")
            cellCanv.itemconfig(self.NameText, text="")
            cellCanv.itemconfig(self.UnitsCount, text="")

    def RecUnits(self, units):
        if self.Units == None:
            self.Units = units
            self.Units.Num -= Settings.UnitsForCaptureCell
        elif not self.Units.Owner == units.Owner and self.Units.Num - units.Num >= 0:
            calcUnits = self.Units.Num - units.Num + randint(math.ceil(-units.Num/4), math.ceil(units.Num/4))
            if not self.Units.Owner == units.Owner and calcUnits < 0:
                units.Num = -calcUnits
                self.Units = Units.Clone(units)
            else:
                self.Units.Num = calcUnits
        elif self.Units.Owner == units.Owner:
            self.Units.Num += units.Num
        
        self.ReloadText()

    def SendUnits(self, num):

        if self.Units.Num - num >= 0:
            self.Units.Num -= num
            cellCanv.itemconfig(self.NameText, text=self.Units.Owner.Name)
            cellCanv.itemconfig(self.UnitsCount, text=str(self.Units.Num))
        else:
            return
        
        return Units(num, self.Units.Owner)

