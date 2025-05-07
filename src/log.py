from rich.console import Console
console = Console()

import logging
from tkinter.messagebox import *
import datetime


def log(
        type=logging.DEBUG,
        text="Log text",
        popup=None,           # 弹出窗口
        popup_title=None,     # 弹出窗口标题
        popup_text=None,      # 弹出窗口文本内容
        write_file=True,      # 写入日志文件，不允许为Node
        output_console=True, # 是否输出至控制台
):
    """
    增加日志，也可以同时弹出窗口。

    参数解释：
        type: 日志类型，整型。
              但建议使用logging中的
              CRITICAL、FATAL、ERROR、WARNING、WARN、INFO、DEBUG、NOTSET等常量，
              默认值为logging.DEBUG。
        text: 日志文本，字符串。
              默认值为"Log text",
        popup: 是否弹出窗口，空值或布尔值。
               如果为否，则不弹出并忽略popup_title、popup_text参数。
               默认值为None，只要type参数是或者比logging.WARNING高的，自动设置为True，否则自动设置为False。
        popup_title: 弹出窗口标题，空值或字符串。
                     默认为None，会自动设置为该错误级别的名称（如：警告、错误等）。
        popup_text: 弹出窗口文本内容，空值或字符串。
                     默认为None，会自动设置为text参数的内容。
    """
    if popup == None:
        if type >= logging.WARNING:
            popup = True
        else:
            popup = False

    def poput_function(text_num, poput_bool):
        # 处理未指定标题、文本、是否弹出窗口
        r_popup_title = None
        r_popup_text = None
        if popup_title == None:
            text_list = (None, "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
            r_popup_title = text_list[text_num]
        if popup_text == None:
            r_popup_text = text
        if popup == None:
            popup == poput_bool
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
                showinfo(r_popup_title, r_popup_text)
            elif type == logging.WARNING:
                showwarning(r_popup_title,r_popup_text)
            elif type == logging.ERROR or type == logging.CRITICAL:
                showerror(r_popup_title, r_popup_text)


    if type == logging.DEBUG:
        if write_file:
            logging.debug(text)
        poput_function(1, False)

    elif type == logging.INFO:
        if write_file:
            logging.info(text)
        poput_function(2, False)

    elif type == logging.WARNING:
        if write_file:
            logging.warning(text)
        poput_function(3, True)

    elif type == logging.ERROR:
        if write_file:
            logging.error(text)
        poput_function(4, True)

    elif type == logging.CRITICAL:
        if write_file:
            logging.critical(text)
        poput_function(5, True)

    else:
        # 参数错误
        logging.error(text)
        poput_function(4, True)