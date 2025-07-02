echo 自动安装模块脚本
pause
echo 更新pip...
python -m pip install --upgrade pip
echo 设置清华源为默认镜像...
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
echo 添加信任主机（避免 SSL 错误）...
pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
echo 安装模块中...
pip install csv
pip install openpyxl
pip install tkinter
pip install pyautogui
pip install typing
pip install urllib
pip install functools
pip install pathlib
pip install queue
pip install subprocess
pip install configparser
pip install multiprocessing
pip install json
pip install os
pip install sys
pip install requests
pip install threading
pip install getpass
pip install ctypes
pip install toml
pip install time
pip install psutil
pip install platform
pip install pprint
pip install shutil
pip install math
pip install logging
pip install datetime
pip install rich
echo 模块安装完成
pause