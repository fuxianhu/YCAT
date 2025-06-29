"""
实用功能 函数、类的定义
"""

from basic import *



def getSettingsJson() -> dict | int:
    """
    获取与设置相关的JSON文件数据
    """
    f = None
    try:
        f = ParseJSON(f"{folder}/language/{jsonSettings['language']}_Settings.json")
    except FileNotFoundError as err:
        log({lang['clear_log_error']}, f"找不到'{jsonSettings['language']}_Setting.json'文件，正在尝试使用zh-CN语言...", popup=False)
    except Exception as err:
        log({lang['clear_log_error']}, f"无法读取'{jsonSettings['language']}_Setting.json'文件，正在尝试使用zh-CN语言...", popup=False)

    if f == None:
        try:
            f = open(f"{folder}/language/zh-CN_Settings.json", "r")
        except FileNotFoundError as err:
            log({lang['clear_log_error']}, f"找不到'zh-CN_Setting.json'文件，无法显示文本。", popup=False)
        except Exception as err:
            log({lang['clear_log_error']}, f"无法读取'zh-CN_Setting.json'文件，无法显示文本。", popup=False)
    else:
        return f
    return -1



def is_program_b_running() -> int | None:
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'python.exe' or proc.info['name'] == 'python3':
            cmdline = proc.cmdline()
            if len(cmdline) > 1 and 'clearLog.py' in cmdline[1]:
                return proc.pid
    return None

def clear_log_folder() -> NoReturn | None:
    """
    删除日志目录以释放磁盘空间
    
    1. 警告用户其风险
    2. **正确关闭logging handlers**
    3. **删除日志目录**
    4. **重启程序**
    """
    if not showWarningOkCancel(lang['clear_log_warning_title'], lang['clear_log_warning_message']):
        return
    # 1. 正确关闭logging handlers
    logger = logging.getLogger() # 获取root logger
    for handler in logger.handlers[:]: # 关闭并移除所有handlers
        handler.close()
        logger.removeHandler(handler)

    # 2. 删除日志目录
    LOG_FOLDER = '../log'
    try:
        shutil.rmtree(LOG_FOLDER)
    except FileNotFoundError as e:
        showerror({lang['clear_log_error']}, f"Exception: FileNotFoundError: File: {LOG_FOLDER} Error: {e}")
    except PermissionError as e:
        showerror({lang['clear_log_error']}, f"Exception: PermissionError: File: {LOG_FOLDER} Error: {e}")
    except OSError as e:
        showerror({lang['clear_log_error']}, f"Exception: OSError: File: {LOG_FOLDER} Error: {e}")
    except Exception as e:
        showerror({lang['clear_log_error']}, f"Exception: Other Exception: File: {LOG_FOLDER} Error: {e}")
    else:

        # 3. 重启程序
        restartProgram(warning=False)


def extractFilenameFromUrl(url: str) -> str:
    """
    ### 获取URL中的文件名
    解析URL并返回文件名或空字符串 ''
    """
    # 解析 URL 获取路径部分
    parsed_url = urlparse(url)
    path = parsed_url.path  # 获取路径部分，如 '/xxx/xxx.png'
    
    # 使用 os.path.basename 提取文件名
    filename = os.path.basename(path)
    
    return filename



####################  Minecraft 材料列表处理  ###################




def auto_adjust_column_width(ws):
    """
    ### 自动调整表格列宽
    """

    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # 获取列字母
        
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        
        adjusted_width = (max_length + 2) * 2.0  # 加一些边距
        ws.column_dimensions[column].width = adjusted_width


def beautify_excel(ws):
    """
    ### 美化Excel表格
    """

    # 设置默认字体
    ws.font = Font(name='微软雅黑', size=11)
    
    # 设置标题行样式
    header_font = Font(bold=True, color='FFFFFF', size=12)
    header_fill = PatternFill(start_color='4F81BD', end_color='4F81BD', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center')
    
    # 设置数据行样式
    data_font = Font(size=11)
    data_alignment = Alignment(horizontal='left', vertical='center')
    border = Border(left=Side(border_style='thin', color='000000'),
                   right=Side(border_style='thin', color='000000'),
                   top=Side(border_style='thin', color='000000'),
                   bottom=Side(border_style='thin', color='000000'))
    
    # 应用标题行样式
    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border
    
    # 应用数据行样式
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font = data_font
            cell.alignment = data_alignment
            cell.border = border
    
    # 设置交替行颜色
    for i, row in enumerate(ws.iter_rows(min_row=2), start=2):
        fill_color = 'DCE6F1' if i % 2 == 0 else 'FFFFFF'
        for cell in row:
            cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type='solid')
    
    # 自动调整列宽
    auto_adjust_column_width(ws)
    
    # 冻结标题行
    ws.freeze_panes = 'A2'


def enhanced_csv_to_excel(csv_file: str, excel_file: str, new_headers: list[str] | None=None):
    """
    **Minecraft 投影Mod的材料列表 CSV转Excel转换器**
    
    ### 参数
    - `csv_file`: 输入的CSV文件路径
    - `excel_file`: 输出的Excel文件路径
    - `new_headers`: 可选，要替换的首行标题列表

    ### 使用示例

    ```python
    enhanced_csv_to_excel(
        csv_file='input.csv',
        excel_file='output.xlsx',
        new_headers=['名称', '个数', '组数(向下取整)', '盒数(向下取整)', '数量']  # 可选，替换原始标题
    )
    ```
    """

    wb = Workbook()
    ws = wb.active
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        # 读取原始数据
        rows = list(reader)
        if rows == []:
            log(logging.ERROR, "CSV is empty.")
        original_headers = rows[0]
        data_rows = rows[1:]  # 排除标题行
        
        # 验证B列是否存在且为数字
        if len(original_headers) < 2:
            raise ValueError("CSV文件必须至少包含B列(第2列)")
               
        ws.append(new_headers)
        
        # 处理数据
        item_column_sum = 0
        valid_rows = 0
        
        for row in data_rows:
            if len(row) < 2:
                continue  # 跳过不完整的行
                
            try:
                b_value = float(row[1])  # 假设B列是第2列
            except ValueError:
                continue  # 跳过B列不是数字的行
                
            # 计算新列值
            e_value = b_value
            d_value = floor(b_value / 1728)
            c_value = floor(b_value / 64) % 1728
            b_value %= 64
            
            # 确保 new_row 包含所有原始列，同时插入 C、D 列（组数和盒数）
            new_row = [row[0], b_value, c_value, d_value, e_value]
            ws.append(new_row)
            item_column_sum += e_value
            valid_rows += 1
        
        # 添加汇总行
        if valid_rows > 0:
            ws.append(['汇总', f'物品总数: {int(item_column_sum)}', '', f'共有 {valid_rows} 种不同物品'])

    beautify_excel(ws)

    # 保存文件
    wb.save(excel_file)
    log(logging.INFO, f"Task Finish: {csv_file} → {excel_file}")
