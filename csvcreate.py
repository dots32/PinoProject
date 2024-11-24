import pandas as pd
from tkinter import *

BG = "#f7f5dd"
PFONT = ('courier', 18, 'bold')
TFONT = ('courier', 18, 'bold')
FONT = ('courier', 12, 'bold')
LFONT = ('courier', 10, 'normal')
COnOff = 0
POnOff = 0
ClientConfigOptions = []
PackageConfigOptions = []

try:
  df = pd.read_csv('PackagesAndCost.csv')
except:
  rows = ['Price/Comp', 'Price/User', 'Cost/Comp', 'Cost/User', 'totalPrice', 'totalCost', 'profit']
  columns = ['Base', 'Cybersecurity', 'Compliance']
  d = {'Base': [80, 185, 10, 65, 265, 75, 190], 'Cybersecurity': [130, 185, 10, 65, 315, 75, 240], 'Compliance': [180, 185, 10, 65, 365, 75, 290]}
  df = pd.DataFrame.from_dict(d)
  df.index = rows
  df.to_csv('PackagesAndCost.csv')
else:
  df = pd.read_csv('PackagesAndCost.csv', index_col=[0])
  rows = ['Price/Comp', 'Price/User', 'Cost/Comp', 'Cost/User', 'totalPrice', 'totalCost', 'profit']
  df.index = rows
  df.to_csv('PackagesAndCost.csv', index=True, header=True)

try:
  dl = pd.read_csv('ClientData.csv')
except:
  col = ['clientName', 'packageName', 'devices', 'users', 'clientPay', 'companyCost', 'profit']
  temprow = {num: 'x' for num in range(7)}
  dct = {k:[v] for k,v in temprow.items()}
  dl = pd.DataFrame.from_dict(dct)
  dl.columns = col
  rc = pd.read_csv('PackagesAndCost.csv')
else:
  col = ['clientName', 'packageName', 'devices', 'users', 'clientPay', 'companyCost', 'profit']
  dl = pd.read_csv('ClientData.csv', index_col=[0])
  # dl.columns = col
  dl.to_csv('ClientData.csv', index=True, header=True)
  rc = pd.read_csv('PackagesAndCost.csv')

def AddNewClientRow(cn, pn, su, us):
    newdict = [[cn, pn, su, us, ((su * rc[pn][0]) + (us * rc[pn][1])), ((su * rc[pn][2]) + (us * rc[pn][3])), (((su * rc[pn][0]) + (us * rc[pn][1])) - ((su * rc[pn][2]) + (us * rc[pn][3])))]]
    newdf = pd.DataFrame(newdict, columns=col)
    global dl
    dl = pd.concat([dl, newdf], ignore_index=True)
    dl = dl.reindex(columns=col)
    dl.index = dl.index + 1
    dl.to_csv('ClientData.csv', index=True, header=True)

def DelClientRow(num):
    global dl
    dl = pd.read_csv('ClientData.csv', index_col=[0])
    dl = dl.drop(dl.index[num])
    # dl = dl.reset_index(drop=True)
    dl.index = range(1, len(dl) + 1)
    dl.to_csv('ClientData.csv', index=True, header=True)


def AddPackage(pn, pc, pu, cc, cu):
  pdict = {pn: [pc, pu, cc, cu, (pc + pu), (cc + cu), (pc + pu) - (cc + cu)]}
  pdf = pd.DataFrame.from_dict(pdict)
  pdf.index = rows
  global df
  df = pd.concat([df, pdf], axis=1)
  df.to_csv('PackagesAndCost.csv')

def DelPackage(num):
  global df
  df = df.drop(df.columns[num], axis=1)
  df.index = rows
  df.to_csv('PackagesAndCost.csv')

def UpdateAllCInputs():
    global CN
    CN = ClientNameInput.get()
    global PN
    PN = PackagesInput.get()
    global CB
    CB = CompsUsedBox.get()
    global UB
    UB = UsersBox.get()
    global DCI
    DCI = DelCIndexInput.get()
    global DNI
    DNI = DelCNameInput.get()
def UpdateAllPInputs():
    global PKN
    PKN = PackageNameInput.get()
    global PPC
    PPC = PricePerCompInput.get()
    global PPU
    PPU = PricePerUserInput.get()
    global CPU
    CPU = CostPerUserInput.get()
    global CPC
    CPC = CostPerCompInput.get()
    global DPI
    DPI = DelPByIndexInput.get()
    global DPN
    DPN = DelPByNameInput.get()

def AddCRowGUI():
    UpdateAllCInputs()
    AddNewClientRow(str(CN), str(PN), int(CB), int(UB))

def DelCRowGUI():
    UpdateAllCInputs()
    DelClientRow(int(DCI))

