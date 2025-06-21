import os
import subprocess
import time
import psutil

# 确保工作目录为当前脚本所在的目录：
script_path = os.path.abspath(__file__) # 获取当前脚本文件的绝对路径
script_dir = os.path.dirname(script_path) # 获取脚本所在目录
os.chdir(script_dir) # 设置工作目录

def kill_program_a():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'python.exe' or proc.info['name'] == 'python3':
            cmdline = proc.cmdline()
            if len(cmdline) > 1 and 'Ycat.py' in cmdline[1]:
                try:
                    print(f"正在终止程序A (PID: {proc.pid})...")
                    proc.terminate()
                    proc.wait(timeout=5)
                    print("程序A已终止")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                    pass
                return

def delete_folder(folder_path):
    try:
        if os.path.exists(folder_path):
            print(f"正在删除文件夹: {folder_path}")
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(folder_path)
            print("文件夹已删除")
        else:
            print(f"文件夹 {folder_path} 不存在")
    except Exception as e:
        print(f"删除文件夹时出错: {e}")

def main():
    print("程序B已启动")
    
    # 要删除的文件夹路径
    folder_to_delete = "../log/"
    
    # 1. 关闭程序A
    kill_program_a()
    
    # 2. 删除指定文件夹
    delete_folder(folder_to_delete)
    
    # 3. 重新打开程序A
    print("正在重新启动程序A...")
    subprocess.Popen(['python', './Ycat.py'])
    print("程序A已重新启动，程序B将退出")
    
    # 给程序A时间启动
    time.sleep(2)


main()