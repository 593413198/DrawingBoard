#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @brief: 计算机图形学大作业
# @author: 161240045 鲁昊
# @envir: linux+python3+tkinter

'''
70 100
220 200
'''

from tkinter import *
import tkinter.messagebox as messagebox
from math import * # 用到一些三角和反三角函数
import pyscreenshot as ImageGrab  # 一个截屏工具for linux
import sys # 用以接受命令行参数
import time 
# from PIL import ImageGrab       # for MacOS and windows

window = Tk() # 创建窗口对象
window.title("Luhao - Drawing Board") # 设置窗口标题
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
All = [] # 储存图元的ID
for i in range(100000):
    All.append([])
pix = [] # 储存图元的所有坐标
for i in range(100000):
    pix.append([])
Color_list = [0]*100000 # 用于存储每个图元的颜色,为了平移和旋转不改变原颜色
tmp = []

# 选择画笔的颜色和粗细
Color_pen = '#000000'
Width_pen = 2

# 创建一块画布
canvas = Canvas(window, bg='white',width=400,height=300) # 创建一块画布

# 创建顶部菜单栏
menu = Menu(window)

# 添加"File"菜单栏 --保存文件等
File_menu = Menu(menu, tearoff=0)
menu.add_cascade(label='文件',menu=File_menu)

# linux下不可以使用PIL中的ImageGrab截图，因此用pyscreenshot代替
# TODO 1.自定义保存的文件名  2.保存准确的窗口大小

def File_save(name='unamed'):
    pic = ImageGrab.grab((50,110,220,250))
    name += '.bmp'
    pic.save(name)
    #messagebox.showinfo(title='warning',message='图片'+name+'成功保存至当前目录！')

def File_reset(size='800x600'):
    for i in canvas.find_all():
        canvas.delete(i)
    window.geometry(size)
    #messagebox.showinfo(title='warning',message='成功清空画布')

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
    #messagebox.showinfo(title='warning',message='切换成功:开始绘制直线')

def Choose_point():
    Type_draw.set(2)
    #messagebox.showinfo(title='warning',message='切换成功:开始绘制点')

def Choose_ellipse():
    Type_draw.set(3)
    #messagebox.showinfo(title='warning',message='切换成功:开始绘制椭圆')

Draw_menu.add_command(label='点', command=Choose_point)
Draw_menu.add_command(label='直线', command=Choose_line)
Draw_menu.add_command(label='椭圆', command=Choose_ellipse)

def toHex(RGB):
    # 将RGB转化成16进制
    # param: RGB = [255,255,255]
    # return: #FFFFFF
    global Color_pen
    strs = '#'
    for i in RGB:
        num = int(i)
        xx = str(hex(num))
        if (len(xx) == 3):
            strs += '0' + xx[-1]
        else:
            strs += xx[-2:]
    Color_pen = strs

def rotate(x0,y0,x,y,r):
    # 将(x,y)绕(x0,y0)顺时针旋转r°后得到的坐标
    r = radians(r)  # 转化成弧度制
    if x-x0 == 0.0: # 讨论不同的象限
        r1 = pi/2
    elif x-x0 > 0.0:
        r1 = atan( (y-y0)/(x-x0) )  # (x,y)在(x0,y0)的坐标系中的角度
    else:
        r1 = pi + atan( (y-y0)/(x-x0) )
    r1 += r  # 顺时针旋转r
    l = sqrt( (x-x0)**2 + (y-y0)**2 )
    x1, y1 = cos(r1) * l + x0, sin(r1) * l + y0
    return [x1, y1]

