import typing
from tkinter import *
from WindowBackground import WindowBackground
from Personalization import Personalization
from basic import *
from cest import CEST
import os
import gc



class Home:
    """
    主页
    初始化实例时自动运行enter()方法
    """

    def __init__(self, win: typing.Union[Tk, Toplevel]) -> None:
        self.open_cest = False
        self.root = win
        self.enter()


    def enter(self) -> None:
        self.root.title(f"{title} - {lang['home']}")
        self.wb = WindowBackground(self.root)
        self.personalization = Personalization(self)
        # wb.setBackgroundImageWithResize()
        self.wb.setBackgroundColor()
        self.personalization_btn = Button(self.root, text=lang['personalization'], command=self.enterPersonalization)
        self.personalization_btn.pack()
        self.cest_btn = Button(self.root, text=lang['cest'], command=self.enterCest)
        self.cest_btn.pack()
        self.root.bind('<Control-p>', self.enterPersonalization)
        self.root.bind('<Control-P>', self.enterPersonalization)
        self.root.bind('<Control-e>', self.enterCest)
        self.root.bind('<Control-E>', self.enterCest)
        
        self.exit_btn = Button(self.root, text=lang['exit'], command=self.exit_cat)
        self.exit_btn.pack()
        self.root.bind('<Escape>', self.exit_cat)


    def enterCest(self, event= None):
        """
        打开CEST
        """
        if self.open_cest:
            showerror(title, lang['no_open_cest'])
        else:
            self.open_cest = True
            self.cest = CEST(home_instance= self)
            del self.cest


    def exit_cat(self, event= None) -> typing.NoReturn:
        """
        退出YFYCAT
        """
        os._exit(0)


    def clear(self) -> None:
        """
        清除所有组件
        """
        self.personalization_btn.destroy()
        self.exit_btn.destroy()
        self.cest_btn.destroy()
        self.root.unbind('<Escape>')
        self.root.unbind('<Control-p>')
        self.root.unbind('<Control-P>')
        self.root.unbind('<Control-e>')
        self.root.unbind('<Control-E>')


    def enterPersonalization(self, event= None) -> None:
        """
        进入个性化设置
        """
        self.clear()
        self.personalization.enter()