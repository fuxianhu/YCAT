# YFY's comprehensive auxiliary tool
# YCAT

from Home import Home
from basic import *

if __name__ != '__main__':
    os._exit(1)

# （节省内存）垃圾回收功能 
# gc.collect()

# os.system("CLS") # 清屏

def check_environment() -> None:
    """
    环境检测
    包括操作系统、操作系统版本、重要文件等
    """
    # 判断当前操作系统的平台表示
    # 常见的返回值包括：
    # 'linux'：Linux系统
    # 'win32'：Windows系统
    # 'darwin'：macOS系统
    if jsonSettings['Ignore operating system restrictions'] is False:
        os_name = platform.system()
        if os_name == 'Linux':
            NOT_SUPPORTED = """Ycat may not support the current operating system. 
         If you want to forcibly disable operating system restrictions, 
         please bear all the consequences of this modification."""
            """
            翻译：
            Ycat可能不支持当前的操作系统。如果您想强制禁用操作系统限制，请承担此修改带来的所有后果。
            """
            logging.log(level=logging.CRITICAL, msg=f"OS: {os_name}")
            raise OSError(NOT_SUPPORTED)
        elif os_name == 'Darwin':
            logging.log(level=logging.CRITICAL, msg=f"OS: {os_name}")
            raise OSError(NOT_SUPPORTED)
        elif os_name != 'Windows':
            logging.log(level=logging.CRITICAL, msg=f"OS: {os_name}")
            raise OSError(NOT_SUPPORTED)
            # logging.log(f"Ydat对此平台的兼容性未知，请谨慎使用！", level=logging.WARNING)
        else:
            logging.log(level=logging.DEBUG, msg="OS: Windows")
    if jsonSettings['Ignore operating system version restrictions'] is False:
        # 获取操作系统版本信息
        os_version = platform.release() # 返回 str
        logging.log(level=logging.DEBUG, msg=f"OS Version: {os_version}")
        flag = True
        for i in jsonSettings['List of allowed operating system versions']:
            if i == os_version:
                flag = False
                break
        if flag:
            raise OSError("""Ycat may not support this version of the operating system. 
         You can try upgrading or downgrading the operating system, 
         modifying the allowed operating system version list, 
         or disabling the operating system version restrictions. 
         Please bear the consequences of the latter two methods.""")
            """
            翻译：
            Ycat可能不支持此版本的操作系统。您可以尝试升级或降级操作系统，
            修改允许的操作系统版本列表，或禁用操作系统版本限制。请承担后两种方法的后果。
            """



check_environment()


root = Tk()
root.iconbitmap(f"{folder}/icon/tool.ico")
root.geometry(f"{str(jsonSettings['window_x'])}x{str(jsonSettings['window_y'])}")

# 设置窗口透明度
root.attributes("-alpha", jsonSettings['window_alpha'])  # 设置窗口透明度，0.0为完全透明，1.0为不透明

home = Home(root)



root.mainloop()