def execute(cin=None):
    # TODO 执行命令行指令
    if cin == None:
        cin = entry.get()
    global All, Color_pen # 新画的图元添加到canvas的容器中

    # setColor R G B 切换画笔颜色为(RGB)
    if cin[:8] == 'setColor':
        cin = cin[8:]
        cin = cin.split()
        RGB = []
        for i in cin:
            RGB.append(int(i))
            toHex(RGB)

    # resetCanvas width height (int) 重置画布，并设置宽高
    if cin[:11] == 'resetCanvas':
        cin = cin[11:]
        cin = cin.split()
        cin = cin[0] + 'x' + cin[1]
        File_reset(cin)

    # saveCanvas name 保存画布到*.bmp当前目录下
    if cin[:10] == 'saveCanvas':
        cin = cin[10:]
        cin = cin.split()
        File_save(cin[0])

    # drawLine id x1 y1 x2 y2 DDA/Bresenham 绘制线段，注意给定了id，方便后面的操作
    if cin[:8] == 'drawLine':
        cin = cin[8:]
        cin = cin.split()
        _id = int(cin[0]) #图元编号
        x1,y1,x2,y2 = float(cin[1]),float(cin[2]),float(cin[3]),float(cin[4])
        Color_list[_id] = Color_pen
        if cin[5] == 'DDA': #用DDA算法绘制直线
            for i in DDA(x1,y1,x2,y2):
                pix[_id].append([i[0],i[1]])
                All[_id].append(Draw_point(i[0],i[1]))
            Message(window,text='直线\n'+str(_id)).pack(side=LEFT)
        elif cin[5] == 'Bresenham': #用Bresenham算法绘制直线
            for i in Bresenham(x1,y1,x2,y2):
                pix[_id].append([i[0],i[1]])
                All[_id].append(Draw_point(i[0],i[1]))
            Message(window,text='直线\n'+str(_id)).pack(side=LEFT)

    # drawEllipse id x y rx ry 画椭圆
    if cin[:11] == 'drawEllipse':
        cin = cin[11:]
        cin = cin.split()
        _id = int (cin[0])
        x,y,rx,ry = float(cin[1]),float(cin[2]),float(cin[3]),float(cin[4])
        Color_list[_id] = Color_pen
        for i in Draw_ellipse(x,y,rx,ry):
            pix[_id].append([i[0],i[1]])
            All[_id].append(Draw_point(i[0],i[1]))
        Message(window,text='椭圆\n'+str(_id)).pack(side=LEFT)

    # drawPolygon id n DDA/Bresenham x1 y1 x2 y2 ..... xn yn　画多边形
    if cin[:11] == 'drawPolygon':
        cin = cin[11:]
        cin = cin.split()
        _id, n = int(cin[0]), int(cin[1])
        how = cin[2] # 选择的算法
        point = [] # 多边形的所有顶点
        Color_list[_id] = Color_pen
        for i in range(n):
            point.append( [ int(cin[i*2+3]), int(cin[i*2+4]) ] )
        point.append([point[0][0],point[0][1]]) # 最后记得首尾相连
        # 下面一次做出n条线段
        if how == 'DDA': # 采用DDA算法
            for i in range(n):
                for j in DDA(point[i][0],point[i][1],point[i+1][0],point[i+1][1]):
                    pix[_id].append([j[0],j[1]])
                    All[_id].append(Draw_point(j[0],j[1]))
            Message(window,text='多边形\n'+str(_id)).pack(side=LEFT)

        elif how == 'Bresenham': # 采用Bresenham算法
            for i in range(n):
                for j in Bresenham(point[i][0],point[i][1],point[i+1][0],point[i+1][1]):
                    pix[_id].append([j[0],j[1]])
                    All[_id].append(Draw_point(j[0],j[1]))
            Message(window,text='多边形\n'+str(_id)).pack(side=LEFT)

    # drawCurve id n Bezier/B-spline x1 y1 .... xn yn 画曲线
    if cin[:9] == 'drawCurve':
        cin = cin[9:]
        cin = cin.split()
        _id, n = int(cin[0]), int(cin[1])
        how = cin[2] # 选择的绘制算法
        point = [] # 曲线的起点，控制点，终点
        for i in range(n):
            point.append( [ int(cin[i*2+3]), int(cin[i*2+4]) ] )
        todraw = Bezier(point) # 通过Bezier算法计算出所有要连接的点
        L = len(todraw)
        for i in range(L-1):
            canvas.create_line(todraw[i][0],todraw[i][1],todraw[i+1][0],todraw[i+1][1], fill=Color_pen, width=Width_pen) # 这里把计算出来的点依次相连得到曲线,因为画曲线关键是Bezier,所以这里没用自己的画直线函数
        Message(window,text='曲线\n'+str(_id)).pack(side=LEFT)
        

    # translate id dx dy 对图元平移
    if cin[:9] == 'translate':
        cin = cin[9:]
        cin = cin.split()
        _id = int(cin[0]) #图元编号
        dx, dy = float(cin[1]), float(cin[2])
        for i in All[_id]:
            canvas.move(i,dx,dy)
        for i in range(len(All[_id])):
            pix[_id][i][0] += dx
            pix[_id][i][1] += dy

    # rotate id x y r 将图元id绕(x,y)顺时针旋转r°
    if cin[:6] == 'rotate':
        # 注意不能改变原来的颜色
        cin = cin[6:]
        cin = cin.split()
        _id = int(cin[0])
        x0, y0, r = float(cin[1]),float(cin[2]),float(cin[3])
        now = []
        Color_tmp = Color_pen
        Color_pen = Color_list[_id]
        for i in range(len(All[_id])):
            canvas.delete(All[_id][i]) # 删除旧的图元
            draw = rotate(x0,y0,pix[_id][i][0],pix[_id][i][1],r)
            now.append(Draw_point(draw[0], draw[1]))
            pix[_id][i][0] = draw[0]
            pix[_id][i][1] = draw[1]
        All[_id] = now # 更新图元
        Color_pen = Color_tmp

    # scale id x y s 以(x,y)为中心缩放s倍
    if cin[:5] == 'scale':
        cin = cin[5:]
        cin = cin.split()
        _id = int(cin[0])
        x0, y0 = float(cin[1]), float(cin[2]) # 缩放中心
        s = float(cin[3]) # 缩放倍数
        for i in range(len(All[_id])):
            canvas.scale(All[_id][i],x0,y0,s,s)
            #canvas.delete(All[_id][i]) # 删除旧的图元
        
