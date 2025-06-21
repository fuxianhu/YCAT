from basic import *


class Personalization:
    def __init__(self, home_instance):
        self.root = home_instance.root
        self.home_instance = home_instance


    def entry_insert(self) -> None:
        """
        预先在输入框中插入默认值
        """
        self.window_alpha_entry.insert(0, str(jsonSettings['window_alpha']))
        self.window_x_entry.insert(0, str(jsonSettings['window_x']))
        self.window_y_entry.insert(0, str(jsonSettings['window_y']))


    def enter(self) -> None:
        """
        进入个性化设置界面
        """
        self.root.title(f'{title} - {lang["personalization"]}')
        self.exit_personalization_btn = Button(self.root, text=lang['return_without_saving_changes'], command=self.exitPersonalization)
        self.window_alpha_label = Label(self.root, text=lang['window_transparency'])
        self.window_alpha_entry = Entry(self.root, width=16)
        self.save_btn = Button(self.root, text=lang['save_all_changes'], command=self.save)
        self.restore_default_settings_btn = Button(self.root, text=lang['restore_default_settings'], command=self.restoreDefaultSettings)
        
        self.window_x_label = Label(self.root, text=lang['window_x'])
        self.window_y_label = Label(self.root, text=lang['window_y'])
        self.window_x_entry = Entry(self.root, width=16)
        self.window_y_entry = Entry(self.root, width=16)

        self.window_alpha_label.place(anchor=NW, x=10, y= 10)
        self.save_btn.place(anchor=S, relx=0.5, rely=1)
        self.window_alpha_entry.place(anchor=NW, x=130, y=10)
        self.exit_personalization_btn.place(anchor=N, relx=0.5)
        self.restore_default_settings_btn.place(anchor=S, relx=0.5, rely=0.93)
        self.window_x_entry.place(anchor=NW, x=100, y= 40)
        self.window_y_entry.place(anchor=NW, x=380, y= 40)
        self.window_x_label.place(anchor=NW, x= 5, y=40)
        self.window_y_label.place(anchor=NW, x= 285, y=40)

        if lang['language'] != 'language':
            s = '(language): '
        else:
            s = ': '
        self.language_label = Label(self.root, text=lang['language'] + s)
        del s
        self.op = StringVar()
        self.op.set(jsonSettings['language_text'])
        self.cmb = ttk.Combobox(self.root, textvariable=self.op)
        self.cmb['values'] = [i[1] for i in languageData['language']]
        self.cmb.place(anchor=NW, x= 5, y= 70)

        self.root.bind('<Control-s>', self.save)
        self.root.bind('<Control-S>', self.save)
        self.root.bind('<Control-r>', self.restoreDefaultSettings)
        self.root.bind('<Control-R>', self.restoreDefaultSettings)
        self.root.bind('<Escape>', self.exitPersonalization)

        self.entry_insert()


    def exitPersonalization(self, event= None) -> None:
        """
        退出个性化设置界面
        """
        self.exit_personalization_btn.destroy()
        self.save_btn.destroy()
        self.window_alpha_entry.destroy()
        self.window_alpha_label.destroy()
        self.restore_default_settings_btn.destroy()
        self.window_x_entry.destroy()
        self.window_x_label.destroy()
        self.window_y_entry.destroy()
        self.window_y_label.destroy()
        self.cmb.destroy()
        self.root.unbind('<Escape>')
        self.root.unbind('<Control-s>')
        self.root.unbind('<Control-S>')
        self.root.unbind('<Control-r>')
        self.root.unbind('<Control-R>')
        del self.op
        self.home_instance.enter()


    def setJsonSettings(self) -> None:
        """
        设置JSON
        """
        try:
            alpha_value = float(self.window_alpha_entry.get())
        except:
            showerror(title, lang['no_float'])
            return
        if alpha_value < 0 or alpha_value > 1:
            showerror(title, lang['no_real_number'])
        else:
            # 设置窗口透明度
            jsonSettings['window_alpha'] = alpha_value
        del alpha_value

        try:
            x_value = int(self.window_x_entry.get())
        except:
            showerror(title, lang['window_x_no_integer'])
            return
        try:
            y_value = int(self.window_y_entry.get())
        except:
            showerror(title, lang['window_y_no_integer'])
            return
        if x_value <= 0:
            showerror(title, lang['window_x_less_than_1'])
            return
        if y_value <= 0:
            showerror(title, lang['window_y_less_than_1'])
            return
        jsonSettings['window_x'] = x_value
        jsonSettings['window_y'] = y_value
        del x_value, y_value

        flag = True
        for i in languageData['language']:
            if i[1] == self.cmb.get():
                jsonSettings['language'] = i[0]
                jsonSettings['language_text'] = i[1]
                flag = False
                break
        
        if flag:
            showerror(title, lang['no_language'])
            return


    def save(self, event= None) -> None:
        """
        保存在个性化设置界面中所做的更改并重启程序
        """
        self.setJsonSettings()

        # 保存JSON配置文件
        SaveJSON(data=jsonSettings, file_path=f'{folder}/config/CatSettings.json')

        restartProgram()


    def restoreDefaultSettings(self, event= None) -> None:
        """
        恢复默认设置并重启
        将CatSettings.json的内容替换为DefaultCatSettings.json的内容
        """

        SaveJSON(data=ParseJSON(f'{folder}/config/DefaultCatSettings.json'), file_path=f'{folder}/config/CatSettings.json')
        restartProgram()