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
    global root,sbsm
    x1,y1 = x-1,y-1
    x2,y2 = x+1,y+1
    if sbsm.get() == 0:canvas.create_oval(x1, y1, x2, y2,fill=col,width=1,outline=col) 
    else:
        sleep(0.001)
        canvas.create_oval(x1, y1, x2, y2,fill='red',width=1,outline='red') 
        root.update()

def BresenhamV4(x1,y1,x2,y2): # четырёхсвязная развёртка 
    x,y,dx,dy,s1,s2 = x1,y1,abs(x2-x1),abs(y2-y1),sign(x2-x1),sign(y2-y1)
    l = None
    if dy<dx: l = False
    else:
        l = True
        dx,dy = dy,dx
    e = 2*dy-dx
    for i in range(1,dx+dy):
        draw_dot(x,y)
        pixels.append([x,y])
        if e < 0:
            if l: y = y + s2
            else: x = x + s1
            e = e+2*dy
        else:
            if l : x = x + s1
            else: y = y + s2
            e = e - 2*dx
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
    counter += 1
# функция, замыкающая контур => соед начало с концом
def close():
    global coords
    BresenhamV4(coords[0][0],coords[0][1],coords[len(coords)-1][0],coords[len(coords)-1][1])

def fillSquare(event):
    global pixels,coords,counter
    close()
    ci = 'blue'
    SeedPixel = [[event.x,event.y]]
    while len(SeedPixel) > 0:
        pixel = SeedPixel.pop()
        x,y = pixel[0],pixel[1]
        draw_dot(x,y,ci)
        tmpX,tmpY = x,y
        # вправо вниз
        while [x,y] not in pixels:
            while [x,y] not in pixels:
                draw_dot(x,y,ci)
                x = x + 1
            x = tmpX
            y = y + 1
        # влево вниз
        x,y = tmpX,tmpY
        while [x,y] not in pixels:
            while [x,y] not in pixels:
                draw_dot(x,y,ci)
                x = x - 1
            x = tmpX
            y = y + 1
        # вправо вверх
        x,y = tmpX,tmpY
        while [x,y] not in pixels:
            while [x,y] not in pixels:
                draw_dot(x,y,ci)
                x = x + 1
            x = tmpX
            y = y - 1 
        # влево вверх
        x,y = tmpX,tmpY
        while [x,y] not in pixels:
            while [x,y] not in pixels:
                draw_dot(x,y,ci)
                x = x - 1
            x = tmpX
            y = y - 1 
    coords = []
    pixels = []
    counter = 0

        

        

        

def clear(): # очистить холст
    global coords,counter
    counter = 0
    coords = []
    pixels = []
    canvas.delete("all") 
# UI Функционал~

if __name__ == "__main__":
    # Инициализация и базовая настройки окна
    root = Tk()
    root.title('Лабораторная работа № 2 Реализация вывода сплайнов Безье')
    root.resizable(0, 0)

    # Инициализация важных переменных
    counter = 0 # переменная, в которой хранится номер клика мыши
    coords = [] # координаты точек
    pixels = [] # координаты точек замкнутого контура
    

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