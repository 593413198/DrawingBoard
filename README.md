## python+tkinter实现简易画板

**创建时间：**
`2019/5/10`

**搭建环境：**
`Ubuntu 18.04 + python 3.6 + tkinter`

**待实现功能：**
- 重置画布 resetCanvas width height
- 保存画布 saveCanvas name.bmp
- 设置画笔颜色 setColor R G B
- 设置画笔粗细 setWidth width
- 绘制线段 drawLine id x1 y1 x2 y2 algorithm
  - Bresenham
  - DDA
- 绘制椭圆 drawEllipse id x y rx ry
  - 中点圆生成算法
-

**代码架构：**
- 引入第三方库
```python
from tkinter import *
import tkinter.messagebox as messagebox # 弹窗
import pyscreenshot as ImageGrab # 截图功能 for linux
#from PIL import ImageGrab # 截图功能 for MacOS and Windows
```

- 窗口及菜单
```python
window = Tk()  # 主窗口window
canvas = Canvas(window, ...) # 主画布canvas
menu = Menu(windows) # 主菜单menu
```

- 全局变量
```python
Type_draw # 记录画图的类型  1:直线 2:点 3:椭圆
Flag_draw # 记录是否允许画图  0:不允许 1:允许
Color_pen # 画笔颜色 采用16进制表示
Width_pen # 画笔粗细
``` 

- 鼠标事件
```python
onLeftDown()  # 鼠标左键单击，允许开始画图
onLeftMove()  # 鼠标左键拖动，开始画图
onLeftUp()    # 鼠标左键松开，停止画图
```

- 绘图算法
```python
Bresenham() # bresenham算法画直线
Draw_ellipse() # 中点圆生成算法画椭圆
```