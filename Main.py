# 导入模块
import time
import tkinter as tk
from tkinter import messagebox, ttk, font
import pandas as pd
from PIL import ImageTk, Image
from pandastable import Table, TableModel
from Data_Query import TrainQuery
import Automatic_Buy
from time import strftime
import AccountIO
import sys, os

# 设置主题颜色
THEME_COLOR = {
    'primary': '#1890ff',      # 亮蓝色
    'secondary': '#e6f7ff',    # 浅蓝文字
    'background': '#141414',   # 深黑背景
    'surface': '#1f1f1f',      # 稍浅的黑色
    'surface_2': '#2d2d2d',    # 更浅的黑色（用于输入区域）
    'error': '#ff4d4f',        # 错误红
    'success': '#52c41a',      # 成功绿
    'border': '#303030',       # 深灰边框
    'hover': '#40a9ff',        # 悬停蓝
    'input_bg': '#2d2d2d',     # 输入框背景
    'text': '#ffffff',         # 主文字颜色
    'text_secondary': '#8c8c8c' # 次要文字颜色
}

# 创建查询对象
train_query = TrainQuery(show_logs=True)

# 这里时获取打包后图片资源
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 获取当前时间
Today = time.strftime("%Y-%m-%d")

# 用来保存查询到的车次号
trains_Number = []

# 保存第一次登录的cookie
Cookie = []

# 自定义输入框样式
class CustomEntry(ttk.Entry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(style='Custom.TEntry')
        self.bind('<FocusIn>', self.on_focus_in)
        self.bind('<FocusOut>', self.on_focus_out)
        
    def on_focus_in(self, event):
        self.state(['focus'])
        
    def on_focus_out(self, event):
        self.state(['!focus'])

# 自定义按钮样式
class CustomButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            relief='flat',
            borderwidth=0,
            highlightthickness=0,
            padx=15,
            pady=8,
            cursor='hand2',
            activebackground=THEME_COLOR['hover'],
            activeforeground=THEME_COLOR['text']
        )
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self['background'] = THEME_COLOR['hover']

    def on_leave(self, e):
        self['background'] = THEME_COLOR['primary']

# 创建表格Frame和滚动条
def create_table(df, parent_frame):
    # 创建一个Frame来包含表格
    container = tk.Frame(parent_frame, background=THEME_COLOR['surface'])
    container.pack(fill='both', expand=True)
    
    # 创建表格
    table = Table(container, dataframe=df, showtoolbar=False,
                showstatusbar=False, width=1160, height=500)
    
    # 设置表格样式
    table.cellwidth = 60  # 设置单元格宽度
    table.cellbackgr = THEME_COLOR['surface']  # 设置单元格背景色
    table.textcolor = THEME_COLOR['text']  # 设置文字颜色
    table.grid_color = THEME_COLOR['border']  # 设置网格线颜色
    table.colheadercolor = THEME_COLOR['primary']  # 设置列头背景色
    table.rowselectedcolor = THEME_COLOR['hover']  # 设置选中行的颜色
    
    # 设置特定列的宽度
    col_widths = {
        '车次': 80,
        '出发站': 100,
        '到达站': 100,
        '出发时间': 100,
        '到达时间': 100,
        '历时': 80,
        '备注': 80
    }
    
    # 显示表格
    table.show()
    
    # 应用列宽设置
    for col, width in col_widths.items():
        if col in table.model.df.columns:
            table.columnwidths[table.model.df.columns.get_loc(col)] = width
    
    # 设置行高和字体
    table.rowheight = 30
    table.thefont = ('Microsoft YaHei UI', 10)
    
    # 设置表头样式
    table.colheaderheight = 35
    table.colheaderfont = ('Microsoft YaHei UI', 10, 'bold')
    table.colheaderfg = 'white'
    
    return table

