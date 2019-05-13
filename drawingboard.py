#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @brief: 计算机图形学大作业
# @author: 161240045 鲁昊
# @envir: linux+python3+tkinter

from tkinter import *
import tkinter.messagebox as messagebox # 弹窗
import pyscreenshot as ImageGrab  # for linux
# from PIL import ImageGrab       # for MacOS and windows


window = Tk() # 创建窗口对象
window.title("Drawing Board") # 设置窗口标题
window.geometry("800x600") # 窗口的初始化大小

# 控制是否允许画图 0:允许画图  1:不允许画图
Flag_draw = IntVar(value=0)

# 控制画图的类型 0:曲线  1:直线
Type_draw = IntVar(value=0)

# (X,Y)记录鼠标的位置
X,Y = IntVar(value=0), IntVar(value=0)

# ID记录每个元素
ID = 0
_id = 0
# TODO 添加一个容器，存储画布上的所有图元，方便后面的平移和删除等操作
All = []
tmp = []

# 选择画笔的颜色和粗细
Color_pen = '#000000'
Width_pen = 2

# 创建顶部菜单栏
menu = Menu(window)

# 添加"File"菜单栏 --保存文件等
File_menu = Menu(menu, tearoff=0)
menu.add_cascade(label='文件',menu=File_menu)

# linux下不可以使用PIL中的ImageGrab截图，因此用pyscreenshot代替
# TODO 1.自定义保存的文件名  2.保存准确的窗口大小

def File_save():
    pic = ImageGrab.grab()
    pic.save('1.bmp')
    messagebox.showinfo(title='warning',message='成功保存至当前目录：*.bmp')

def File_reset():
    for i in canvas.find_all():
        canvas.delete(i)
    messagebox.showinfo(title='warning',message='成功清空画布')


File_menu.add_command(label='保存', command=File_save)
File_menu.add_command(label='清空',command=File_reset)



# 添加"Color"菜单栏 --选择画笔颜色
Color_menu = Menu(menu, tearoff=0)
menu.add_cascade(label='颜色',menu=Color_menu)

def Color_black():
    global Color_pen
    Color_pen = '#000000'
def Color_red():
    global Color_pen
    Color_pen = '#FF0000'
def Color_blue():
    global Color_pen
    Color_pen = '#008FFF'

Color_menu.add_command(label='黑色', command=Color_black)
Color_menu.add_command(label='红色',   command=Color_red)
Color_menu.add_command(label='蓝色', command=Color_blue)


# 添加"Width"菜单栏 --设置画笔粗细
Width_menu = Menu(menu, tearoff=0)
menu.add_cascade(label='粗细',menu=Width_menu)

def Width_1():
    global Width_pen
    Width_pen = 1

def Width_3():
    global Width_pen
    Width_pen = 3

def Width_5():
    global Width_pen
    Width_pen = 5

Width_menu.add_command(label='1 磅',   command=Width_1)
Width_menu.add_command(label='3 磅',   command=Width_3)
Width_menu.add_command(label='5 磅',   command=Width_5)


# 添加"Draw Type"菜单栏 --切换绘制图形的类别
Draw_menu = Menu(menu, tearoff=0)
menu.add_cascade(label='绘图',menu=Draw_menu)

def Draw_point(x,y):
    # 实现画点,这是后面画直线、圆、多边形等等的基础
    return canvas.create_oval(x,y, x,y,
                        fill = Color_pen, outline = Color_pen,
                        width = Width_pen)


def Choose_line():
    Type_draw.set(1)
    messagebox.showinfo(title='warning',message='切换成功:开始绘制直线')

def Choose_point():
    Type_draw.set(2)
    messagebox.showinfo(title='warning',message='切换成功:开始绘制点')

def Choose_ellipse():
    Type_draw.set(3)
    messagebox.showinfo(title='warning',message='切换成功:开始绘制椭圆')

Draw_menu.add_command(label='直线', command=Choose_line)
Draw_menu.add_command(label='椭圆', command=Choose_ellipse)

# 对图元删除，平移等操作
Operate_menu = Menu(menu, tearoff=0)
menu.add_cascade(label='操作',menu=Operate_menu)

def Delete(_id):
    # 提供输入框
    for i in All[_id]:
        canvas.delete(i)

Operate_menu.add_command(label='删除',command=Delete)



def Bresenham(x1, y1, x2, y2):
    pointList = []
    if x1 == x2: # Special Case: Horizenal Line
        if y1 <= y2:
            return [[x1, y] for y in range(y1, y2 + 1)]
        else:
            pointList = [[x1, y] for y in range(y2, y1 + 1)]
            pointList.reverse()
            return pointList
    elif abs(y2 - y1) <= abs(x2 - x1): 
        return _Bresenham(x1, y1, x2, y2)
    else: 
        pointList = _Bresenham(y1, x1, y2, x2)
        return [[p[1], p[0]] for p in pointList]


