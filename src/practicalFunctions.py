"""
一些小规模的实用功能
"""

from basic import *

# # 命令、程序
# functions = [
#     {
#         "name": "（远程）关机等",
#         "command": "shutdown.exe /i"
#     },

# ]
def getSettingsJson() -> dict | int:
    """
    获取与设置相关的JSON文件数据
    """
    f = None
    try:
        f = ParseJSON(f"{folder}/language/{jsonSettings['language']}_Settings.json")
    except FileNotFoundError as err:
        log(logging.ERROR, f"找不到'{jsonSettings['language']}_Setting.json'文件，正在尝试使用zh-CN语言...", popup=False)
    except Exception as err:
        log(logging.ERROR, f"无法读取'{jsonSettings['language']}_Setting.json'文件，正在尝试使用zh-CN语言...", popup=False)

    if f == None:
        try:
            f = open(f"{folder}/language/zh-CN_Settings.json", "r")
        except FileNotFoundError as err:
            log(logging.ERROR, f"找不到'zh-CN_Setting.json'文件，无法显示文本。", popup=False)
        except Exception as err:
            log(logging.ERROR, f"无法读取'zh-CN_Setting.json'文件，无法显示文本。", popup=False)
    else:
        return f
    return -1



def is_program_b_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'python.exe' or proc.info['name'] == 'python3':
            cmdline = proc.cmdline()
            if len(cmdline) > 1 and 'clearLog.py' in cmdline[1]:
                return proc.pid
    return None

def clear_log_folder() -> NoReturn:
    # 检查程序B是否在运行
    pid = is_program_b_running()
    if pid:
        print("检测到程序B正在运行，正在终止它...")
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=5)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            pass
        print("程序B已终止，程序A退出。")
        return
    
    print("程序A已启动，输入任意内容将启动程序B...")
    input_str = input("请输入: ")
    
    if input_str:
        print("正在启动程序B...")
        subprocess.Popen(['python', 'clearLog.py'])
        print("程序B已启动，程序A将等待被关闭...")
        
        # 等待程序B关闭自己
        while True:
            time.sleep(3600)