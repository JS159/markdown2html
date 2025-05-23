import os
import glob
import shutil
import threading
import webbrowser
from pathlib import Path
import sys

def get_available_themes():
    """获取可用的主题列表"""
    # 尝试多种可能的主题目录路径
    possible_theme_dirs = [
        # 当前工作目录的themes子目录
        os.path.join(os.getcwd(), "themes"),
        # 脚本所在目录的themes子目录
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "themes"),
        # 相对于当前目录的themes
        "themes"
    ]
    
    css_files = []
    theme_dir_used = None
    
    # 尝试每个可能的路径
    for theme_dir in possible_theme_dirs:
        if os.path.exists(theme_dir) and os.path.isdir(theme_dir):
            temp_css_files = glob.glob(os.path.join(theme_dir, "*.css"))
            if temp_css_files:
                css_files = temp_css_files
                theme_dir_used = theme_dir
                print(f"找到主题目录: {theme_dir}，CSS文件数量: {len(css_files)}")
                break
    
    # 如果没有找到任何主题，返回默认的elegant主题
    if not css_files:
        print(f"警告: 未找到任何主题文件。尝试的目录: {possible_theme_dirs}")
        return ["elegant"]
    
    # 从CSS文件名中提取主题名称
    themes = [os.path.splitext(os.path.basename(css))[0] for css in css_files]
    print(f"发现的主题: {themes}")
    
    # 排序主题，确保elegant主题排在最前面
    sorted_themes = []
    
    # 首先添加elegant主题（如果存在）
    if "elegant" in themes:
        sorted_themes.append("elegant")
        themes.remove("elegant")
    
    # 添加剩余的主题（按字母顺序）
    themes.sort()
    sorted_themes.extend(themes)
    
    return sorted_themes

def ensure_directory(directory_path):
    """确保目录存在，不存在则创建"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return directory_path

def clean_directory(directory_path):
    """清空目录内容"""
    if os.path.exists(directory_path):
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    else:
        os.makedirs(directory_path)
    return directory_path

def copy_resources(source_dir, target_dir):
    """复制资源文件（图片等）到目标目录"""
    if not os.path.exists(source_dir):
        return
        
    # 获取绝对路径以确保比较的准确性
    source_dir = os.path.abspath(source_dir)
    target_dir = os.path.abspath(target_dir)
    
    # 如果源目录和目标目录相同，则跳过复制
    if source_dir == target_dir:
        return
        
    ensure_directory(target_dir)
    
    # 复制所有非md文件
    for root, _, files in os.walk(source_dir):
        rel_path = os.path.relpath(root, source_dir)
        target_path = os.path.join(target_dir, rel_path)
        
        # 跳过复制当前目录的情况 (./)
        if rel_path == '.':
            target_path = target_dir
        else:
            ensure_directory(target_path)
        
        for file in files:
            if not file.endswith('.md'):
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_path, file)
                
                # 避免复制到相同文件
                if os.path.normpath(src_file) != os.path.normpath(dst_file):
                    try:
                        shutil.copy2(src_file, dst_file)
                    except shutil.SameFileError:
                        # 忽略相同文件错误
                        pass
                    except Exception as e:
                        print(f"复制文件时出错: {str(e)}")

def open_in_browser(html_file):
    """打开HTML文件所在的文件夹"""
    try:
        # 确保使用绝对路径
        abs_path = os.path.abspath(html_file)
        file_dir = os.path.dirname(abs_path)
        
        if sys.platform == 'win32':
            # Windows
            os.startfile(file_dir)
        elif sys.platform == 'darwin':
            # macOS
            threading.Thread(target=lambda: os.system(f'open "{file_dir}"')).start()
        else:
            # Linux
            threading.Thread(target=lambda: os.system(f'xdg-open "{file_dir}"')).start()
            
        print(f"已打开文件夹: {file_dir}")
    except Exception as e:
        print(f"无法打开文件夹: {e}")

def find_markdown_files(directory):
    """查找目录中的所有Markdown文件"""
    markdown_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
                
    return markdown_files

def get_file_title(file_path):
    """从Markdown文件中提取标题"""
    title = os.path.basename(file_path)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:]
                    
    except Exception:
        pass
        
    return os.path.splitext(title)[0]