# 查询车次信息
def chick_info(start_place, end_place, start_time, start_hour, end_hour, user_type):
    # 禁用查询按钮，显示加载状态
    query_button.config(state='disabled', text='查询中...')
    root.update()
    
    try:
        print(start_place.get(), end_place.get(), start_time.get(), start_hour.get(), end_hour.get(), user_type)
        # 使用TrainQuery类查询车票信息
        trains = train_query.query_tickets(
            start_place.get(), 
            end_place.get(), 
            start_time.get()
        )
        
        if not trains:
            messagebox.showinfo('提示', '未查询到车次信息！')
            return
            
        # 将数据转换为DataFrame
        df = pd.DataFrame(trains)
        
        # 提取车次号
        global trains_Number
        trains_Number = df['车次'].tolist()
        print(trains_Number)
        
        # 过滤时间段
        if start_hour.get() and end_hour.get():
            try:
                start_h = int(start_hour.get())
                end_h = int(end_hour.get())
                if 0 <= start_h <= 24 and 0 <= end_h <= 24:
                    # 转换时间字符串为小时
                    df['出发小时'] = df['出发时间'].apply(lambda x: int(x.split(':')[0]))
                    # 过滤时间段
                    df = df[(df['出发小时'] >= start_h) & (df['出发小时'] <= end_h)]
                    # 删除临时列
                    df = df.drop('出发小时', axis=1)
                else:
                    messagebox.showwarning('警告', '时间范围应在0-24之间')
            except ValueError:
                messagebox.showwarning('警告', '请输入有效的小时数字')
        
        if df.empty:
            messagebox.showinfo('提示', '该时间段内未查询到车次信息！')
            return
            
        # 清除旧的表格
        for widget in table_frame.winfo_children():
            widget.destroy()
        
        # 设置表格显示的列顺序
        columns = [
            '车次', '出发站', '到达站', '出发时间', '到达时间', '历时',
            '商务座', '特等座', '一等座', '二等座',
            '高级软卧', '软卧', '动卧', '硬卧',
            '软座', '硬座', '无座', '其他', '备注'
        ]
        
        # 重新排序DataFrame的列
        df = df[columns]
        
        # 创建新的表格
        table = create_table(df, table_frame)
        
        # 更新结果标签
        result_label.config(text=f'查询结果 (共{len(df)}条)')
        
    except Exception as e:
        print(f"查询出错: {str(e)}")
        messagebox.showinfo('提示', f'查询失败：{str(e)}')
    finally:
        # 恢复查询按钮状态
        query_button.config(state='normal', text='查询')

# ==========================================================================================================
# 创建应用程序主窗口
root = tk.Tk()

# 设置ttk样式
style = ttk.Style()
style.configure('Custom.TEntry',
                fieldbackground=THEME_COLOR['input_bg'],
                foreground=THEME_COLOR['text'],
                borderwidth=1,
                relief='solid',
                padding=8)
style.configure('Custom.TCombobox',
                fieldbackground=THEME_COLOR['input_bg'],
                foreground=THEME_COLOR['text'],
                borderwidth=1,
                relief='solid',
                padding=8)
style.map('Custom.TCombobox',
          fieldbackground=[('readonly', THEME_COLOR['input_bg'])],
          selectbackground=[('readonly', THEME_COLOR['input_bg'])],
          selectforeground=[('readonly', THEME_COLOR['text'])])

# 设置窗口图标
root.iconbitmap(get_resource_path(r'images/favicon.ico'))

# 设置窗口背景色
root.configure(background=THEME_COLOR['background'])

# 设置窗口位置和大小
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 1200  # 增加窗口宽度
window_height = 800  # 增加窗口高度
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f'{window_width}x{window_height}+{x}+{y}')

# 设置窗口大小不可改变
root.resizable(width=False, height=False)

# 设置窗口标题
root.title('12306车票查询与抢票')

