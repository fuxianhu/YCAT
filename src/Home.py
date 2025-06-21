"""
测试功能暂时不对外开放
"""

import typing
from tkinter import *
from WindowBackground import WindowBackground
from personalization import Personalization
from basic import *
from cest import CEST
import os
import gc
from practicalFunctions import *
from AutoGUI import AutoGUI



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
        self.autoGUI = AutoGUI(self)
        # wb.setBackgroundImageWithResize()
        self.wb.setBackgroundColor()
        self.personalization_btn = Button(self.root, text=lang['personalization'], command=self.enterPersonalization)
        self.personalization_btn.pack()

        self.autoGUI_btn = Button(self.root, text=lang['auto_gui_button'], command=self.enterAutoGUI)
        self.autoGUI_btn.pack()
        self.root.bind('<Control-g>', self.enterAutoGUI)
        self.root.bind('<Control-G>', self.enterAutoGUI)

        # self.cest_btn = Button(self.root, text=lang['cest'], command=self.enterCest)
        # self.cest_btn.pack()
        self.root.bind('<Control-p>', self.enterPersonalization)
        self.root.bind('<Control-P>', self.enterPersonalization)
        # self.root.bind('<Control-e>', self.enterCest)
        # self.root.bind('<Control-E>', self.enterCest)
        
        self.exit_btn = Button(self.root, text=lang['exit'], command=self.exit_cat)
        self.exit_btn.pack()
        self.root.bind('<Escape>', self.exit_cat)

        self.mainMenu = Menu(self.root)
        self.root['menu'] = self.mainMenu
        self.mnuSettings = Menu(self.mainMenu, tearoff=False)
        self.mainMenu.add_cascade(label="设置", menu=self.mnuSettings)
        settingsJson = getSettingsJson()
        self.settingsArr = []
        # self.settings2Arr = []
        # log(type=logging.INFO, text=settingsJson)
        for key, value in settingsJson.items():
            self.settingsArr.append(Menu(self.mnuSettings, tearoff=False))
            head = len(self.settingsArr) - 1
            self.mnuSettings.add_cascade(label=key, menu=self.settingsArr[head])
            # self.mnuSettings.add_cascade(self.settingsArr[head])
            for option in value:

                self.settingsArr[head].add_command(label=option[0], accelerator=option[2], command=partial(os.system, "start " + option[1]))
        


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
        # self.cest_btn.destroy()
        self.root.unbind('<Escape>')
        self.root.unbind('<Control-p>')
        self.root.unbind('<Control-P>')
        self.root.unbind('<Control-g>')
        self.root.unbind('<Control-G>')
        self.mainMenu.destroy()
        self.autoGUI_btn.destroy()


    def enterPersonalization(self, event= None) -> None:
        """
        进入个性化设置
        """
        self.clear()
        self.personalization.enter()


    def enterAutoGUI(self, event= None) -> None:
        """
        打开连点器
        """
        self.clear()
        self.autoGUI.enter()