def _Bresenham(x1, y1, x2, y2): #
    slope = (y2 - y1) / (x2 - x1)
    p = 2 * slope - 1
    [x, y] = [x1, y1]
    pointList = []
    if x1 < x2:
        if slope >= 0:
            while True:
                pointList.append([x, y])
                if x == x2:
                    return pointList
                if p <= 0:
                    [x, y, p] = [x + 1, y, p + 2 * slope]
                else:
                    [x, y, p] = [x + 1, y + 1, p + 2 * slope - 2]
        else: 
            pointList = _Bresenham(x1, -y1, x2, -y2)
            return [[p[0], -p[1]] for p in pointList]
    else:
        pointList = _Bresenham(x2, y2, x1, y1)
        pointList.reverse()
        return pointList

def Ellipsepot(x0, y0, x, y):
    # 运用椭圆的4路对称画点
    ''' 
    Draw_point((x0 + x), (y0 + y))
    Draw_point((x0 + x), (y0 - y))
    Draw_point((x0 - x), (y0 - y))
    Draw_point((x0 - x), (y0 + y))
    '''
    t = 0.2
    tmp.append(Draw_point((x0 + t*x), (y0 + t*y)))
    tmp.append(Draw_point((x0 + t*x), (y0 - t*y)))
    tmp.append(Draw_point((x0 - t*x), (y0 - t*y)))
    tmp.append(Draw_point((x0 - t*x), (y0 + t*y)))


def Draw_ellipse(x0, y0, a, b):
    # 中点圆生成算法画椭圆
    sqa = a*a;
    sqb = b*b;
    d = sqb + sqa*(0.25 - b);
    x = 0;
    y = b;
    Ellipsepot(x0, y0, x, y);
    while sqb*(x + 1) < sqa*(y - 0.5):
        if d < 0:
            d += sqb*(2 * x + 3)
        else:
            d += (sqb*(2 * x + 3) + sqa*((-2)*y + 2))
            y -= 1
        x += 1
        Ellipsepot(x0, y0, x, y)
    d = (b * (x + 0.5)) * 2 + (a * (y - 1)) * 2 - (a * b) * 2
    while (y > 0):
        if d < 0:
            d += sqb * (2 * x + 2) + sqa * ((-2) * y + 3)
            x += 1
        else:
            d += sqa * ((-2) * y + 3)
        y -= 1
        Ellipsepot(x0, y0, x, y)


# 创建一块画布
#image = PhotoImage()
canvas = Canvas(window, bg='white',width=400,height=300) # 创建一块画布
#canvas.create_image(400,300,image=image)

# 鼠标左键单击，允许开始画图
def onLeftDown(event):
    Flag_draw.set(1)
    # 当前单击坐标记录为绘图的初始位置
    X.set(event.x)
    Y.set(event.y)
    if Type_draw.get() == 2:
        # 画点
        Draw_point(X.get(),Y.get())

# 按住鼠标左键，开始画图
def onLeftMove(event):
    global ID
    if not Flag_draw:
        return
    if Type_draw.get() == 0:
        # 绘制曲线
        canvas.create_line(X.get(),Y.get(),event.x,event.y, 
                        fill = Color_pen, width = Width_pen)
        X.set(event.x)
        Y.set(event.y)
    if Type_draw.get() == 1:
        # 绘制直线
        try:
            for i in tmp:
                canvas.delete(i)
        except Exception as e:
            pass
        for i in Bresenham(X.get(), Y.get(), event.x, event.y):
            tmp.append(Draw_point(i[0],i[1]))
        #ID = canvas.create_line(X.get(), Y.get(), event.x, event.y, 
        #        fill=Color_pen, width=Width_pen)
    if Type_draw.get() == 3:
        # 绘制椭圆
        try:
            for i in tmp:
                canvas.delete(i)
        except Exception as e:
            pass
        Draw_ellipse(X.get(), Y.get(), event.x, event.y)
         
    
# 松开鼠标左键,停止画图
def onLeftUp(event):
    Flag_draw.set(0)
    global ID,_id
    if Type_draw.get() == 1:
        # 绘制直线，此直线要添加到容器中
        All.append([])
        for i in Bresenham(X.get(), Y.get(), event.x, event.y):
            All[ID].append(Draw_point(i[0],i[1]))
        _id = ID
        ID += 1
        Message(window,text='直线 '+str(ID)).pack(side=LEFT)
        Operate_menu.add_command(label='直线'+str(ID),command=Delete(_id))
        messagebox.showinfo(title='warning',message='该直线ID:'+str(ID))
           


    if Type_draw.get() == 3:
        # 绘制椭圆
        All.append([])
        All[ID].append(Draw_ellipse(X.get(), Y.get(), event.x, event.y))
        _id = ID
        ID += 1
        Message(window,text='椭圆 '+str(ID)).pack(side=LEFT)
        Operate_menu.add_command(label='椭圆'+str(ID),command=lambda:Delete(_id))
        messagebox.showinfo(title='warning',message='该椭圆ID:'+str(ID))
    
    Flag_draw.set(0)    
    global tmp
    tmp = []



canvas.bind('<Button-1>',onLeftDown) # 绑定"单击鼠标左键"的事件
canvas.bind('<B1-Motion>',onLeftMove) # 绑定"按住鼠标左键"的事件
canvas.bind('<ButtonRelease-1>',onLeftUp) # 绑定"松开鼠标左键"的事件
canvas.pack(fill=BOTH, expand=YES)
window.config(menu=menu)
window.mainloop()
