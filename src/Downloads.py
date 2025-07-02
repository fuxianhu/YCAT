"""

多线程下载器

"""



from basic import *
from practicalFunctions import extractFilenameFromUrl


class MultiThreadDownloader:
    """
    ### 多线程下载器
    包含**UI、具体实现**
    """


    def askSave(self):
        """
        ### 询问并保存文件保存路径
        """
        url = self.url_entry.get()
        if url != '':
            save_path = asksaveasfilename(
                initialfile=extractFilenameFromUrl(url),
                filetypes=[("All files", "*.*"), ("Text file", "*.txt")],
            )
            if save_path:
                self.save_path = save_path  # 将选择的路径保存为实例变量


    def __init__(self, root):
        """
        ### 基础界面
        """

        self.root = root
        self.root.title(lang['downloader_title'])
        self.root.geometry("600x300")
        
        self.askSaveBtn = Button(self.root, text=lang['select_save_path'], command=self.askSave)
        self.askSaveBtn.pack(pady=(10, 0))

        # 下载链接输入
        self.url_label = Label(self.root, text=lang['download_link'])
        self.url_label.pack(pady=(10, 0))
        
        self.url_entry = Entry(self.root, width=60)
        self.url_entry.pack(pady=(0, 10))
        
        # 线程数选择
        self.thread_label = Label(self.root, text=lang['number_of_threads'])
        self.thread_label.pack()
        
        self.thread_entry = Entry(self.root, width=10)
        self.thread_entry.insert(0, "64")  # 默认64线程
        self.thread_entry.pack()
        
        # 下载按钮
        self.download_button = Button(self.root, text=lang['start_downloading'], command=self.start_download)
        self.download_button.pack(pady=(10, 10))
        
        # 进度条框架
        self.progress_frame = Frame(self.root)
        self.progress_frame.pack(fill="x", padx=20, pady=(10, 0))
        
        # 进度条
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient="horizontal", length=500, mode="determinate")
        self.progress_bar.pack()
        
        # 进度百分比
        self.progress_var = StringVar()
        self.progress_var.set("0%")
        self.progress_label = Label(self.root, textvariable=self.progress_var)
        self.progress_label.pack(pady=(5, 0))
        
        # 状态信息
        self.status_var = StringVar()
        self.status_label = Label(self.root, textvariable=self.status_var, fg="blue")
        self.status_label.pack(pady=(10, 0))
        
        # 下载相关变量
        self.downloading = False
        self.file_size = 0
        self.downloaded = 0
        self.threads = []
    
    def start_download(self):
        """
        ### 检查并开始下载
        """
        if self.downloading:
            self.status_var.set(lang['it_is_already_being_downloaded'])
            return
        
        url = self.url_entry.get().strip()
        if not url:
            self.status_var.set(lang['enter_the_download_link'])
            return
        
        try:
            thread_num = int(self.thread_entry.get())
            if thread_num <= 0:
                raise ValueError
        except ValueError:
            self.status_var.set(lang['number_of_threads_must_be_a_positive_integer'])
            return
        
        self.downloading = True
        self.download_button.config(state="disabled")
        self.status_var.set(lang['getting_file_information'])
        
        # 在新线程中开始下载
        threading.Thread(target=self.prepare_download, args=(url, thread_num), daemon=True).start()
    

    def prepare_download(self, url, thread_num):
        try:
            # 获取文件大小
            response = requests.head(url, allow_redirects=True)
            if response.status_code != 200:
                raise Exception(f"{lang['http_error']}{response.status_code}")
            
            self.file_size = int(response.headers.get('content-length', 0))
            if self.file_size == 0:
                raise Exception(lang['unable_to_retrieve_file_size'])
            
            # 解析文件名
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = "downloaded_file"
            
            if self.file_size < 1024:
                size = f"{self.file_size} Byte"
            elif self.file_size < 1048576:
                size = f"{self.file_size/1024:.2f} KB"
            elif self.file_size < 1073741824:
                size = f"{self.file_size/1048576:.2f} MB"
            else:
                size = f"{self.file_size/1073741824:.2f} GB"
            self.status_var.set(f"{lang['preparing_to_download']}{filename} ({lang['size']}{size})")
            
            # 计算每个线程下载的字节范围
            chunk_size = ceil(self.file_size / thread_num)
            ranges = []
            for i in range(thread_num):
                start = i * chunk_size
                end = start + chunk_size - 1
                if end >= self.file_size:
                    end = self.file_size - 1
                ranges.append((start, end))
            
            # 初始化下载状态
            self.downloaded = 0
            self.progress_bar["value"] = 0
            self.progress_var.set("0%")
            
            # 创建临时文件
            self.temp_files = []
            for i in range(thread_num):
                temp_file = f"{filename}.part{i}"
                self.temp_files.append(temp_file)
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            # 启动下载线程
            self.threads = []
            for i in range(thread_num):
                start, end = ranges[i]
                thread = threading.Thread(
                    target=self.download_chunk,
                    args=(url, i, start, end, self.temp_files[i]),
                    daemon=True
                )
                self.threads.append(thread)
                thread.start()
            
            # 启动进度更新线程
            threading.Thread(target=self.update_progress, args=(filename,), daemon=True).start()
            
        except Exception as e:
            self.status_var.set(f"{lang['error']}{str(e)}")
            self.reset_download_state()
    
    def download_chunk(self, url, thread_id, start, end, temp_file):
        """
        ### 下载线程
        """
        try:
            headers = {'Range': f'bytes={start}-{end}'}
            response = requests.get(url, headers=headers, stream=True)
            
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if not self.downloading:
                        break
                    if chunk:
                        f.write(chunk)
                        with threading.Lock():
                            self.downloaded += len(chunk)
        
        except Exception as e:
            print(f"{lang['thread']}{thread_id} {lang['error']}{str(e)}")
    
    def update_progress(self, filename):
        """
        ### 下载进度更新线程
        """
        while self.downloading and self.downloaded < self.file_size:
            progress = (self.downloaded / self.file_size) * 100
            self.progress_bar["value"] = progress
            self.progress_var.set(f"{progress:.1f}%")
            self.root.update()
            
            # 检查所有线程是否完成
            if all(not thread.is_alive() for thread in self.threads):
                break
            
            threading.Event().wait(0.1)
        
        if self.downloaded >= self.file_size:
            self.merge_files(filename)
            self.status_var.set(f"{lang['download_completed']}{filename}")
        else:
            self.status_var.set(lang['download_stopped'])
        
        self.reset_download_state()
    
    def merge_files(self, filename):
        """
        ### 保存下载完的文件
        合并文件，将多个文件合并为一个文件
        """
        try:
            # 优先使用用户选择的保存路径
            final_path = self.save_path if self.save_path else filename
            with open(final_path, 'wb') as outfile:
                for temp_file in self.temp_files:
                    with open(temp_file, 'rb') as infile:
                        outfile.write(infile.read())
                    os.remove(temp_file)
            
            self.progress_bar["value"] = 100
            self.progress_var.set("100%")
            
        except Exception as e:
            self.status_var.set(f"{lang['merge_file_error']}{str(e)}")
    
    def reset_download_state(self):
        """
        ### 重新设置下载状态
        """
        self.downloading = False
        self.download_button.config(state="normal")
        self.threads = []