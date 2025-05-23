import os
import json

class ConfigManager:
    """配置管理类，负责保存和加载用户配置"""
    
    def __init__(self, config_file="config.json"):
        """初始化配置管理器"""
        self.config_file = config_file
        self.config = self._load_config()
        
    def _load_config(self):
        """加载配置"""
        default_config = {
            "theme": "elegant",
            "last_input_path": "",
            "last_output_path": "",
            "recursive": True,
            "open_folder_after": True
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # 确保合并任何缺少的默认值
                    for key, value in default_config.items():
                        if key not in loaded_config:
                            loaded_config[key] = value
                    return loaded_config
            except Exception as e:
                print(f"加载配置文件出错: {e}")
                return default_config
        else:
            return default_config
            
    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            print(f"配置已保存到 {self.config_file}")
            return True
        except Exception as e:
            print(f"保存配置出错: {e}")
            return False
            
    def get(self, key, default=None):
        """获取配置项"""
        return self.config.get(key, default)
        
    def set(self, key, value):
        """设置配置项"""
        self.config[key] = value
        
    def update(self, config_dict):
        """批量更新配置项"""
        self.config.update(config_dict)
        
    def get_all(self):
        """获取所有配置"""
        return self.config.copy() 