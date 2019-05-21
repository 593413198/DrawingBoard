## python+tkinter实现绘图板

**创建时间：**
`2019/5/10`

**搭建环境：**
`Ubuntu 18.04 + python 3.6 + tkinter`

**使用指南：**
![画板界面图片](/example.png)
**上方菜单提供了用户界面的所有操作**
**下方文本框提供了命令行接口，按"执行命令"按钮即可执行指令**
**最底部显示canvas上的所有图元，包括 “类型”+“ID”**

**已实现功能：**
- 重置画布 resetCanvas width height
- 保存画布 saveCanvas name.bmp
- 设置画笔颜色 setColor R G B
- 绘制线段 drawLine id x1 y1 x2 y2 algorithm
- 绘制椭圆 drawEllipse id x y rx ry
- 绘制多边形 drawPolygon id n x1 y1 x2 y2 ... xn yn
- 对图元平移 translate id dx dy
- 对图元旋转 rotate id x y r
- 对图元缩放 scale id x y s

**代码架构：**
- 第三方库
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
menu = Menu(windows) # 顶部主菜单menu
entry = Entry(..) # 接受命令行指令的输入
button = Button(..) # 读入指令并执行
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
Draw_point() # 画点函数
Bresenham() # bresenham算法画直线
Draw_ellipse() # 中点圆生成算法画椭圆
```

-  相关函数
```python
toHex() # 将RGB转化成十六进制色彩表示
rotate() # 旋转指定点
execute() # 读入命令行并执行
```


