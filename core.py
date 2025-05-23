import os
import re
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
import base64
from pygments.formatters import HtmlFormatter
import io
from PIL import Image
import networkx as nx
import matplotlib.pyplot as plt
import uuid

class MarkdownConverter:
    def __init__(self, theme="elegant"):
        self.theme = theme
        self.html_template = self._get_html_template()
        self.md_extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.toc',
            CodeHiliteExtension(css_class='highlight'),
            FencedCodeExtension(),
            TableExtension()
        ]
        
    def _get_html_template(self):
        """获取HTML模板"""
        # 尝试多种可能的主题文件路径
        possible_theme_dirs = [
            # 当前工作目录的themes子目录
            os.path.join(os.getcwd(), "themes"),
            # 脚本所在目录的themes子目录
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "themes"),
            # 相对于当前目录的themes
            "themes"
        ]
        
        css_content = ""
        js_content = ""
        
        # 尝试从每个可能的目录加载主题文件
        for theme_dir in possible_theme_dirs:
            css_file = os.path.join(theme_dir, f"{self.theme}.css")
            js_file = os.path.join(theme_dir, f"{self.theme}.js")
            
            # 尝试读取CSS文件
            if os.path.exists(css_file):
                try:
                    with open(css_file, 'r', encoding='utf-8') as f:
                        css_content = f.read()
                    print(f"已加载CSS文件: {css_file}")
                    break  # 找到CSS文件后退出循环
                except Exception as e:
                    print(f"读取CSS文件时出错: {str(e)}")
        
        # 重新遍历目录寻找JS文件
        for theme_dir in possible_theme_dirs:
            js_file = os.path.join(theme_dir, f"{self.theme}.js")
            
            # 尝试读取JS文件
            if os.path.exists(js_file):
                try:
                    with open(js_file, 'r', encoding='utf-8') as f:
                        js_content = f.read()
                    print(f"已加载JS文件: {js_file}")
                    break  # 找到JS文件后退出循环
                except Exception as e:
                    print(f"读取JS文件时出错: {str(e)}")
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{title}}}}</title>
    <style>
        {css_content}
        {HtmlFormatter().get_style_defs('.highlight')}
    </style>
</head>
<body data-theme="{self.theme}" class="{self.theme}-theme">
    <div class="container">
        {{{{content}}}}
    </div>
    <script>
        {js_content}
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', (event) => {{
            const currentTheme = document.body.getAttribute('data-theme');
            const isDarkTheme = currentTheme === "dark" || document.body.classList.contains('dark-theme');
            
            mermaid.initialize({{
                startOnLoad: true,
                theme: isDarkTheme ? 'dark' : 'default',
                themeVariables: isDarkTheme ? {{
                    primaryColor: '#BB86FC',
                    primaryTextColor: '#F8F8F8',
                    primaryBorderColor: '#DDDDDD',
                    lineColor: '#FFFF00',
                    secondaryColor: '#03DAC6',
                    tertiaryColor: '#282A36',
                    textColor: '#F8F8F8',
                    mainBkg: '#3A3C4B',
                    nodeBorder: '#DDDDDD',
                    clusterBkg: '#333333',
                    clusterBorder: '#DDDDDD',
                    edgeLabelBackground: '#444444',
                    fontSize: '16px'
                }} : undefined
            }});
            
            // 使用CSS覆盖Mermaid样式，确保线条为黄色
            if (isDarkTheme) {{
                const style = document.createElement('style');
                style.textContent = `
                    .mermaid .flowchart-link {{ stroke: #FFAB40 !important; }}
                    .mermaid .marker {{ fill: #FFAB40 !important; }}
                    .mermaid line {{ stroke: #FFAB40 !important; }}
                    .mermaid .path {{ stroke: #FFAB40 !important; }}
                    .mermaid .messageText {{ fill: #FFAB40 !important; }}
                    .mermaid .relationshipLine {{ stroke: #FFAB40 !important; }}
                    .mermaid .loopLine {{ stroke: #FFAB40 !important; }}
                    .mermaid text {{ fill: #F8F8F8 !important; }}
                    .mermaid .nodeLabel {{ fill: #F8F8F8 !important; }}
                    .mermaid .edgeLabel {{ fill: #F8F8F8 !important; }}
                    .mermaid .label {{ fill: #F8F8F8 !important; color: #F8F8F8 !important; }}
                `;
                document.head.appendChild(style);
            }}
        }});
    </script>