def AddPColGUI():
    UpdateAllPInputs()
    AddPackage(str(PKN), int(PPC), int(PPU), int(CPU), int(CPC))

def DelPColGUI():
    UpdateAllPInputs()
    DelPackage(int(DPI))

window = Tk()
window.title('Pino gui')
window.minsize(width=500, height=400)
window.config(bg=BG, padx=50, pady=70)

Title = Label(text='Admin Configuration', font=TFONT, bg=BG)
Title.place(x=70, y=0)

WhichTable = Label(text='Which table would you like to configure?', font=FONT, bg=BG)
WhichTable.place(x=0, y=30)

def ClientConfigOptionsAppear():
    global COnOff
    global ClientConfigOptions
    global PackageConfigOptions
    global POnOff
    POnOff = 0
    COnOff = COnOff + 1
    if COnOff % 2 == 1:
        for item in PackageConfigOptions:
            item.place_forget()

        ClientAddButton = Button(text='Add', bg=BG, width=12, highlightthickness=0, command=AddCRowGUI)
        ClientAddButton.place(x=200, y=75)
        ClientConfigOptions.append(ClientAddButton)

        ClientDelButton = Button(text='Delete', bg=BG, width=12, highlightthickness=0, command=DelCRowGUI)
        ClientDelButton.place(x=300, y=75)
        ClientConfigOptions.append(ClientDelButton)

        ToAddLabel = Label(text='To add a client-', font= FONT, bg=BG)
        ToAddLabel.place(x=200, y=100)
        ClientConfigOptions.append(ToAddLabel)

        ClientNameLabel = Label(text='Client Name:', font=LFONT, bg=BG)
        ClientNameLabel.place(x=200, y=120)
        ClientConfigOptions.append(ClientNameLabel)
        PackageNameLabel = Label(text='Package Bought:', font=LFONT, bg=BG)
        PackageNameLabel.place(x=200, y=140)
        ClientConfigOptions.append(PackageNameLabel)
        ComputersLabel = Label(text='Devices Used:', font=LFONT, bg=BG)
        ComputersLabel.place(x=200, y=162)
        ClientConfigOptions.append(ComputersLabel)
        UsersUsingLabel = Label(text='User Count:', font=LFONT, bg=BG)
        UsersUsingLabel.place(x=200, y=182)
        ClientConfigOptions.append(UsersUsingLabel)

        ToDelLabel = Label(text='To Delete a client-', font= FONT, bg=BG)
        ToDelLabel.place(x=200, y=200)
        ClientConfigOptions.append(ToDelLabel)

        RowToDeleteByIndex = Label(text='Row (index):', font=LFONT, bg=BG)
        RowToDeleteByIndex.place(x=200, y=220)
        ClientConfigOptions.append(RowToDeleteByIndex)

        OrLabel = Label(text='Or', font=LFONT, bg=BG)
        OrLabel.place(x=230, y=240)
        ClientConfigOptions.append(OrLabel)

        RowToDeleteByName = Label(text='Row (Name):', font=LFONT, bg=BG)
        RowToDeleteByName.place(x=200, y=260)
        ClientConfigOptions.append(RowToDeleteByName)

        global ClientNameInput
        ClientNameInput = Entry(width=15, bg=BG)
        ClientNameInput.insert(END, '')
        ClientNameInput.place(x=300, y=122)
        ClientConfigOptions.append(ClientNameInput)

        global PackagesInput
        PackagesInput = Entry(width=15, bg=BG)
        PackagesInput.insert(END, '')
        PackagesInput.place(x=323, y=142)
        ClientConfigOptions.append(PackagesInput)

        global CompsUsedBox
        CompsUsedBox = Spinbox(from_=0, to=100000, width=10, bg=BG)
        CompsUsedBox.place(x=310, y=163)
        ClientConfigOptions.append(CompsUsedBox)

        global UsersBox
        UsersBox = Spinbox(from_=0, to=100000, width=10, bg=BG)
        UsersBox.place(x=295, y=184)
        ClientConfigOptions.append(UsersBox)

        global DelCIndexInput
        DelCIndexInput = Entry(width=15, bg=BG)
        DelCIndexInput.place(x=300, y=222)
        ClientConfigOptions.append(DelCIndexInput)

        global DelCNameInput
        DelCNameInput = Entry(width=15, bg=BG)
        DelCNameInput.place(x=300, y=262)
        ClientConfigOptions.append(DelCNameInput)

    elif COnOff % 2 == 0:
        for item in ClientConfigOptions:
            item.place_forget()
        for item in PackageConfigOptions:
            item.place_forget()


