from basic import *

class CEST:
    """
    计算机考试评分工具
    Computer Exam Scoring Tool
    """

    def __init__(self, home_instance):
        self.home_instance = home_instance
        self.win = Toplevel(self.home_instance.root)
        self.win.title(lang['cest_name'])
        self.win.geometry('800x600')
        self.win.iconbitmap(f"{folder}/icon/tool.ico")
        self.winmenu = Menu(self.win)
        self.win['menu'] = self.winmenu
        self.mnu_file = Menu(self.winmenu, tearoff=False)
        self.winmenu.add_cascade(label=lang['file'], menu=self.mnu_file)
        self.mnu_file.add_command(label=lang['exit'], command=self.exit_cest)
        self.mnu_file.add_command(label=lang['import'], command=self.import_file)

        # 绑定窗口关闭事件
        self.win.protocol("WM_DELETE_WINDOW", self.exit_cest)

        self.win.bind('<Escape>', self.exit_cest)
        self.win.mainloop()
        

    def exit_cest(self, event=None):
        self.clear()
        self.home_instance.open_cest = False


    def clear(self):
        """
        清除控件
        """
        self.win.unbind('<Escape>')
        self.win.destroy()


    def import_file(self):
        """
        导入并解析文件、检查文件、计算分数、显示结果、将结果写入Execl里面。
        """
        cwd_folder = os.getcwd()
        
        self.file_path = askopenfilename(title=lang['open_toml'], filetypes=[('TOML', '*.toml')])
        if self.file_path == '':
            return
        
        # Excel
        self.excel_path = asksaveasfilename(title=lang['open_excel_save_folder'], filetypes=[('Excel', '*.xlsx')])
        wb = openpyxl.Workbook()
        ws = wb.active  # 获取默认的工作表
        
        ws['a1'] = "学生姓名"
        ws['b1'] = "总分"

        # 读取 TOML 文件
        with open(self.file_path, 'r', encoding='utf-8') as file:
            config = toml.load(file)

        c = []

        for candidates in config['list_of_candidates']:
            if not os.path.exists(config['examinee_folder'] + candidates + '/'):
                showerror(title, "no this candidate.")
                continue
            os.chdir(config['examinee_folder'] + candidates + '/')
            for check in config['checklist']:
                if check[0] == 'new file' or check[0] == 'new folder':
                    """
                    检测一个文件或文件夹是否存在
                    """
                    if os.path.exists(check[1]):
                        c.append(True)
                elif check[0] == 'check text file content':
                    """
                    检测文本文件，读取文本文件的内容，与参数2进行比较。
                    """
                    if os.path.exists(check[1]):
                        with open(check[1], 'r', encoding='utf-8') as f:
                            if f.read() == check[2]:
                                c.append(True)
                            else:
                                c.append(False)
                    else:
                        c.append(False)
                elif check[0] == 'check file bytes':
                    """
                    检测文件，但是是直接比较两个文件的内容是否一样，处理二进制文件。
                    """
                    if os.path.exists(check[1]):
                        with open(check[1], 'rb') as f1, open(check[2], 'rb') as f2:
                            if f1.read() == f2.read():
                                c.append(True)
                            else:
                                c.append(False)
                    else:
                        c.append(False)
                elif check[0] == 'check file text':
                    """
                    检测文件，但是是直接比较两个文件的内容是否一样，处理文本文件。
                    """
                    if os.path.exists(check[1]):
                        with open(check[1], 'r') as f1, open(check[2], 'r') as f2:
                            if f1.read() == f2.read():
                                c.append(True)
                            else:
                                c.append(False)
                    else:
                        c.append(False)
                elif check[0] == 'file_is_hidden':
                    """检查文件是否隐藏（Windows 系统）"""
                    try:
                        # 获取文件属性
                        attrs = ctypes.windll.kernel32.GetFileAttributesW(check[1])
                        # 检查是否包含隐藏属性
                        # return attrs & 0x2  # 0x2 是隐藏属性的标志
                        if attrs & 0x2:
                            c.append(True)
                        else:
                            c.append(False)
                    except Exception:
                        # return False
                        c.append(False)
                
                else:
                    showerror(title, lang['import_file_error_1'] + 'config["list_of_candidates"]["checklist"][0]')
            # count = 0
            if type(config['score_calculation']) == str:
                exec(f"print({config['score_calculation']})")
            else:
                cnt = 0
                for i in range(len(c)):
                    cnt += config['score_calculation'][i] if c[i] else 0
                print(cnt)
            # print(count)
            c = []
        

        # 恢复原始工作目录，保证其它功能不报错
        os.chdir(cwd_folder)

        wb.save(self.excel_path)  # 保存后将会覆盖原先文件，无提示






