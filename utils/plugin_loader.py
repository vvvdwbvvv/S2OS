import os
import yaml

def load_plugins(plugin_root="plugins"):
    plugins = []
    for name in os.listdir(plugin_root):
        path = os.path.join(plugin_root, name)
        meta_path = os.path.join(path, "exploit.yaml")
        so_path = os.path.join(path, f"{name}.so")
        if os.path.isfile(meta_path) and os.path.isfile(so_path):
            with open(meta_path) as f:
                meta = yaml.safe_load(f)
            meta["name"] = name
            meta["so_path"] = so_path
            plugins.append(meta)
    return plugins