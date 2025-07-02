# Ycat
**YFY**'s **C**omprehensive **A**uxiliary **T**ool

**请关注讨论区公告**。若有侵权，请联系删除。

**版本**：`0.2.3.20250702_Beta`

开发时：
- 主文件：`./src/Ycat.py`
- 使用`Python3.x`或更高版本（编写使用`Python 3.12.4`）
- 大多算法或某些程序（如`高速连点器`）为了保证运行效率和速度，使用`ISO C++17`或更新的`C++标准`编写，再让`Python`调用编译好的可执行程序（`exe`），原因是`Python`很慢。
- 编译器需支持`<bits/stdc++.h>`头文件，否则无法正常编译，比如`Dev Cpp`可以正常编译。
- `C++`编译：用`g++`，确保上一条生效，一般使用`-O2`优化，也可以使用`-O3`优化，编译命令示例： 
    ```bash
    g++ -O2 -std=c++17 -o .\x .\x.cpp
    ```
- 程序读写和编写文本文件时，使用`UTF-8`编码，而不是`ANSII`、`GBK`、`GB`、`UTF-16`等，例如：
    ```python
    open(<your_filename>, 'r', encoding='utf-8')
    ```

- 错误可能出现在**控制台或日志文件**

英文单词尽量使用**美式英语**，比如：
| 美式拼写 | 英式拼写 |
| ------- | ------- |
| `color` | `colour` |
| `humor` | `humour` |
| `favor` | `favour` |
| `neighbor` | `neighbour` |
| `labor` | `labour` |
| 其它： |
| `tire` | `tyre` |


### 本项目`驼峰命名法（Camel Case）`与`蛇形命名法（Snake Case）`混用，可能给您带来了不便，敬请谅解，技术债，能用就不要改（狗头