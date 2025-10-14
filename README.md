# Qwen3-VL Computer Use

基于Qwen3-VL视觉语言模型的计算机操作自动化工具。该项目允许用户通过自然语言指令控制计算机，实现屏幕截图、鼠标控制和键盘输入等操作。

## 功能特点

- **视觉理解**: 利用Qwen3-VL模型理解屏幕截图内容
- **计算机控制**: 支持鼠标点击、键盘输入、屏幕滚动等操作
- **自动化任务**: 根据用户指令自动执行计算机操作
- **实时反馈**: 提供操作执行状态和结果反馈

## 技术架构

### 核心组件

1. **Qwen3-VL模型**: 阿里云的视觉语言模型，用于理解屏幕内容和用户指令
2. **ComputerUse工具**: 基于pynput库实现的计算机控制工具
3. **屏幕截图模块**: 使用pyscreenshot库捕获屏幕图像
4. **对话历史管理**: 管理与模型的交互历史

### 支持的操作

- 鼠标操作: 左键点击、右键点击、中键点击、双击、三击、移动、拖拽
- 键盘操作: 按键输入、文本输入、组合键
- 其他操作: 滚动、等待、任务终止

## 安装指南

### 环境要求

- Python 3.10+
- DashScope API密钥 (阿里云Qwen模型访问权限)

### 安装步骤

1. 克隆项目:
   ```bash
   git clone https://github.com/xiaopang927423/Qwen3-VL-computer-Use.git
   cd Qwen3-VL-cookbook/pythonProject6
   ```

2. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量:
   在项目根目录创建 `.env` 文件，添加以下内容:
   ```
   DASHSCOPE_API_KEY=your_api_key_here
   DASHSCOPE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
   ```

## 使用方法

### 基本使用

运行主程序:
```bash
python cookbook_computer_use.py
```

程序启动后会提示输入您的需求，例如"打开VSCode"或"在浏览器中搜索Qwen3-VL"。

### 工作流程

1. 用户输入任务指令
2. 程序截取当前屏幕截图
3. 将截图和指令发送给Qwen3-VL模型
4. 模型分析截图并生成操作指令
5. 程序执行相应的计算机操作
6. 重复步骤2-5直到任务完成

## 项目结构

```
.
├── cookbook_computer_use.py     # 主程序入口
├── utils/
│   ├── agent_function_call.py   # 计算机操作工具实现
│   ├── take_screenshot.py       # 屏幕截图功能
│   └── chat_history.py          # 对话历史管理
├── test/
│   ├── test_action.py           # 操作测试
│   └── test_pynput.py           # pynput库功能测试
└── .env                         # 环境变量配置文件
```

## 核心模块说明

### ComputerUse工具 (utils/agent_function_call.py)

实现了与计算机交互的各种操作:
- 鼠标控制: 点击、移动、拖拽
- 键盘输入: 文本输入、按键组合
- 系统操作: 滚动、等待、任务终止

### 屏幕截图 (utils/take_screenshot.py)

负责捕获屏幕图像并调整到合适的分辨率供模型分析。

### 对话管理 (utils/chat_history.py)

管理与Qwen3-VL模型的对话历史，包括系统提示、用户指令和模型响应。

## 注意事项

1. **权限问题**: 在某些操作系统上，可能需要为应用程序授予屏幕录制和控制权限
2. **分辨率适配**: 程序会自动调整屏幕截图分辨率以匹配模型要求
3. **操作延迟**: 某些操作(如程序启动)可能需要等待时间，程序内置了等待机制
4. **API密钥**: 需要有效的DashScope API密钥才能访问Qwen3-VL模型

## 测试

项目包含以下测试文件:
- `test_pynput.py`: 测试pynput库的基本功能
- `test_action.py`: 测试操作执行流程

运行测试:
```bash
python test/test_pynput.py
python test/test_action.py
```

## 依赖库

- openai: 与DashScope API通信
- pynput: 控制鼠标和键盘
- pyscreenshot: 屏幕截图
- python-dotenv: 环境变量管理
- qwen-agent: Qwen模型工具包

## 许可证

本项目仅供学习和研究使用，请遵守相关法律法规和阿里云服务条款。
