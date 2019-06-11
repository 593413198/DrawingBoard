
## python+tkinter实现绘图板

**创建时间：**
`2019/5/10`

**搭建环境：**
`Ubuntu 18.04 + python 3.6 + tkinter`

**界面预览：**

![界面预览](https://img-blog.csdnimg.cn/2019061122345931.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2x1aGFvMTk5ODA5MDk=,size_1,color_FFFFFF,t_70)

#### 使用指南
**运行**：linux环境下，make编译运行，执行用户端程序

**用户界面**：见图

**命令行界面**：
- **命令行手动输入**：在界面底部文本框输入指令，点击按钮”**执行上述命令**“执行，一次只能执行一条
- **命令行自动读取并执行**：在图形界面点击按钮“**执行input.txt中所有命令**”，请务必以**input.txt**命名，且多边形和曲线的**点坐标不要换行**
<br/>
<br/>

**已实现功能：**
- 重置画布 resetCanvas width height
- 保存画布 saveCanvas name.bmp
- 设置画笔颜色 setColor R G B
- 绘制线段 drawLine id algorithm x1 y1 x2 y2
 - DDA + Bresenham算法
- 绘制椭圆 drawEllipse id x y rx ry
 - 中点圆算法
- 绘制多边形 drawPolygon id n algorihtm x1 y1 x2 y2 ... xn yn
 - DDA + Bresenham算法
- 绘制曲线　drawCurve id n algorithm x1 y1 ... xn yn
 - Bezier算法
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
Color_list # 存储每个图元的颜色
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
DDA() # DDA算法画直线
Bresenham() # bresenham算法画直线
Draw_ellipse() # 中点圆生成算法画椭圆
```

-  相关函数
```python
toHex() # 将RGB转化成十六进制色彩表示
rotate() # 旋转指定点
execute() # 读入命令行并执行
```