def PackageConfigOptionsAppear():
    global PackageConfigOptions
    global ClientConfigOptions
    global POnOff
    global COnOff
    COnOff = 0
    POnOff += 1
    if POnOff % 2 == 1:
        for item in ClientConfigOptions:
            item.place_forget()

        PackageAddButton = Button(text='Add', bg=BG, width=12, highlightthickness=0, command=AddPColGUI)
        PackageAddButton.place(x=200, y=75)
        PackageConfigOptions.append(PackageAddButton)

        PackageDelButton = Button(text='Delete', bg=BG, width=12, highlightthickness=0, command=DelPColGUI)
        PackageDelButton.place(x=300, y=75)
        PackageConfigOptions.append(PackageDelButton)

        PackageAddLabel = Label(text='To add a package-', font=FONT, bg=BG)
        PackageAddLabel.place(x=200, y=100)
        PackageConfigOptions.append(PackageAddLabel)

        PackageNameLabel = Label(text='Package Name:', font=LFONT, bg=BG)
        PackageNameLabel.place(x=200, y=120)
        PackageConfigOptions.append(PackageNameLabel)
        PricePerUserLabel = Label(text='Price per user:', font=LFONT, bg=BG)
        PricePerUserLabel.place(x=200, y=140)
        PackageConfigOptions.append(PricePerUserLabel)
        PricePerCompLabel = Label(text='Price per comp:', font=LFONT, bg=BG)
        PricePerCompLabel.place(x=200, y=160)
        PackageConfigOptions.append(PricePerCompLabel)
        CostPerUserLabel = Label(text='Cost per user:', font=LFONT, bg=BG)
        CostPerUserLabel.place(x=200, y=180)
        PackageConfigOptions.append(CostPerUserLabel)
        CostPerCompLabel = Label(text='Cost per comp:', font=LFONT, bg=BG)
        CostPerCompLabel.place(x=200, y=200)
        PackageConfigOptions.append(CostPerCompLabel)

        global PackageNameInput
        PackageNameInput = Entry(width=15, bg=BG)
        PackageNameInput.place(x=308, y=122)
        PackageConfigOptions.append(PackageNameInput)

        global PricePerCompInput
        PricePerCompInput = Entry(width=15, bg=BG)
        PricePerCompInput.place(x=323, y=142)
        PackageConfigOptions.append(PricePerCompInput)

        global PricePerUserInput
        PricePerUserInput = Entry(width=15, bg=BG)
        PricePerUserInput.place(x=323, y=162)
        PackageConfigOptions.append(PricePerUserInput)

        global CostPerUserInput
        CostPerUserInput = Entry(width=15, bg=BG)
        CostPerUserInput.place(x=315, y=182)
        PackageConfigOptions.append(CostPerUserInput)

        global CostPerCompInput
        CostPerCompInput = Entry(width=15, bg=BG)
        CostPerCompInput.place(x=315, y=202)
        PackageConfigOptions.append(CostPerCompInput)

        global DelPByIndexInput
        DelPByIndexInput = Entry(width=15, bg=BG)
        DelPByIndexInput.place(x=326, y=246)
        PackageConfigOptions.append(DelPByIndexInput)

        global DelPByNameInput
        DelPByNameInput = Entry(width=15, bg=BG)
        DelPByNameInput.place(x=318, y=286)
        PackageConfigOptions.append(DelPByNameInput)

        ToDelPLabel = Label(text='To Delete a package-', font=FONT, bg=BG)
        ToDelPLabel.place(x=200, y=222)
        PackageConfigOptions.append(ToDelPLabel)

        ColToDeleteByIndexLabel = Label(text='Column (index):', font=LFONT, bg=BG)
        ColToDeleteByIndexLabel.place(x=200, y=244)
        PackageConfigOptions.append(ColToDeleteByIndexLabel)

        OrPLabel = Label(text='Or', font=LFONT, bg=BG)
        OrPLabel.place(x=230, y=264)
        PackageConfigOptions.append(OrPLabel)

        ColToDeleteByNameLabel = Label(text='Column (Name):', font=LFONT, bg=BG)
        ColToDeleteByNameLabel.place(x=200, y=284)
        PackageConfigOptions.append(ColToDeleteByNameLabel)

    elif POnOff % 2 == 0:
        for item in ClientConfigOptions:
            item.place_forget()
        for item in PackageConfigOptions:
            item.place_forget()






ClientButton = Button(text='ClientData', bg=BG, width=25, height=4, highlightthickness=0, command=ClientConfigOptionsAppear)
ClientButton.place(x=0, y=100)

PackagesButton = Button(text='Packages', bg=BG, width=25, height=4, highlightthickness=0, command=PackageConfigOptionsAppear)
PackagesButton.place(x=0, y=200)



window.mainloop()