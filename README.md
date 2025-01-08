# Python版12306查询系统操作手册

## 1. 环境配置

### 1.1 Python环境要求
- Python 3.8+
- pip包管理器

### 1.2 创建虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
## Windows
venv\Scripts\activate
## macOS/Linux
source venv/bin/activate
```

### 1.3 安装依赖
```bash
# 安装基础依赖
pip install pandas pillow pandastable requests

# 安装GUI依赖（如果系统没有tkinter）
## macOS
brew install python-tk

## Ubuntu/Debian
sudo apt-get install python3-tk

## CentOS/RHEL
sudo yum install python3-tkinter
```

## 2. 项目结构
```
12306/
├── Data_Query.py    # 主要查询逻辑
├── Main.py          # GUI界面和主程序
├── requirements.txt # 依赖清单
└── README.md        # 项目说明
```

## 3. 运行程序

### 3.1 直接运行
```bash
# 确保在虚拟环境中
python Main.py
```

### 3.2 命令行查询
```bash
python Data_Query.py
```

## 4. 使用说明

### 4.1 查询参数
- 出发站：支持中文站名（例如：北京）
- 到达站：支持中文站名（例如：上海）
- 出发日期：YYYY-MM-DD格式（默认明天）
- 时间段：HH:MM格式（可选）

### 4.2 输出文件
- train_schedule.txt：保存详细的车次信息
- train_stops.txt：保存经停站信息

### 4.3 示例查询
```bash
请输入出发站（例如：北京）：深圳北
请输入到达站（例如：天津）：长沙南
请输入出发日期（格式：YYYY-MM-DD，直接回车默认明天）：
请输入起始时间（格式：HH:MM，例如：08:00，直接回车表示不限制）：10:00
请输入结束时间（格式：HH:MM，例如：18:00，直接回车表示不限制）：15:00
```

## 5. 常见问题解决

### 5.1 依赖安装失败
```bash
# 尝试更新pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 5.2 tkinter相关错误
确保系统已安装tkinter：
```bash
# 验证tkinter安装
python -c "import tkinter; tkinter._test()"
```

### 5.3 查询失败处理
- 检查网络连接
- 确认站名输入正确
- 查看是否需要更新车站代码

## 6. 注意事项
1. 保持虚拟环境激活状态
2. 确保网络连接稳定
3. 遵守12306接口访问频率限制
4. 定期更新依赖包版本 