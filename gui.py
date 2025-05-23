import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

from core import MarkdownConverter
from utils import get_available_themes, ensure_directory, copy_resources, open_in_browser, find_markdown_files, get_file_title
from config_manager import ConfigManager

class MarkdownToHtmlGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown 转 HTML 工具")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # 设置应用图标
        # self.root.iconbitmap('icon.ico')  # 如果有图标文件，可以取消注释
        
        # 加载配置
        self.config_manager = ConfigManager()
        
        # 获取可用主题
        self.themes = get_available_themes()
        if not self.themes:
            self.themes = ["elegant"]
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建界面元素
        self._create_input_section()
        self._create_theme_section()
        self._create_options_section()
        self._create_output_section()
        self._create_buttons()
        self._create_status_bar()
        
        # 应用配置
        self._apply_config()
        
        # 转换器
        self.converter = None
        
        # 状态变量
        self.is_converting = False
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
    def _apply_config(self):
        """应用配置到界面元素"""
        theme = self.config_manager.get("theme")
        if theme in self.themes:
            self.theme_var.set(theme)
        
        last_input = self.config_manager.get("last_input_path")
        if last_input and os.path.exists(last_input):
            self.input_var.set(last_input)
            
        last_output = self.config_manager.get("last_output_path")
        if last_output and os.path.exists(last_output):
            self.output_var.set(last_output)
            
        self.recursive_var.set(self.config_manager.get("recursive", True))
        self.open_browser_var.set(self.config_manager.get("open_folder_after", True))
        
    def _save_config(self):
        """保存当前配置"""
        self.config_manager.update({
            "theme": self.theme_var.get(),
            "last_input_path": self.input_var.get(),
            "last_output_path": self.output_var.get(),
            "recursive": self.recursive_var.get(),
            "open_folder_after": self.open_browser_var.get()
        })
        self.config_manager.save_config()
        
    def _on_close(self):
        """窗口关闭事件处理"""
        self._save_config()
        self.root.destroy()
        
    def _create_input_section(self):
        """创建输入部分"""
        input_frame = ttk.LabelFrame(self.main_frame, text="输入", padding="5")
        input_frame.pack(fill=tk.X, pady=5)
        
        # 输入标签和输入框
        ttk.Label(input_frame, text="输入文件或目录:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_var, width=50)
        self.input_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # 创建按钮框架
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=0, column=2, padx=5, pady=5)
        
        # 选择文件按钮
        self.browse_files_btn = ttk.Button(btn_frame, text="选择文件", command=self._browse_input_files)
        self.browse_files_btn.pack(side=tk.LEFT, padx=2)
        
        # 选择文件夹按钮
        self.browse_folder_btn = ttk.Button(btn_frame, text="选择文件夹", command=self._browse_input_folder)
        self.browse_folder_btn.pack(side=tk.LEFT, padx=2)
        
        # 设置网格列的权重
        input_frame.columnconfigure(1, weight=1)
        
    def _create_theme_section(self):
        """创建主题部分"""
        theme_frame = ttk.LabelFrame(self.main_frame, text="主题", padding="5")
        theme_frame.pack(fill=tk.X, pady=5)
        
        # 主题标签和下拉菜单
        ttk.Label(theme_frame, text="选择主题:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.theme_var = tk.StringVar(value=self.themes[0])
        self.theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, values=self.themes, state="readonly")
        self.theme_combo.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # 设置网格列的权重
        theme_frame.columnconfigure(1, weight=1)
        
    def _create_options_section(self):
        """创建选项部分"""
        options_frame = ttk.LabelFrame(self.main_frame, text="选项", padding="5")
        options_frame.pack(fill=tk.X, pady=5)
        
        # 递归处理选项
        self.recursive_var = tk.BooleanVar(value=True)
        self.recursive_check = ttk.Checkbutton(options_frame, text="递归处理目录", variable=self.recursive_var)
        self.recursive_check.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        # 在浏览器中打开选项
        self.open_browser_var = tk.BooleanVar(value=True)
        self.open_browser_check = ttk.Checkbutton(options_frame, text="转换后打开文件夹", variable=self.open_browser_var)
        self.open_browser_check.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
    def _create_output_section(self):
        """创建输出部分"""
        output_frame = ttk.LabelFrame(self.main_frame, text="输出", padding="5")
        output_frame.pack(fill=tk.X, pady=5)
        
        # 输出标签和输入框
        ttk.Label(output_frame, text="输出目录:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_var, width=50)
        self.output_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # 浏览按钮
        self.browse_output_btn = ttk.Button(output_frame, text="浏览...", command=self._browse_output)
        self.browse_output_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # 日志文本框
        ttk.Label(output_frame, text="转换日志:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.log_frame = ttk.Frame(output_frame)
        self.log_frame.grid(row=2, column=0, columnspan=3, sticky=tk.NSEW, padx=5, pady=5)
        
        self.log_text = tk.Text(self.log_frame, height=10, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # 设置网格行列的权重
        output_frame.columnconfigure(1, weight=1)
        output_frame.rowconfigure(2, weight=1)
        
    def _create_buttons(self):
        """创建按钮部分"""
        button_frame = ttk.Frame(self.main_frame, padding="5")
        button_frame.pack(fill=tk.X, pady=10)
        
        # 转换按钮
        self.convert_btn = ttk.Button(button_frame, text="转换", command=self._start_conversion)
        self.convert_btn.pack(side=tk.RIGHT, padx=5)
        
        # 取消按钮
        self.cancel_btn = ttk.Button(button_frame, text="取消", command=self._cancel_conversion, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.RIGHT, padx=5)
        
    def _create_status_bar(self):
        """创建状态栏"""
        self.status_var = tk.StringVar(value="就绪")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def _browse_input_files(self):
        """浏览输入文件"""
        paths = filedialog.askopenfilenames(
            title="选择Markdown文件",
            filetypes=[("Markdown文件", "*.md"), ("所有文件", "*.*")]
        )
        
        if paths:  # 用户选择了文件
            # 将文件路径列表转换为字符串，以分号分隔
            path_str = ";".join(paths)
            self.input_var.set(path_str)
            
            # 自动设置默认输出路径为第一个文件的目录
            output_path = os.path.dirname(paths[0])
            self.output_var.set(output_path)
            
            # 保存配置
            self._save_config()
        
    def _browse_input_folder(self):
        """浏览输入目录"""
        path = filedialog.askdirectory(title="选择包含Markdown文件的目录")
        
        if path:
            self.input_var.set(path)
            
            # 自动设置默认输出路径
            if os.path.isfile(path):
                output_path = os.path.dirname(path)
            else:
                output_path = path
                
            self.output_var.set(output_path)
            
            # 保存配置
            self._save_config()
        
    def _browse_output(self):
        """浏览输出目录"""
        path = filedialog.askdirectory(title="选择输出目录")
        if path:
            self.output_var.set(path)
            
            # 保存配置
            self._save_config()
        
    def _log(self, message):
        """向日志添加消息"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        
    def _update_status(self, message):
        """更新状态栏"""
        self.status_var.set(message)
        
    def _toggle_controls(self, converting=False):
        """切换控件状态"""
        state = tk.DISABLED if converting else tk.NORMAL
        
        self.input_entry.config(state=state)
        self.browse_files_btn.config(state=state)
        self.browse_folder_btn.config(state=state)
        self.theme_combo.config(state="readonly" if not converting else tk.DISABLED)
        self.output_entry.config(state=state)
        self.browse_output_btn.config(state=state)
        self.convert_btn.config(state=state)
        
        self.cancel_btn.config(state=tk.NORMAL if converting else tk.DISABLED)
        
    def _start_conversion(self):
        """开始转换过程"""
        if self.is_converting:
            messagebox.showwarning("警告", "已有转换任务正在进行...")
            return
            
        # 获取输入路径
        input_path = self.input_var.get().strip()
        if not input_path:
            messagebox.showerror("错误", "请选择输入文件或目录!")
            return
            
        # 检查输入路径是否存在
        input_paths = input_path.split(";")
        for path in input_paths:
            if not os.path.exists(path):
                messagebox.showerror("错误", f"输入路径不存在: {path}")
                return
        
        # 获取输出路径
        output_path = self.output_var.get().strip()
        if not output_path:
            # 如果没有指定输出路径，默认使用输入文件所在目录
            if len(input_paths) == 1 and os.path.isfile(input_paths[0]):
                output_path = os.path.dirname(input_paths[0])
            else:
                output_path = os.path.dirname(input_paths[0]) if os.path.isfile(input_paths[0]) else input_paths[0]
            self.output_var.set(output_path)
            
        # 获取主题
        theme = self.theme_var.get()
        
        # 获取选项
        recursive = self.recursive_var.get()
        open_browser_after = self.open_browser_var.get()
        
        # 保存配置
        self._save_config()
        
        # 启动转换线程
        self._toggle_controls(converting=True)
        self._update_status("正在转换...")
        self.is_converting = True
        
        # 清空日志
        self.log_text.delete(1.0, tk.END)
        
        conversion_thread = threading.Thread(
            target=self._do_conversion,
            args=(input_path, output_path, theme, recursive, open_browser_after)
        )
        conversion_thread.daemon = True
        conversion_thread.start()
        
    def _do_conversion(self, input_path, output_path, theme, recursive, open_browser_after):
        """执行转换操作（在单独的线程中）"""
        try:
            # 创建转换器
            self.converter = MarkdownConverter(theme=theme)
            
            # 确保输出目录存在
            ensure_directory(output_path)
            
            # 检查是否是多个文件（以分号分隔）
            if ";" in input_path:
                file_paths = input_path.split(";")
                self._log(f"正在转换 {len(file_paths)} 个文件")
                
                converted_files = []
                for i, file_path in enumerate(file_paths, 1):
                    if not self.is_converting:
                        self._log("转换已取消")
                        break
                    
                    if not file_path.lower().endswith('.md'):
                        self._log(f"跳过非Markdown文件: {file_path}")
                        continue
                        
                    self._log(f"[{i}/{len(file_paths)}] 正在转换: {os.path.basename(file_path)}")
                    
                    html_path = os.path.join(output_path, os.path.basename(file_path).replace('.md', '.html'))
                    
                    # 确保输出文件所在目录存在
                    ensure_directory(os.path.dirname(html_path))
                    
                    try:
                        result = self.converter.convert_file(file_path, html_path)
                        converted_files.append(result)
                        
                        self._log(f"已创建HTML文件: {result}")
                    except Exception as e:
                        self._log(f"转换文件时出错: {str(e)}")
                
                self._log(f"完成！共转换了 {len(converted_files)} 个文件到 {output_path}")
                
                # 如果需要在浏览器中打开第一个文件
                if open_browser_after and converted_files:
                    self._log("在浏览器中打开第一个文件...")
                    try:
                        open_in_browser(converted_files[0])
                    except Exception as e:
                        self._log(f"在浏览器中打开文件时出错: {str(e)}")
            
            # 如果输入是单个文件
            elif os.path.isfile(input_path):
                self._log(f"正在转换文件: {input_path}")
                
                html_path = os.path.join(output_path, os.path.basename(input_path).replace('.md', '.html'))
                
                # 确保输出文件所在目录存在
                ensure_directory(os.path.dirname(html_path))
                
                try:
                    result = self.converter.convert_file(input_path, html_path)
                    
                    self._log(f"已创建HTML文件: {result}")
                    
                    # 如果需要在浏览器中打开
                    if open_browser_after:
                        self._log("在浏览器中打开文件...")
                        try:
                            open_in_browser(result)
                        except Exception as e:
                            self._log(f"在浏览器中打开文件时出错: {str(e)}")
                except Exception as e:
                    self._log(f"转换文件时出错: {str(e)}")
            
            # 如果输入是目录
            elif os.path.isdir(input_path):
                self._log(f"正在处理目录: {input_path}")
                
                # 复制资源文件
                self._log("复制资源文件...")
                try:
                    # 使用绝对路径避免相对路径问题
                    abs_input = os.path.abspath(input_path)
                    abs_output = os.path.abspath(output_path)
                    if abs_input == abs_output:
                        self._log("输入和输出目录相同，跳过资源复制")
                    else:
                        copy_resources(abs_input, abs_output)
                except Exception as e:
                    self._log(f"复制资源文件时出错: {str(e)}")
                    self._log("继续处理Markdown文件转换...")
                
                # 找到所有Markdown文件
                try:
                    if recursive:
                        self._log("递归查找所有Markdown文件...")
                        md_files = find_markdown_files(input_path)
                    else:
                        self._log("查找当前目录下的Markdown文件...")
                        md_files = [os.path.join(input_path, f) for f in os.listdir(input_path) 
                                   if os.path.isfile(os.path.join(input_path, f)) and f.lower().endswith('.md')]
                    
                    self._log(f"找到 {len(md_files)} 个Markdown文件")
                except Exception as e:
                    self._log(f"查找Markdown文件时出错: {str(e)}")
                    md_files = []
                
                # 转换每个文件
                converted_files = []
                for i, md_file in enumerate(md_files, 1):
                    if not self.is_converting:
                        self._log("转换已取消")
                        break
                        
                    try:
                        rel_path = os.path.relpath(md_file, input_path)
                        self._log(f"[{i}/{len(md_files)}] 正在转换: {rel_path}")
                        
                        html_file = os.path.splitext(rel_path)[0] + '.html'
                        html_path = os.path.join(output_path, html_file)
                        
                        # 确保输出子目录存在
                        ensure_directory(os.path.dirname(html_path))
                        
                        # 转换文件
                        result = self.converter.convert_file(md_file, html_path)
                        converted_files.append(result)
                    except Exception as e:
                        self._log(f"转换文件 {os.path.basename(md_file)} 时出错: {str(e)}")
                    
                self._log(f"完成！共转换了 {len(converted_files)} 个文件到 {output_path}")
                
                # 如果需要在浏览器中打开第一个文件
                if open_browser_after and converted_files:
                    self._log("在浏览器中打开第一个文件...")
                    try:
                        open_in_browser(converted_files[0])
                    except Exception as e:
                        self._log(f"在浏览器中打开文件时出错: {str(e)}")
            
            self._update_status("转换完成")
            
        except Exception as e:
            self._log(f"错误: {str(e)}")
            self._update_status("转换失败")
            
        finally:
            # 更新界面
            self.is_converting = False
            self.root.after(0, lambda: self._toggle_controls(converting=False))
    
    def _cancel_conversion(self):
        """取消转换"""
        if self.is_converting:
            self.is_converting = False
            self._update_status("转换已取消")
            self._log("正在取消转换...")
            
def main():
    """主函数"""
    root = tk.Tk()
    app = MarkdownToHtmlGUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main() 