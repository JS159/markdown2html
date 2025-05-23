# Markdown 转 HTML 工具

这是一个 Markdown 转 HTML 工具，使用 Python 开发，支持多种主题风格和多种转换方式，完全基于AI开发。

## 功能特点

### 核心功能

- **多主题支持**：提供多种精美主题（elegant、elegant-dark、github、minimalist、night、sepia）
- **双模式操作**：支持命令行和图形界面两种使用方式
- **批量转换**：能够批量处理单个文件、多个文件或整个目录
- **文件关联处理**：自动解析文件夹下的 Markdown 文件之间的引用和跳转关系
- **完整资源处理**：确保生成的 HTML 文件能够成功跳转和显示所有资源
- **Mermaid 图表支持**：自动解析 Mermaid 格式，转换成图片
- **代码高亮**：支持代码块分析和语法高亮

## 使用说明

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动图形界面

```bash
python main.py --gui
```

或直接运行（默认为图形界面模式）：

```bash
python main.py
```

### 使用命令行模式

```bash
python main.py --cli [其他参数]
```

## 示例文件

示例 Markdown 文件位于 `example` 目录下：

- `mermaid_test.md` - 展示 Mermaid 图表功能
- `theme_showcase.md` - 展示不同主题效果

## 项目结构

主要组件：

- `core.py` - 核心转换逻辑
- `gui.py` - 图形用户界面实现
- `command_line.py` - 命令行接口实现
- `utils.py` - 工具函数
- `config_manager.py` - 配置管理
- `call_llm.py` - LLM API 调用工具

主题文件存放在 `themes` 目录下，每个主题包含对应的 CSS 和 JS 文件。
