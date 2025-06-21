"""
测试功能暂时不对外开放
"""


from WindowBackground import WindowBackground
from personalization import Personalization
from practicalFunctions import *
from AutoGUI import AutoGUI
from cest import CEST
from basic import *




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
        """ 初始化窗口 """
        self.root.title(f"{title} - {lang['home']}")
        self.wb = WindowBackground(self.root)
        self.personalization = Personalization(self)
        self.autoGUI = AutoGUI(self)
        self.wb.setBackgroundColor()


        """ 创建Button控件并绑定快捷键 """
        self.personalization_btn = Button(self.root, text=lang['personalization'], command=self.enterPersonalization)
        self.personalization_btn.pack()
        self.root.bind('<Control-p>', self.enterPersonalization)
        self.root.bind('<Control-P>', self.enterPersonalization)

        self.autoGUI_btn = Button(self.root, text=lang['auto_gui_button'], command=self.enterAutoGUI)
        self.autoGUI_btn.pack()
        self.root.bind('<Control-g>', self.enterAutoGUI)
        self.root.bind('<Control-G>', self.enterAutoGUI)

        self.exit_btn = Button(self.root, text=lang['exit'], command=self.exit_cat)
        self.exit_btn.pack()
        self.root.bind('<Escape>', self.exit_cat)

        self.godModBtn = Button(self.root, text=lang['god_mod_button'], command=self.openGodMod)
        self.godModBtn.pack()
        self.root.bind('<Control-g>', self.openGodMod)
        self.root.bind('<Control-G>', self.openGodMod)

        self.clearLogBtn = Button(self.root, text=lang['clear_log_button'], command=self.clearLog)
        self.clearLogBtn.pack()
        self.root.bind('<Control-l>', self.clearLog)
        self.root.bind('<Control-L>', self.clearLog)

        """ 菜单 """
        self.mainMenu = Menu(self.root)
        self.root['menu'] = self.mainMenu

        """ 菜单选项 - 设置 """
        # 1. 【获取语言】并【获取/src/language/xx-xx_Settings.json文件】
        self.mnuSettings = Menu(self.mainMenu, tearoff=False)
        self.mainMenu.add_cascade(label="设置", menu=self.mnuSettings)
        settingsJson = getSettingsJson()
        self.mnuSettings.add_command(label=lang['open_settings'], command=lambda: hotkey('win', 'i'))

        # 2. 遍历json文件，使其内容添加到菜单中。
        self.settingsArr = []
        for key, value in settingsJson.items():
            self.settingsArr.append(Menu(self.mnuSettings, tearoff=False))
            head = len(self.settingsArr) - 1
            self.mnuSettings.add_cascade(label=key, menu=self.settingsArr[head])
            for option in value:
                try:
                    self.settingsArr[head].add_command(label=option[0], accelerator=option[1], command=partial(os.system, "start " + option[1]))
                except Exception as e:
                    log(logging.ERROR, popup=False, text=f'{str(e)} | read settingsJson:' + settingsJson, output_console=False)




    def openGodMod(self, event= None):
        """
        打开上帝模式
        访问几乎所有的系统设置和控制面板选项
        """
        os.system('start shell:::{ED7BA470-8E54-465E-825C-99712043E01C}')


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


    def clearLog(self, event= None) -> NoReturn:
        """
        清空日志
        """
        clear_log_folder()