import numpy as np
import matplotlib.pyplot as plt
#
# '''
# x = np.arange(0, 5, 0.1)
# line, = plt.plot(x, x*x) # plot返回一个列表，通过line,获取其第一个元素
# # 调用Line2D对象的set_*方法设置属性值
# line.set_antialiased(False)
# # 同时绘制sin和cos两条曲线，lines是一个有两个Line2D对象的列表
# lines = plt.plot(x, np.sin(x), x, np.cos(x)) #
# # 调用setp函数同时配置多个Line2D对象的多个属性值
# plt.setp(lines, color="r", linewidth=2.0)
# plt.subplot()
# '''
#
# from matplotlib.lines import Line2D
#
# fig = plt.figure()
# line1 = Line2D([0,1],[0,1],transform = fig.transFigure,figure = fig,color='r')
# line2 = Line2D([0,1],[1,0],transform =fig.transFigure,figure = fig, color= "g")
# fig.lines.extend([line1,line2])
# fig.show()


