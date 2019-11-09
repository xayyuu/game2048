
# 文件说明
&emsp;&emsp;game2048.py  # 实现2048游戏的主程序  
&emsp;&emsp;game2048_gui.py  # 实现2048游戏的GUI程序，基于Pygame    
&emsp;&emsp;game2048test.py  # 一些单元测试  

# 原理
&emsp;&emsp;待续

# 运行方式   
有两种方法，分别为：   
1.  
```
cd ~/game2048
chmod +x *
./game2048.py  # or ./game2048_gui.py 使用game2048_gui时,依赖pygame模块,需要通过pip install pygame安装pygame模块.
```
2.  
```
cd ~/game2048
python game2048.py # or python game2048_gui.py
```


# 可优化空间
有几个大的优化方向：
- 用`pygame`模块来写界面这块，效果会比较好。  
  * ~~实现主功能，程序运行良好。~~
  * 撤销功能暂未实现。
  * 棋盘大小设成固定值4,不够灵活，待改进，考虑提供游戏开始选项界面，在其中可以选择不同棋盘大小的游戏。
  * 退出方式不够友好，待改进。
  * 颜色不够丰富，待改进，考虑增加丰富的颜色。
  * 全局变量太多，待改进。
- 用`类`来实现现有的代码逻辑，从中学习面向对象编程的思想。  
- 更全面的测试，发现更好的测试工具（如GUI常用的测试工具）。  

# 附录
### 测试用例
##### 合并一行的测试用例  
8 8 4 4 -->  16 8  0 0  
2 2 4 8 -->  4 4 8 0  
4 4 8 0 -->  8 8 0 0  
16 4 4 2 --> 16 8 2 0  
0  0 4 4 --> 8 0 0 0  
0 4 2 2 --> 4 4 0 0   

### 参考资料       
[一起来写2048(160行python代码)](http://www.tuicool.com/articles/YNzqu2j)
> 注意：  资料中合并操作代码是有bug的。

[RGB颜色查询对照表](http://www.114la.com/other/rgb.htm)


如果有bug，敬请指正！  
# game2048
