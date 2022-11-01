from tkinter import *
import tkinter
from time import sleep

# ~ Дополнительные методы
def sign(x):
    if x >= 0: return 1
    return -1
# Дополнительные методы ~

# ~ Алгоритмы отрисовки
def draw_dot(x,y,col='black'):
   canvas.create_line(x,y,x+1,y+1,fill=col) 
def BresenhamV4(x1,y1,x2,y2): # четырёхсвязная развёртка 
    global ContourPoints
    x,y,dx,dy,s1,s2 = x1,y1,abs(x2-x1),abs(y2-y1),sign(x2-x1),sign(y2-y1)
    l = None
    if dy<dx: l = False
    else:
        l = True
        dx,dy = dy,dx
    e = 2*dy-dx
    for i in range(1,dx+dy):
        draw_dot(x,y)
        ContourPoints.append([x,y])
        if e < 0:
            if l: y = y + s2
            else: x = x + s1
            e = e+2*dy
        else:
            if l : x = x + s1
            else: y = y + s2
            e = e - 2*dx
    ContourPoints.append([x,y])
    draw_dot(x,y)


#  Алгоритмы отрисовки ~



# ~UI Функционал

def callback(event): # метод отслеживания нажатий
    global counter,coords,var
    coords.append([int(event.x),int(event.y)])
    if len(coords) > 1:
        tmp = len(coords)
        BresenhamV4(coords[tmp-2][0],coords[tmp-2][1],coords[tmp-1][0],coords[tmp-1][1])
         
    print('Current click: ',counter + 1)
    print('Vertex coordinates: ',coords)
    counter += 1
# функция, замыкающая контур => соед начало с концом
def close():
    global coords
    BresenhamV4(coords[0][0],coords[0][1],coords[len(coords)-1][0],coords[len(coords)-1][1])
#функция, находящая максимальный и минимальный y
def findMm():
    global ContourPoints
    ym,YM = coords[0][1],coords[0][1]
    for i in range(len(ContourPoints)):
        if ym >= ContourPoints[i][1]: ym = ContourPoints[i][1]
        if YM <= ContourPoints[i][1]: YM = ContourPoints[i][1]
    return [ym,YM]


def pave(sign,SeedPixel):

     global ContourPoints,coords,counter,ci,sbsm
     tmpY  = None
     ym,YM = findMm()
     InnerPoints = []  # координаты точек внутри замкнутого контура 
     while len(SeedPixel) != 0:
            
            pixel = SeedPixel.pop()
            x,y = pixel[0],pixel[1]
            tmpY = y
            tmpInnerPoints = [el for el in InnerPoints]
            
            draw_dot(x,y,ci)
            if [x,y] not in InnerPoints: InnerPoints.append([x,y])
            xw = x
            x = x + 1
            while [x,y] not in ContourPoints:
                if [x,y] not in InnerPoints:
                    InnerPoints.append([x,y])
                    draw_dot(x,y,ci)
                x = x + 1
            xr = x - 1
            x = xw 
            x = x - 1
            while [x,y] not in ContourPoints:  
                if [x,y] not in InnerPoints:
                    InnerPoints.append([x,y])
                    draw_dot(x,y,ci)
                x = x - 1
            xl = x + 1
       # x = x + 1
            x = xl
            y = y + sign
            while x <= xr:
                if sbsm.get() == 1 :  root.update()
                fl = False
                while ([x,y] not in ContourPoints) and ([x,y] not in InnerPoints) and (x < xr):
                    x = x + 1
                    if not fl: fl = True
                    else :
                        if (x == xr) and ([x,y] not in ContourPoints) and ([x,y] not in InnerPoints):SeedPixel.append([x,y])
                        else: SeedPixel.append([x-1,y])
                        fl = False
                        
                xb = x
                while ([x,y] in ContourPoints) or ([x,y] in InnerPoints) and (x < xr): x = x + 1
                if x == xb: x = x + 1
            
                if [x,y] in coords or y <= ym  or y >= YM  : break
                if sign == 1 and tmpY > y: break
                if sign == -1 and tmpY < y: break
            if tmpInnerPoints == InnerPoints: 
                print('breakpoint')
                break
                print(ym,YM,y)
     print('Finished with dy = ', sign)
        


def fillSquare(event):
    global ContourPoints,coords,counter,ci
    close()
    pave(1,[[event.x,event.y]])
    pave(-1,[[event.x,event.y]])
                    



    # Обнуление параметров
    ContourPoints = []
    coords = []
    counter = 0

        

        

        

def clear(): # очистить холст
    global InnerPoints,ContourPoints,coords
    InnerPoints = []
    ContourPoints = []
    coords = []
    counter = 0
    canvas.delete("all") 
# UI Функционал~

if __name__ == "__main__":
    # Инициализация и базовая настройки окна
    root = Tk()
    root.title('Лабораторные работы № 4 Реализация алгоритмов растровой графики для заполнения сплошных областей')
    root.resizable(0, 0)

    # Инициализация важных переменных
    counter = 0 # переменная, в которой хранится номер клика мыши
    coords = [] # координаты вершин
    ContourPoints = [] # координаты точек линии замкнутого контура
    ci = 'blue' # цвет, в который будет подкрашиватся замкнутая область

    # Инициализация и настройка холста
    canvas= Canvas(root, width=800, height=600,bg='white')
    canvas.bind("<Button-1>", callback)
    canvas.bind("<Button-3>", fillSquare)
    canvas.pack()
    # Step by step mode (animation)
    sbsm = IntVar()
    sbsmCBtn = Checkbutton(root, text = "Step by step mode",
                      variable = sbsm,
                      onvalue = 1,
                      offvalue = 0)
    sbsmCBtn.pack()

    # Кнопка очистки очистка холста
    clsBtn = tkinter.Button(root,text='Очистить холст',command=clear)
    clsBtn.pack()
    root.mainloop()