</body>
</html>
"""

    def _process_mermaid_diagrams(self, content):
        """处理mermaid图表，转为图片"""
        pattern = r'```mermaid\s*(.*?)\s*```'
        
        def replace_mermaid(match):
            mermaid_code = match.group(1)
            try:
                # 这里应该使用适当的工具将mermaid代码转换为图片
                # 这只是一个占位示例，实际项目中可能需要使用其他库或API
                img_data = f'<div class="mermaid">{mermaid_code}</div>'
                return img_data
            except Exception as e:
                return f"<div class='error'>Error rendering mermaid: {str(e)}</div>"
                
        return re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)
    
    def _process_file_links(self, content, base_path, file_mapping=None):
        """处理文件内的链接，确保它们在HTML中正确工作"""
        if not file_mapping:
            file_mapping = {}
            
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        def replace_link(match):
            text = match.group(1)
            link = match.group(2)
            
            # 如果链接是一个Markdown文件
            if link.endswith('.md'):
                if link in file_mapping:
                    return f'[{text}]({file_mapping[link]})'
                html_link = link.replace('.md', '.html')
                return f'[{text}]({html_link})'
            
            # 如果是内部链接（例如#section）
            if link.startswith('#'):
                return f'[{text}]({link})'
                
            # 如果是外部链接
            if link.startswith('http'):
                return f'[{text}]({link})'
                
            # 其他本地文件
            return f'[{text}]({link})'
            
        return re.sub(pattern, replace_link, content)
    
    def convert_file(self, md_file_path, output_path=None):
        """将单个Markdown文件转换为HTML"""
        if not output_path:
            output_path = os.path.splitext(md_file_path)[0] + '.html'
        
        # 读取Markdown文件
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"读取到Markdown内容，长度: {len(content)} 字符")
            print(f"Markdown内容前100个字符: {content[:100]}")
            
            # 将[toc]或[TOC]替换为HTML占位符
            content = re.sub(r'\[(toc|TOC)\]', '<div class="toc-placeholder"></div>', content)
            
            # 处理mermaid图表
            content = self._process_mermaid_diagrams(content)
            
            # 处理文件链接
            base_path = os.path.dirname(md_file_path)
            content = self._process_file_links(content, base_path)
            
            # 转换为HTML
            try:
                html_content = markdown.markdown(content, extensions=self.md_extensions)
                print(f"转换后HTML内容，长度: {len(html_content)} 字符")
                if len(html_content) > 0:
                    print(f"HTML内容前100个字符: {html_content[:100]}")
                else:
                    print("警告: HTML内容为空!")
            except Exception as e:
                print(f"转换HTML时出错: {str(e)}")
                html_content = f"<p>Error converting markdown: {str(e)}</p>"
            
            # 获取标题
            title = os.path.basename(md_file_path)
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match:
                title = title_match.group(1)
                
            print(f"使用标题: {title}")
            
            # 填充模板
            html_output = self.html_template.replace('{{title}}', title).replace('{{content}}', html_content)
            
            print(f"生成的完整HTML，长度: {len(html_output)} 字符")
            
            # 写入输出文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_output)
                
            return output_path
        except Exception as e:
            print(f"处理文件时出错: {str(e)}")
            raise
    
    def convert_directory(self, input_dir, output_dir=None):
        """转换目录中的所有Markdown文件"""
        if not output_dir:
            output_dir = input_dir
            
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 获取所有Markdown文件
        md_files = []
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.md'):
                    md_files.append(os.path.join(root, file))
        
        # 创建文件映射关系（用于处理链接）
        file_mapping = {}
        for md_file in md_files:
            rel_path = os.path.relpath(md_file, input_dir)
            html_file = os.path.splitext(rel_path)[0] + '.html'
            html_path = os.path.join(output_dir, html_file)
            file_mapping[rel_path] = html_file
        
        # 转换每个文件
        converted_files = []
        for md_file in md_files:
            rel_path = os.path.relpath(md_file, input_dir)
            html_file = os.path.splitext(rel_path)[0] + '.html'
            html_path = os.path.join(output_dir, html_file)
            
            # 确保输出目录存在
            os.makedirs(os.path.dirname(html_path), exist_ok=True)
            
            # 读取Markdown内容
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 处理mermaid图表
            content = self._process_mermaid_diagrams(content)
            
            # 处理文件链接
            content = self._process_file_links(content, os.path.dirname(md_file), file_mapping)
            
            # 转换为HTML
            html_content = markdown.markdown(content, extensions=self.md_extensions)
            
            # 获取标题
            title = os.path.basename(md_file)
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match:
                title = title_match.group(1)
            
            # 填充模板
            html_output = self.html_template.replace('{{title}}', title).replace('{{content}}', html_content)
            
            # 写入输出文件
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_output)
                
            converted_files.append(html_path)
            
        return converted_files 