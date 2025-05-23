#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Markdown转HTML工具
支持命令行和图形界面两种模式
"""

import sys
import argparse

def main():
    """主入口函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Markdown转HTML工具")
    parser.add_argument('--gui', action='store_true', help='启动图形界面模式')
    parser.add_argument('--cli', action='store_true', help='启动命令行模式')
    
    args, remaining = parser.parse_known_args()
    
    # 如果没有指定模式，或者指定为GUI模式，则启动图形界面
    if not args.cli or args.gui:
        try:
            from gui import main as gui_main
            gui_main()
        except ModuleNotFoundError:
            print("错误：无法启动图形界面。请确保安装了必要的依赖。")
            print("尝试运行: pip install -r requirements.txt")
            return 1
        except ImportError as e:
            print(f"错误：启动图形界面失败: {str(e)}")
            print("尝试运行: pip install -r requirements.txt")
            return 1
    # 如果指定为命令行模式，则启动命令行工具
    else:
        try:
            from command_line import main as cli_main
            sys.argv = [sys.argv[0]] + remaining  # 重置命令行参数，去掉--cli
            cli_main()
        except ModuleNotFoundError:
            print("错误：无法启动命令行模式。请确保安装了必要的依赖。")
            print("尝试运行: pip install -r requirements.txt")
            return 1
        except ImportError as e:
            print(f"错误：启动命令行模式失败: {str(e)}")
            print("尝试运行: pip install -r requirements.txt")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 