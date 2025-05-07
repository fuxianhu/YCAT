"""
基础
"""

from typing import *
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import tkinter.messagebox

from pathlib import Path
from urllib.parse import urlparse, unquote
from queue import Queue
from log import *
from pathlib import Path
import openpyxl
import json

import os
import sys
import requests
import threading
import getpass
import ctypes

import configparser
import toml

import multiprocessing
import platform
import pprint

VERSION = "0.1.9.20250427_Beta"






# 获取当前脚本的目录 E:\YFY\YCAT\src
folder = Path(__file__).parent.resolve().as_posix()





def ParseJSON(file_path):
    """
    解析JSON文件
    """
    with open(file_path, 'r', encoding='utf-8') as jsonFile:
        return json.load(jsonFile)



jsonSettings = ParseJSON(f'{folder}/config/CatSettings.json')
languageData = ParseJSON(f"{folder}/config/LanguageData.json")
downloadsConfig = ParseJSON(f'{folder}/config/Downloads.json')
if type(downloadsConfig) != dict:
    log(type=logging.CRITICAL, text="YFYCAT: Downloads.json is not a dict.", popup=False)
    raise TypeError("YFYCAT: Downloads.json is not a dict.")


def SaveJSON(data, file_path= f'{folder}/config/CatSettings.json') -> None:
    """
    保存JSON文件
    """
    with open(file_path, 'w', encoding='utf-8') as jsonFile:
        json.dump(data, jsonFile)


if type(jsonSettings) != dict:
    raise TypeError("YFYCAT: data.json is not a dict.")



# 读取语言文件

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

def restartProgram() -> NoReturn:
    """
    重启程序
    """
    if showWarningOkCancel(title=lang['restart_software_warning'], message=lang['restart_software_warning_message']):
        os.execv(sys.executable, ['python'] + sys.argv)