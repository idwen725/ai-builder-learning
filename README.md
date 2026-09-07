# AI Builder Learning

这是我的 AI 与计算机科学学习项目。

我正在通过这个项目学习：

- Python 编程
- 软件工程基础
- AI 应用开发
- AI Agent 相关技术


## 项目介绍

这个项目是一个基于本地大语言模型的 AI 助手。

目前使用 Ollama 运行本地模型，通过 Python 程序调用 AI，并实现了一些基础功能：

- 与本地 AI 对话
- 保存聊天记录
- 加载历史记忆
- 日志记录
- 使用配置文件管理参数


## 当前功能

目前已经实现：

✅ Python 项目结构管理

✅ 使用 requests 调用 AI API

✅ 本地大语言模型调用

✅ 对话历史保存

✅ 长期记忆功能

✅ 日志系统

✅ 环境变量配置


## 使用技术

主要技术：

- Python
- Ollama
- Qwen3
- requests
- python-dotenv
- Git


## 项目结构

```
ai-builder-learning

├── src
│   ├── app.py          # 程序入口
│   ├── ai_client.py    # AI接口调用
│   ├── config.py       # 配置管理
│   ├── memory.py       # 记忆系统
│   └── logger.py       # 日志系统
│
├── requirements.txt    # Python依赖
├── .env.example        # 配置示例
└── README.md           # 项目说明
```


## 安装方法


### 1. 下载项目

```
git clone https://github.com/idwen725/ai-builder-learning.git
```


### 2. 创建虚拟环境

```
python -m venv .venv
```


### 3. 激活虚拟环境

Windows:

```
.venv\Scripts\activate
```


### 4. 安装依赖

```
pip install -r requirements.txt
```


### 5. 配置环境变量

复制：

```
.env.example
```

创建：

```
.env
```

示例：

```
MODEL=qwen3:4b
URL=http://localhost:11434/api/generate
TIMEOUT=30
```


## 运行方法


确保 Ollama 已经启动。

运行：

```
python src/main.py
```


## 学习进度

目前完成：

- Python 基础
- 文件操作
- JSON 数据处理
- API 调用
- 类与对象
- 项目模块化
- AI 接口调用
- 记忆系统
- 日志系统
- 配置管理


## 后续计划

未来继续学习：

- AI Agent 架构
- 工具调用
- RAG 检索增强生成
- Machine Learning
- Deep Learning
- Transformer 原理