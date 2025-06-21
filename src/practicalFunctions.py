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


