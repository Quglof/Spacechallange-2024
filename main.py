import math as m
import tkinter as tk
from tkinter import ttk


class planet:
    def __init__(self, name, r, yearLenght, offset): # [r] = AU [yearLenght] = years [offset] = deg
        self.name  = name
        self.r = r
        self.yearLenght = yearLenght
        self.offset = offset
        self.angVel = 360/yearLenght

class spaceship:
    def __init__(self, speed, name): # [speed] = AU/year
        self.speed = speed
        self.name = name


Venus = planet("Vénusz",0.723,0.61,0)
Earth = planet("Föld",1,1,0)
Mars = planet("Mars",1.5,1.88,0)
Jupiter = planet("Jupiter",5.2,12,0)
Saturn = planet("Szaturnusz",9.6,29,0)
Uranus = planet("Uránusz",19.8,84.3,0)

SaturnV = spaceship(1.47550183, "NASA Saturn V")
Shuttle = spaceship(1.60306497,"NASA Space Shuttle")
Falcon9 = spaceship(0.643382314,"SpaceX Falcon 9")
SoyuzU = spaceship(0.379701038,"Soyuz-U")


def pos(planet,date): # [date] = years
    a = m.radians((planet.angVel * date + planet.offset)%360)
    x = m.cos(a)*planet.r
    y = m.sin(a)*planet.r
    return (x,y)

def dist(pos1,pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    dist = m.sqrt(abs(x1-x2)**2+abs(y1-y2)**2)
    return dist

def min_dist(planet1,planet2,ship,starttime): # Base date = 2024.01.01, [starttime] = years
    pos1 = planet1.angVel*starttime + planet1.offset
    pos2 = planet2.angVel*starttime + planet2.offset
    i = 0
    while not ((i/365 - abs(planet1.r-planet2.r)/ship.speed > 0) and (abs(pos1-pos2) <= 1 and i > 10)):
        pos1 += planet1.angVel/365
        pos2 += planet2.angVel/365
        pos1 %= 360
        pos2 %= 360
        i += 1
    return i/365 - abs(planet1.r-planet2.r)/ship.speed


def addyeartodate(baseYear,baseMonth,baseDay,addYear):
    outYear = int((addYear // 1) + baseYear)
    addYear -= outYear

    nday = 365
    if baseYear % 4 == 0:
        if (baseYear % 100 == 0 and baseYear % 400 == 0) or baseYear % 100 != 0:
            nday = 366
    outDay = baseDay + round((addYear % 1) * nday)

    counter = 0
    for i, num in enumerate(days):
        counter += num
        if counter >= outDay:
            outMonth = i+1
            outDay -= (counter-num)
            return (outYear,outMonth,outDay)


Planets = [Venus, Earth, Mars, Jupiter, Saturn, Uranus]
Planet_names = [plan.name for plan in Planets]
ships = [SaturnV,Shuttle,SoyuzU,Falcon9]
ship_names = [ship.name for ship in ships]

days = [31,28,31,30,31,30,30,31,30,31,30,31]
months = ["Jan","Feb","Mar","Apr", "Maj", "Jun","Jul","Aug","Sep","Okt","Nov","Dec"]

win = tk.Tk()
win.geometry("300x450")
win.resizable(width=False, height=True)

def shipselect(x,y,z):
    ship = ships[ship_names.index(shipV.get())]
    shipLable.config(text=f"Űrhajó\nSebesség = {ship.speed:.6f} CE/év")


def monthselect(x,y,z):
    year = int(yearV.get())
    if year % 4 == 0:
        if (year % 100 == 0 and year % 400 == 0) or year % 100 != 0:
            days[1] = 29
        else: days[1] = 28
    else: days[1] = 28
    inDays = [x + 1 for x in range(int(days[months.index(monthV.get())] if monthV.get() else 30))]
    dayBox["values"] = inDays


def calculate():
    syear = int(yearBox.get())
    smonth = int(months.index(monthBox.get()))
    sday = int(dayBox.get())

    sPlanet = Planets[Planet_names.index(startPlanetCombobox.get())]
    ePlanet = Planets[Planet_names.index(endPlanetCombobox.get())]
    selected_ship = ships[ship_names.index(shipBox.get())]
    sDate = yearCal()

    alignDate = min_dist(sPlanet,ePlanet,selected_ship,sDate)
    #print(f"{sPlanet.name} --> {ePlanet.name} start @ {sDate} align @ {alignDate}")

    cLable.config(text=f"{sPlanet.name} → {ePlanet.name}\n{yearBox.get()}. {(months.index(monthBox.get())+1):02d}. {int(dayBox.get()):02d}.")

    alignYear, alignMonth, alignDay = addyeartodate(syear,smonth,sday,alignDate)

    d = (dist(pos(sPlanet,sDate),pos(ePlanet,alignDate)))

    distLable.config(text=f"Legrövidebb út\n Indulás: {alignYear}. {alignMonth:02d}. {alignDay:02d}.\nTávolság: {d:.4f} CE\nUtazási idő: {d/selected_ship.speed:.02f} év")


def yearCal():
    year = int(yearBox.get())
    month = int(months.index(monthBox.get()))
    day = int(dayBox.get())
    out = year - 2024 + ((month)+(day-1)/(days[month]))/12
    return out


startplanetLabel = ttk.Label(win, text="Inuló Bolygó", font=("Arial", 10))
endplanetLabel = ttk.Label(win, text="Cél Bolygó", font=("Arial", 10))


startPlanetCombobox = ttk.Combobox(win, values=Planet_names, state="readonly", font=("Arial",10))
endPlanetCombobox = ttk.Combobox(win,values=Planet_names, state="readonly", font=("Arial",10))

shipV = tk.StringVar()
shipLable = ttk.Label(win, text="Űrhajó", font=("Arial", 8), justify="center")
shipBox = ttk.Combobox(win, values=ship_names,state="readonly", font=("Arial",10), textvariable=shipV)
shipV.trace('w',shipselect)

#Date
datelabe = ttk.Label(text="Dátum", font=("Arial", 10), justify="center")
monthV = tk.StringVar()
yearV = tk.StringVar()
yearBox = ttk.Combobox(win, values=[2024+x for x in range(1000)],  textvariable=yearV, font=("Arial",10), width=4)
monthBox = ttk.Combobox(win, values=months, state="readonly", textvariable=monthV, font=("Arial",10), width=4)
dayBox = ttk.Combobox(win, state="readonly", font=("Arial",10), width=2)
monthV.trace("w", monthselect)

#Calulate Button
calButton = ttk.Button(win, text="Számolás!", command=calculate, width=12)

#Calulated stuff's Labels
cLable = ttk.Label(win, font=("Arial",15), justify="center")
distLable = ttk.Label(win, font=("Arial",15), justify="center")
#WIP

startplanetLabel.pack(pady=0)
startPlanetCombobox.pack(pady=0)
endplanetLabel.pack(pady=(10,0))
endPlanetCombobox.pack(pady=(0,10))
shipLable.pack()
shipBox.pack()
datelabe.pack(pady=(10,50))


yearBox.place(x=150 - 30 - (4*10+10) - 10, y=190)
monthBox.place(x=150 - (4*10+10)/2, y=190)
dayBox.place(x=150 + 30 +10, y=190)

calButton.pack()
cLable.pack()
distLable.pack()

win.mainloop()