def Execute():
    # 用于执行input.txt文件中的所有命令行文件
    f = open('input.txt','r')
    for i in f:
        i = i[:-1]
        execute(i)
        canvas.update()
    f.close()
    #messagebox.showinfo(title='提示',message='所有命令行执行完毕！')


entry = Entry(window, width=40)
button = Button(window,text='执行上述命令',command=execute)
button1= Button(window,text='执行input.txt中所有命令',command=Execute)
def Delete():
    # 提供输入框
    cin =  entry.get()
    for i in All[int(cin)-1]:
        canvas.delete(i)
    #Message(window,text='椭圆 '+str(ID)).pack(side=LEFT)

def sign(x):
    if x>1:
        return 1
    if x==0:
        return 0
    return -1

def DDA(x1, y1, x2, y2):
    # 运用DDA算法绘制直线
    pointList = []
    L = max(abs(x1-x2), abs(y1-y2))
    dx, dy = (x2-x1)/L, (y2-y1)/L
    x, y = x1+0.5*sign(dx), y1+0.5*sign(dy)
    i = 1
    while i<L:
        pointList.append([x,y])
        x, y = x+dx, y+dy
        i += 1
    return pointList


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

def _Bresenham(x1, y1, x2, y2): 
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

ans = []
def Ellipsepot(x0, y0, x, y):
    # 运用椭圆的4路对称画点
    global ans
    ans.append([x0 + x, y0 + y])
    ans.append([x0 + x, y0 - y])
    ans.append([x0 - x, y0 - y])
    ans.append([x0 - x, y0 + y])

