"""
图形用户界面自动化
"""
from basic import *


class AutoGUI():
    """
    ### 鼠标连点（包括GUI）

    左、中、右键
    """
    def __init__(self, home_instance):
        self.home_instance = home_instance

    
    def enter(self):
        self.lb = Label(
            self.home_instance.root,
            text=lang['auto_gui_warning'],
            foreground="red",          # 文本颜色为红色
            font=("黑体", 16, "bold"), # 字体加粗
            relief="solid",           # 边框样式（solid, raised, sunken, groove, ridge）
            # borderwidth=10,           # 边框宽度
        )
        self.lb.pack()

        self.acFm = Frame(self.home_instance.root)
        self.acFm.pack()

        self.keyVar = StringVar()
        self.keyVar.set("左键")
        self.keyOm = OptionMenu(self.acFm, self.keyVar, "左键", "中键", "右键")
        self.keyOm.pack(side=LEFT, ipadx=5)
    


        def on_entry_change(*args):
            try:
                value = int(self.acSpeedEntryVar.get())
                if self.acSpeedSlider['from'] <= value <= self.acSpeedSlider['to']:
                    self.acSpeedSlider.set(value)
            except ValueError:
                pass

        # 创建StringVar变量
        self.acSpeedEntryVar = StringVar()

        # 设置trace，当变量值改变时调用回调函数
        self.acSpeedEntryVar.trace_add('write', on_entry_change)

        # 创建滑块
        self.acSpeedSlider = ttk.Scale(self.acFm, from_=0, to=1000, orient='horizontal')
        self.acSpeedSlider.pack(side=LEFT, ipadx=5)

        # 创建Entry并绑定变量
        self.acSpeedEntry = ttk.Entry(self.acFm, textvariable=self.acSpeedEntryVar)
        self.acSpeedEntry.insert(0, '0')
        
        self.acSpeedEntry.pack(side=LEFT, ipadx=5)

        # 滑块变化时更新Entry内容
        def on_acSpeedSliderChange(val):
            self.acSpeedEntryVar.set(int(float(val)))

        self.acSpeedSlider.configure(command=on_acSpeedSliderChange)
        



        self.acBtn = Button(self.acFm, text=lang['start_ac'], command=self.startAC)
        self.acBtn.pack(side=LEFT)
        self.acProgram = None

        self.exitBtn = Button(self.home_instance.root, text=lang['exit'], command=self.exitAutoClick)
        self.exitBtn.pack()
        self.home_instance.root.bind('<Escape>', self.exitAutoClick)


    def startAC(self):
        """
        ### 开始自动点击
        """
        if self.acProgram is not None:
            self.acProgram.terminate()
        
        k = ''
        if self.keyVar.get() == '左键':
            k = 'left'
        elif self.keyVar.get() == '中建':
            k = 'middle'
        elif self.keyVar.get() == '右键':
            k = 'right'
        self.acProgram = subprocess.Popen(["./AutoClick.exe", self.acSpeedEntry.get(), k], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         creationflags=subprocess.CREATE_NO_WINDOW
                         )


    def exitAutoClick(self, event= None):
        """
        ### 退出
        """
        self.home_instance.root.unbind('<Escape>')
        self.acFm.destroy()
        self.exitBtn.destroy()
        self.lb.destroy()
        self.home_instance.enter()