# 创建主Frame，使用网格布局
main_frame = tk.Frame(root, background=THEME_COLOR['background'])
main_frame.pack(fill='both', expand=True, padx=20, pady=20)

# 创建顶部容器Frame
header_container = tk.Frame(main_frame, background=THEME_COLOR['background'])
header_container.pack(fill='x', pady=(0, 20))

# 创建logo和标题Frame
logo_frame = tk.Frame(header_container, background=THEME_COLOR['surface'], relief='flat', bd=1)
logo_frame.pack(fill='x')

# 设置logo
img = Image.open(get_resource_path('images/logo.png'))
img = img.resize((1160, 120), Image.Resampling.LANCZOS)
img_tk = ImageTk.PhotoImage(img)
logo_label = tk.Label(logo_frame, image=img_tk, background=THEME_COLOR['surface'])
logo_label.pack(fill='x', padx=10, pady=10)

# 创建标题和时间Frame
title_frame = tk.Frame(logo_frame, background=THEME_COLOR['surface'])
title_frame.pack(fill='x', pady=5)

name = tk.Label(title_frame, text='12306车票查询与抢票', font=(
    "Microsoft YaHei UI", 26, "bold"), fg=THEME_COLOR['text'], background=THEME_COLOR['surface'])
name.pack()

time_label = tk.Label(title_frame, font=("Microsoft YaHei UI", 14), 
                     fg=THEME_COLOR['text_secondary'], background=THEME_COLOR['surface'])
time_label.pack(pady=5)

# 创建查询区域Frame
query_container = tk.Frame(main_frame, background=THEME_COLOR['surface_2'], relief='flat', bd=1)
query_container.pack(fill='x', pady=(0, 20))

# 创建输入区域Frame
input_frame = tk.Frame(query_container, background=THEME_COLOR['surface_2'])
input_frame.pack(fill='x', padx=30, pady=20)

# 创建左侧输入区域
left_input_frame = tk.Frame(input_frame, background=THEME_COLOR['surface_2'])
left_input_frame.pack(side='left', fill='x', expand=True)

# 创建输入控件的行
def create_input_row(parent, items):
    row = tk.Frame(parent, background=THEME_COLOR['surface_2'])
    row.pack(fill='x', pady=5)
    for item in items:
        frame = tk.Frame(row, background=THEME_COLOR['surface_2'])
        frame.pack(side='left', padx=(0, 30))
        label = tk.Label(frame, text=item['label'], font=('Microsoft YaHei UI', 12),
                        fg=THEME_COLOR['text'], background=THEME_COLOR['surface_2'])
        label.pack(side='left', padx=(0, 8))
        item['widget'](frame).pack(side='left')

# 第一行：出发站和目的站
row1 = tk.Frame(left_input_frame, background=THEME_COLOR['surface_2'])
row1.pack(fill='x', pady=5)

# 出发站
start_frame = tk.Frame(row1, background=THEME_COLOR['surface_2'])
start_frame.pack(side='left', padx=(0, 30))
tk.Label(start_frame, text='出发站', font=('Microsoft YaHei UI', 12),
         fg=THEME_COLOR['text'], background=THEME_COLOR['surface_2']).pack(side='left', padx=(0, 8))
start_place = CustomEntry(start_frame, font=('Microsoft YaHei UI', 12), width=12, style='Custom.TEntry')
start_place.pack(side='left')

# 目的站
end_frame = tk.Frame(row1, background=THEME_COLOR['surface_2'])
end_frame.pack(side='left', padx=(0, 30))
tk.Label(end_frame, text='目的站', font=('Microsoft YaHei UI', 12),
         fg=THEME_COLOR['text'], background=THEME_COLOR['surface_2']).pack(side='left', padx=(0, 8))
end_place = CustomEntry(end_frame, font=('Microsoft YaHei UI', 12), width=12, style='Custom.TEntry')
end_place.pack(side='left')

