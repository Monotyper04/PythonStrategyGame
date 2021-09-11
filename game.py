from random import randint
import cell
from cell import Cell
from player import Player
from settings import Settings
from units import Units
from tkinter import *
import math

Players = [ Player('tes', "red", 99999, None), 
            Player("gig", "blue", 000, None),
            Player("Olg", "green", 000, None)]

Cells = []

root = Tk()
 
c = Canvas(root, width=Settings.ScreenRes[0], height=Settings.ScreenRes[1], bg='white')
c.pack()
cell.cellCanv = c

PlayersTurn = 0
UnitsSendNum = 10 #how many units has been sended
SelectedCell = None

def UpUnSnN(*args): #Up UnitSendNum
    global UnitsSendNum

    UnitsSendNum+=10
    if UnitsSendNum > 100:
        UnitsSendNum = 10
    
    UpdateGui()

def DwnUnSnN(*args): #Down UnitSendNum
    global UnitsSendNum

    UnitsSendNum-=10
    if UnitsSendNum < 10:
        UnitsSendNum = 100

    UpdateGui()

def OnClick(cl):
    global PlayersTurn
    global SelectedCell

    print("click" + str(cl.ArrayPos))

    checkUnits = not cl.Units == None and cl.Units.Num > 0 and cl.Units.Owner.Name == Players[PlayersTurn].Name

    if SelectedCell == None and checkUnits:
        SelectedCell = cl

    elif not SelectedCell == None:
        deltaPos = (SelectedCell.ArrayPos[0] - cl.ArrayPos[0], SelectedCell.ArrayPos[1] - cl.ArrayPos[1])
        checkNearOdd = not SelectedCell.ArrayPos[1]%2 == 0 and deltaPos[0] <= 0 and deltaPos[0] >=-1 and deltaPos[1] <= 1 and deltaPos[1] >=-1
        checkNearEven = SelectedCell.ArrayPos[1]%2 == 0 and deltaPos[0] <= 1 and deltaPos[0] >= 0 and deltaPos[1] <= 1 and deltaPos[1] >=-1

        if checkNearEven or checkNearOdd:
            cl.RecUnits(SelectedCell.SendUnits(UnitsSendNum))

            SelectedCell = None

            PlayersTurn += 1
            if PlayersTurn > len(Players)-1:
                PlayersTurn = 0

            UpdateGui()


cell.OnClickFunc = OnClick

def UpdateGui():
    c.itemconfig(gui, text="Turn:"+Players[PlayersTurn].Name+" SelectedUnits:"+str(UnitsSendNum))


if len(Cells) == 0 :
    ypos=Settings.CellSize/2
    y=0
    while ypos <= Settings.NumCells[1] * Settings.CellSize:
        XCells = []
        x=0
        while x < math.ceil(Settings.NumCells[0]):
            if y%2 == 0:
                xpos = Settings.CellSize * x + Settings.CellSize/2
            else:
                xpos = Settings.CellSize * (x + 1)

            XCells.append(Cell(None, xpos, ypos, Settings.CellSize, None, (x,y)))
            x+=1
        Cells.append(XCells)
        ypos+=Settings.CellSize/1.25
        y+=1

gui = c.create_text(20, Settings.ScreenRes[1]-20, anchor="w")
UpdateGui()

root.bind("e",UpUnSnN)
root.bind("q",DwnUnSnN)


for i in range(len(Players)):
    Cells[randint(0,Settings.NumCells[0]-1)][randint(0,Settings.NumCells[1]-1)].RecUnits(Units(randint(100,150),Players[i]))


root.mainloop()
