import os
import sys
import argparse
from core import MarkdownConverter
from utils import get_available_themes, ensure_directory, copy_resources, open_in_browser

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Markdown转HTML工具")
    
    # 添加命令行参数
    parser.add_argument('-i', '--input', required=True, help='输入Markdown文件或目录')
    parser.add_argument('-o', '--output', dest='output_path', help='指定输出目录，如果未指定，则默认为与输入相同的目录')
    parser.add_argument('-t', '--theme', default='elegant', help='使用的主题名称')
    parser.add_argument('-l', '--list-themes', action='store_true', help='列出所有可用主题')
    parser.add_argument('-r', '--recursive', action='store_true', help='递归处理输入目录中的所有Markdown文件')
    parser.add_argument('-f', '--open-folder', dest="open_browser", action='store_true', help='转换后打开文件夹')
    
    args = parser.parse_args()
    return args

def list_themes():
    """列出所有可用的主题"""
    themes = get_available_themes()
    if not themes:
        print("没有找到可用的主题，请确保themes目录中包含主题文件。")
    else:
        print("可用的主题:")
        for theme in themes:
            print(f"  - {theme}")

def main():
    """主函数"""
    args = parse_arguments()
    
    # 如果仅仅是列出主题，则执行后退出
    if args.list_themes:
        list_themes()
        return
    
    # 检查输入路径是否存在
    if not os.path.exists(args.input):
        print(f"错误：输入路径 '{args.input}' 不存在。")
        return 1
    
    # 创建转换器
    converter = MarkdownConverter(theme=args.theme)
    
    # 确定输出路径
    output_path = args.output_path
    
    # 如果是文件
    if os.path.isfile(args.input):
        if not args.input.lower().endswith('.md'):
            print("错误：输入文件必须是Markdown文件（.md扩展名）。")
            return 1
            
        # 如果没有指定输出，则使用与输入相同的目录
        if not output_path:
            output_path = os.path.splitext(args.input)[0] + '.html'
        elif os.path.isdir(output_path):
            # 如果输出是目录，则在该目录中创建HTML文件
            base_name = os.path.basename(os.path.splitext(args.input)[0])
            output_path = os.path.join(output_path, base_name + '.html')
            
        # 确保输出目录存在
        ensure_directory(os.path.dirname(output_path))
        
        # 转换文件
        result = converter.convert_file(args.input, output_path)
        print(f"已创建HTML文件: {result}")
        
        # 如果需要在浏览器中打开
        if args.open_browser:
            open_in_browser(result)
    
    # 如果是目录
    elif os.path.isdir(args.input):
        # 如果没有指定输出，则使用与输入相同的目录
        if not output_path:
            output_path = args.input
            
        # 确保输出目录存在
        ensure_directory(output_path)
        
        # 复制资源文件（非MD文件）
        copy_resources(args.input, output_path)
        
        # 如果递归处理整个目录
        if args.recursive:
            results = converter.convert_directory(args.input, output_path)
            print(f"已创建 {len(results)} 个HTML文件在 {output_path}")
            
            # 如果需要在浏览器中打开第一个文件
            if args.open_browser and results:
                open_in_browser(results[0])
        else:
            # 只处理当前目录下的md文件
            files_processed = 0
            first_html = None
            
            for file in os.listdir(args.input):
                if file.lower().endswith('.md'):
                    md_path = os.path.join(args.input, file)
                    html_path = os.path.join(output_path, os.path.splitext(file)[0] + '.html')
                    result = converter.convert_file(md_path, html_path)
                    files_processed += 1
                    
                    if not first_html:
                        first_html = result
                    
                    print(f"已创建HTML文件: {result}")
            
            print(f"共处理了 {files_processed} 个文件")
            
            # 如果需要在浏览器中打开第一个文件
            if args.open_browser and first_html:
                open_in_browser(first_html)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())