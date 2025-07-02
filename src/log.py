# 注意！请勿导入basic.py，否则会出现循环导入的问题。

from rich.console import Console
console = Console()

import logging
from tkinter.messagebox import *
import datetime


def log(
        type: int =logging.DEBUG,
        text: str ="Log text",
        popup: bool | None=None,           # 弹出窗口
        popup_title: str | None=None,     # 弹出窗口标题
        popup_text: str | None=None,      # 弹出窗口文本内容
        write_file: bool=True,      # 写入日志文件
        output_console: bool=True, # 是否输出至控制台
):
    """
    ### 记录日志，也可以同时弹出窗口。

    参数解释：
    - `type`: **日志类型** 建议使用logging中的CRITICAL、FATAL、ERROR、WARNING、WARN、INFO、DEBUG、NOTSET等常量，
    - `text`: **日志文本**，字符串。默认值为"Log text",
    - `popup`: **是否弹出窗口**，空值或布尔值。
               如果为否，则不弹出并忽略popup_title、popup_text参数。
               **如果为`None`，只要`type≥logging.WARNING`时，自动设置为`True`，否则自动设置为`False`**
    - `popup_title`: **弹出窗口标题**
    - `popup_text`: **弹出窗口文本内容**
    - `write_file`: **写入日志文件**
    - `output_console`: **是否输出至控制台**
    """
    if popup == None:
        if type >= logging.WARNING:
            popup = True
        else:
            popup = False
    if popup_title == None:
        popup_title = 'YCAT'
    if popup_text == None:
        popup_text = text

    def poput_function(text_num):
        """
        输出到控制台、弹出窗口
        """

        # 输出到控制台
        if output_console:
            if type == logging.DEBUG:
                console.print(f"[#808080]{datetime.datetime.now()} DEBUG {text}")
            if type == logging.INFO:
                console.print(f"{datetime.datetime.now()} INFO {text}")
            if type == logging.WARNING:
                console.print(f"[#FF8C00]{datetime.datetime.now()} WARNING {text}")
            if type == logging.ERROR:
                console.print(f"[#FF0000]{datetime.datetime.now()} ERROR {text}")
            if type == logging.CRITICAL:
                console.print(f"[#FF00FF]{datetime.datetime.now()} CRITICAL {text}")

        # 弹出窗口
        if popup:
            if type == logging.INFO or type == logging.DEBUG:
                showinfo(popup_title, popup_text)
            elif type == logging.WARNING:
                showwarning(popup_title, popup_text)
            elif type == logging.ERROR or type == logging.CRITICAL:
                showerror(popup_title, popup_text)


    if type == logging.DEBUG:
        if write_file:
            logging.debug(text)
        poput_function(1)

    elif type == logging.INFO:
        if write_file:
            logging.info(text)
        poput_function(2)

    elif type == logging.WARNING:
        if write_file:
            logging.warning(text)
        poput_function(3)

    elif type == logging.ERROR:
        if write_file:
            logging.error(text)
        poput_function(4)

    elif type == logging.CRITICAL:
        if write_file:
            logging.critical(text)
        poput_function(5)

    else:
        # 参数错误
        logging.error(text)
        poput_function(4)