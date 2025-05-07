:: C++程序编译
:: 确保不乱码
:: ./compile.bat
chcp 65001
echo C++程序编译脚本
g++ --version
cd src
echo 请确认当前目录在src目录下，且g++在PATH环境变量中！否则请结束脚本运行。
pause
echo 开始编译
g++ -std=c++17 -o .\algorithm .\algorithm.cpp
echo 编译进度 1/1
echo 编译完成
pause
:: 清除python的cache： del /Q __pycache__