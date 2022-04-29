import json
import os

class JsonConfig:
    def __init__(self):
        self.json_data = None
        self.file_path = '%s/config/config.json'%(os.environ.get('HOME'))

    def get_config(self, module_name, sub_name, re_load = True):
        self.reload()
        return self.json_data[module_name][sub_name]

    def write_config(self, module_name, sub_name, value):
        self.reload()

        self.json_data[module_name][sub_name] = value
        f_d = open(self.file_path, 'w', encoding="utf-8")
        json.dump(self.json_data, f_d, indent=4)
        f_d.close()

    def reload(self):
        try:
            with open(self.file_path, 'r', encoding='utf8') as fp:
                self.json_data = json.load(fp)
                fp.close()
        except:
            self.json_data = None

jsonconfig = JsonConfig()

if __name__ == "__main__":
    pass
