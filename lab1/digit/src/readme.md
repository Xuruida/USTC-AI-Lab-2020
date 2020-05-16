# Digit Problem

## A* 算法

- **digitAstar_initial.cpp**: 最初的版本，线性查重无优化。

- **digitAstar_departed.cpp**: 仍然线性查重，但是为测试集三加入了特定的优化（分成两步），可以跑出小于100步的解。

- **digitAstar_unordered_set.cpp**: 使用STL unordered set，利用内置hash结构进行查找优化。

```shell
make initial # 生成初始源代码对应的可执行程序
make departed # 生成第一次优化后的程序
make uos # 生成个第二次优化后的程序

make     # 生成所有程序

sh ./run.sh   # 编译运行第二次优化后的 A* 算法程序，并输入测试三(3.txt)
```

编译后生成的可执行程序有一个参数name，该参数指定了input文件夹中输入文件名。

例：
```shell
./digitAstar_initial.out 1.txt # 利用1.txt作为输入
```

程序输入为初始状态矩阵，运行过程中每次找到最小的启发函数或当前节点(Index % 100000 == 0)时输出一次当前节点状态。

找到第一个结束时给出序列，程序停止运行。