def Draw_ellipse(x0, y0, a, b):
    # 中点圆生成算法画椭圆
    global ans
    ans = []
    rx2 = a*a;
    ry2 = b*b;
    x, y = 0, b
    px, py = 0, 2*rx2*y
    Ellipsepot(x0, y0, x, y);
    p = round( ry2 - rx2*b + 0.25*rx2 )
    while px < py:
        x += 1
        px += 2*ry2
        if p < 0:
            p += ry2 + px
        else:
            y -= 1
            py -= 2*rx2
            p += ry2 + px - py
        Ellipsepot(x0, y0, x, y)
    p = round( ry2*(x+0.5)*(x+0.5) + rx2*(y-1)**2 - rx2*ry2 )    
    while y > 0:
        y -= 1
        py -= 2*rx2
        if p > 0:
            p += rx2 - py
        else:
            x += 1
            px += rx2*2
            p += rx2 - py + px
        Ellipsepot(x0, y0, x, y)
    return ans

# 提前计算一些组合数
C = [1]*10
for i in range(10):
    C[i] = [1]*10
for i in range(2,10):
    for j in range(1,i):
        C[i][j] = C[i-1][j] + C[i-1][j-1]

def Bezier(x): # 运用Bezier算法画曲线，其中x是[[x1,y1],[x2,y2],...]的形式
    point = []
    n = len(x)-1 # 点的数目
    t = 0
    while t<=1:
        X, Y = 0, 0
        for i in range(n+1):
            X += C[n][i]*t**i*(1-t)**(n-i)*x[i][0]
            Y += C[n][i]*t**i*(1-t)**(n-i)*x[i][1]
        point.append([X,Y])
        t+=0.05
    return point

# 鼠标左键单击，允许开始画图
def onLeftDown(event):
    Flag_draw.set(1)
    # 当前单击坐标记录为绘图的初始位置
    X.set(event.x)
    Y.set(event.y)

# 按住鼠标左键，开始画图
def onLeftMove(event):
    global ID
    if not Flag_draw:
        return
    if Type_draw.get() == 1:
        # 绘制直线
        for i in tmp:
            canvas.delete(i)
        for i in Bresenham(X.get(), Y.get(), event.x, event.y):
            tmp.append(Draw_point(i[0],i[1]))
    if Type_draw.get() == 3:
        # 绘制椭圆
        for i in tmp:
            canvas.delete(i)
        for i in Draw_ellipse(X.get(), Y.get(), event.x, event.y):
            tmp.append(Draw_point(i[0],i[1]))
         
    
# 松开鼠标左键,停止画图
def onLeftUp(event):
    Flag_draw.set(0)
    global ID,_id, tmp
    if Type_draw.get() == 2:
        # 打印出点的坐标
        All.append([])
        All[ID].append(Draw_point(event.x,event.y))
        ID += 1

    if Type_draw.get() == 1:
        # 绘制直线，此直线要添加到容器中
        All.append([])
        for i in tmp:
            canvas.delete(i)
        for i in Bresenham(X.get(), Y.get(), event.x, event.y):
            All[ID].append(Draw_point(i[0],i[1]))
            pix[ID].append( [i[0],i[1]] )
        ID += 1
        Message(window,text='直线 '+str(ID-1)).pack(side=LEFT)
        #Operate_menu.add_command(label='直线'+str(ID),command=Delete(_id))

    if Type_draw.get() == 3:
        # 绘制椭圆
        All.append([])
        for i in tmp:
            canvas.delete(i)
        for i in Draw_ellipse(X.get(), Y.get(), event.x, event.y):
            All[ID].append(Draw_point(i[0],i[1]))
            pix[ID].append( [i[0],i[1]] )
        ID += 1
        Message(window,text='椭圆 '+str(ID-1)).pack(side=LEFT)
        #messagebox.showinfo(title='warning',message='该椭圆ID:'+str(ID))
    
    Flag_draw.set(0)    
    tmp = []


canvas.bind('<Button-1>',onLeftDown) # 绑定"单击鼠标左键"的事件
canvas.bind('<B1-Motion>',onLeftMove) # 绑定"按住鼠标左键"的事件
canvas.bind('<ButtonRelease-1>',onLeftUp) # 绑定"松开鼠标左键"的事件
canvas.pack(fill=BOTH, expand=YES)
entry.pack()
button.pack()
button1.pack()
window.config(menu=menu)
window.mainloop()
