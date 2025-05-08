from basic import *


class MultiThreadDownloader:
    def __init__(self, url: str, save_path: str, thread_num:int = 8):
        self.output_arr = []
        self.url = url
        self.thread_num = thread_num
        self.file_size = 0
        # 请求头设置
        self.headers = downloadsConfig["Headers"]
        self.progress = 0
        self.lock = threading.Lock()

        # 解析URL获取文件名
        parsed_url = urlparse(url)
        filename = unquote(parsed_url.path.split('/')[-1])
        if not filename:
            filename = "download.bin"

        # 处理保存路径
        save_path = save_path.strip()
        original_path = Path(save_path)
        
        # 判断是否是目录（以分隔符结尾或已存在的目录）
        if save_path.endswith(('/', '\\')) or (original_path.exists() and original_path.is_dir()):
            self.save_path = original_path / filename
        else:
            self.save_path = original_path

        # 确保父目录存在
        self.save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 临时文件目录
        self.temp_dir = self.save_path.parent / f"{self.save_path.name}_temp"
        self.temp_dir.mkdir(exist_ok=True)

    def getFileInfo(self):
        """获取文件大小和是否支持断点续传"""
        try:
            with requests.head(self.url, headers=self.headers, allow_redirects=True) as r:
                if 'Content-Length' in r.headers:
                    self.file_size = int(r.headers['Content-Length'])
                return 'Accept-Ranges' in r.headers
        except Exception as e:
            self.output_arr += f"{lang['failed_to_connect_to_server']} {str(e)}"
            return False

    def downloadRange(self, start : int, end : int, part_id : int):
        """下载指定范围的数据块"""
        headers = self.headers.copy()
        headers['Range'] = f'bytes={start}-{end}'
        
        max_retries = 3
        for _ in range(max_retries):
            try:
                with requests.get(self.url, headers=headers, stream=True, timeout=10) as r:
                    r.raise_for_status()
                    temp_file = self.temp_dir / f"part_{part_id}"
                    with open(temp_file, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024*1024):
                            if chunk:
                                f.write(chunk)
                                with self.lock:
                                    self.progress += len(chunk)
                return True
            except Exception as e:
                self.output_arr += f"{lang['partition_download_failed_1']} {part_id} {lang['partition_download_failed_2']}"
        return False

    def mergeFiles(self):
        """合并临时分块文件"""
        # 确保目标文件存在并清空内容
        with open(self.save_path, 'wb') as f:
            pass
            
        with open(self.save_path, 'ab') as f:
            for part_id in range(self.thread_num):
                temp_file = self.temp_dir / f"part_{part_id}"
                if temp_file.exists():
                    with open(temp_file, 'rb') as part:
                        f.write(part.read())
                    temp_file.unlink()

    def start(self):
        """启动下载任务"""
        if not self.getFileInfo():
            self.output_arr += lang['server_not_support']
            self.thread_num = 1

        if self.file_size == 0:
            self.output_arr += lang['unable_get_file_size']
            self.thread_num = 1

        # 删除已存在的目标文件
        if self.save_path.exists():
            self.save_path.unlink()

        # 计算分块大小
        chunk_size = self.file_size // self.thread_num
        threads = []
        q = Queue()

        # 创建并启动下载线程
        for i in range(self.thread_num):
            start = i * chunk_size
            end = start + chunk_size - 1 if i < self.thread_num -1 else self.file_size -1
            t = threading.Thread(target=lambda: q.put(self.downloadRange(start, end, i)))
            t.start()
            threads.append(t)

        # 显示进度条
        self.showProgress()

        # 等待所有线程完成
        for t in threads:
            t.join()

        # 合并文件
        if all(q.get() for _ in range(self.thread_num)):
            self.mergeFiles()
            self.temp_dir.rmdir()
            self.output_arr += f"\n{lang['download_completed']}{self.save_path}"
        else:
            self.output_arr += f"\n{lang['download_failed']}"

    def showProgress(self):
        """显示下载进度条"""
        if self.file_size == 0:
            return
        
        # while self.progress < self.file_size:
        #     percent = self.progress / self.file_size * 100
        #     bar = '■' * int(percent // 2) + ' ' * (50 - int(percent // 2))
        #     print(f"\r[{bar}] {percent:.1f}%", end='', flush=True)
        #     threading.Event().wait(0.5)
        # print()

    def enter(self, url : str, save_path : str):
        # 用户输入
        # url = input("请输入下载地址：").strip()
        # save_path = input("请输入保存路径（文件/目录，为空则自动保存至用户桌面）：").strip()
        if save_path == '':
            try:
                save_path = f"C:/Users/{getpass.getuser()}/Desktop/"
            except OSError:
                self.output_arr += lang['no_username']
                return
            except Exception as e:
                self.output_arr += f"{lang['failed_user_desktop_path']} {str(e)}"
                return
        # 创建下载器实例
        downloader = MultiThreadDownloader(
            url=url,
            save_path=save_path,
            thread_num=16
        )
        
        # 开始下载
        downloader.start()


    # def exit_downloads(self, event=None):
    #     pass

