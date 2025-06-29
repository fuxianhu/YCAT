"""
基础
"""


import csv
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from tkinter.filedialog import *
from tkinter.messagebox import *
from pyautogui import *
from tkinter import *
from typing import *
from log import *
from urllib.parse import urlparse, unquote
from functools import partial
import tkinter.messagebox
from tkinter.filedialog import *
import tkinter.ttk as ttk
from pathlib import Path
from queue import Queue
import openpyxl
import subprocess
import configparser
import multiprocessing
import json
import os
import sys
import requests
import threading
import getpass
import ctypes
import typing
import toml
import time
import psutil
import platform
import pprint
import shutil
from math import *

"""
VERSION 版本
格式如下：
x.x.x.xxxxxxxx_xxxxxxxxxx
版本  日期      类型
例如：
1.0.0.21000101_RC
"""

VERSION = "0.2.2.20250629_Alpha"



# 获取当前脚本的目录，例如 E:\YFY\YCAT\src
folder = Path(__file__).parent.resolve().as_posix()

# 创建目录
# 添加 exist_ok=True 参数可以避免目录已存在时报错
os.makedirs(f"{os.path.dirname(folder)}/log/", exist_ok=True)

logging.basicConfig(
    filemode="w", 
    filename=f"{os.path.dirname(folder)}/log/Ycat.log", 
    level=logging.DEBUG, 
    format="%(asctime)s (%(name)s) [%(levelname)s] %(message)s"
)


"""
----------解析、检查、保存JSON文件----------
"""

def ParseJSON(filePath: str):
    """
    解析JSON文件
    """
    with open(filePath, 'r', encoding='utf-8') as jsonFile:
        return json.load(jsonFile)


def jsonParseAndCheck(jsonFilePath: str, saveType= dict) -> Any:
    """
    解析并检查其类型的 json 格式文件
    抛出异常或返回对应类型的数据
    类型检查的类型默认为 dict (字典)
    """
    jsonData = ParseJSON(jsonFilePath)
    if type(jsonData) != saveType:
        ERROR_TEXT = f"YFYCAT: {jsonFilePath}.json is not a {str(saveType)}."
        log(type=logging.CRITICAL, text=ERROR_TEXT, popup=False)
        raise TypeError(ERROR_TEXT)
    return jsonData


jsonSettings = jsonParseAndCheck(f'{folder}/config/CatSettings.json')
languageData = jsonParseAndCheck(f"{folder}/config/LanguageData.json")
downloadsConfig = jsonParseAndCheck(f'{folder}/config/Downloads.json')


def SaveJSON(data, file_path= f'{folder}/config/CatSettings.json') -> None:
    """
    保存JSON文件
    """
    with open(file_path, 'w', encoding='utf-8') as jsonFile:
        json.dump(data, jsonFile)


if type(jsonSettings) != dict:
    raise TypeError("YFYCAT: data.json is not a dict.")



"""
----------读取语言文件并确定窗口标题----------
"""

def read_section_to_dict(config_file, section_name, encoding='utf-8') -> dict[str, str]:
    """读取配置文件中的指定节，并返回键值对字典"""
    config = configparser.ConfigParser()
    config.read(config_file, encoding=encoding)  # 指定编码（如UTF-8）
    
    if not config.has_section(section_name):
        raise ValueError(f"Section '{section_name}' not found in config file")
    
    # 将节的所有键值对转为字典
    return dict(config[section_name])




lang = read_section_to_dict(f"{folder}/language/{jsonSettings['language']}.conf", "language")

title = f"{lang['title']} {VERSION}"



"""
----------自定义一个警告窗口，程序自重启功能----------
"""

def showWarningOkCancel(title=None, message=None, **options) -> bool:
    """
    由于 tkinter.messagebox.showwarning() 函数的返回值只会是True，
    为了满足需求，需要自定义一个窗口实现，和 tkinter.messagebox.showwarning() 函数不同的是：
    _type 参数从OK替换成了OKCANCEL
    """
    return tkinter.messagebox.OK == tkinter.messagebox._show(
        title, 
        message, 
        tkinter.messagebox.WARNING, 
        tkinter.messagebox.OKCANCEL, 
        **options
        )

def restartProgram(warning: bool= True) -> NoReturn:
    """
    重启程序
    """
    if warning:
        if showWarningOkCancel(title=lang['restart_software_warning'], message=lang['restart_software_warning_message']):
            os.execv(sys.executable, ['python'] + sys.argv)