# 第二行：出发时间和时间段
time_row = tk.Frame(left_input_frame, background=THEME_COLOR['surface_2'])
time_row.pack(fill='x', pady=5)

# 出发时间
date_frame = tk.Frame(time_row, background=THEME_COLOR['surface_2'])
date_frame.pack(side='left', padx=(0, 30))
tk.Label(date_frame, text='出发时间', font=('Microsoft YaHei UI', 12),
         fg=THEME_COLOR['text'], background=THEME_COLOR['surface_2']).pack(side='left', padx=(0, 8))
start_time = CustomEntry(date_frame, font=('Microsoft YaHei UI', 12), width=12, style='Custom.TEntry')
start_time.insert(0, Today)
start_time.pack(side='left')

# 时间段
time_frame = tk.Frame(time_row, background=THEME_COLOR['surface_2'])
time_frame.pack(side='left', padx=(0, 30))
tk.Label(time_frame, text='时间段', font=('Microsoft YaHei UI', 12),
         fg=THEME_COLOR['text'], background=THEME_COLOR['surface_2']).pack(side='left', padx=(0, 8))
start_hour = CustomEntry(time_frame, font=('Microsoft YaHei UI', 12), width=3, style='Custom.TEntry')
start_hour.pack(side='left')
tk.Label(time_frame, text='-', font=('Microsoft YaHei UI', 12),
         fg=THEME_COLOR['text'], background=THEME_COLOR['surface_2']).pack(side='left', padx=3)
end_hour = CustomEntry(time_frame, font=('Microsoft YaHei UI', 12), width=3, style='Custom.TEntry')
end_hour.pack(side='left')
tk.Label(time_frame, text='时', font=('Microsoft YaHei UI', 12),
         fg=THEME_COLOR['text'], background=THEME_COLOR['surface_2']).pack(side='left', padx=(3, 0))

# 第三行：车票类型和查询按钮
bottom_row = tk.Frame(left_input_frame, background=THEME_COLOR['surface_2'])
bottom_row.pack(fill='x', pady=5)

# 车票类型
type_frame = tk.Frame(bottom_row, background=THEME_COLOR['surface_2'])
type_frame.pack(side='left')
tk.Label(type_frame, text='车票类型', font=('Microsoft YaHei UI', 12),
         fg=THEME_COLOR['text'], background=THEME_COLOR['surface_2']).pack(side='left', padx=(0, 8))
user_type = ttk.Combobox(type_frame, values=['成人票', '学生票'], width=8,
                        font=('Microsoft YaHei UI', 12), state='readonly', style='Custom.TCombobox')
user_type.set('成人票')
user_type.pack(side='left')

# 查询按钮
button_frame = tk.Frame(bottom_row, background=THEME_COLOR['surface_2'])
button_frame.pack(side='right', padx=30)
query_button = CustomButton(button_frame, text='查询', font=('Microsoft YaHei UI', 13, 'bold'),
                          fg='white', background=THEME_COLOR['primary'],
                          command=lambda: chick_info(start_place, end_place, start_time, 
                                                   start_hour, end_hour, user_type.get()))
query_button.configure(padx=30, pady=10)
query_button.pack()

# 创建结果区域Frame
result_container = tk.Frame(main_frame, background=THEME_COLOR['surface'], relief='flat', bd=1)
result_container.pack(fill='both', expand=True)

# 创建结果标签
result_label = tk.Label(result_container, text='查询结果', font=('Microsoft YaHei UI', 14, 'bold'),
                       fg=THEME_COLOR['text'], background=THEME_COLOR['surface'])
result_label.pack(anchor='w', padx=20, pady=10)

# 创建表格Frame
table_frame = tk.Frame(result_container, background=THEME_COLOR['surface'])
table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

# 定义显示时间的函数
def showtime():
    string = strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=string)
    time_label.after(1000, showtime)

# 调用showtime()函数
showtime()

# 启动主事件循环
root.mainloop()
