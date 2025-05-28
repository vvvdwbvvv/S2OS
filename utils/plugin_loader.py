import os
import yaml
import logging

def load_plugins(plugin_root="plugins"):
    plugins = []
    # Ensure plugin_root exists
    if not os.path.exists(plugin_root):
        logging.error(f"Plugin directory not found: {os.path.abspath(plugin_root)}")
        return plugins

    for name in os.listdir(plugin_root):
        path = os.path.join(plugin_root, name)
        meta_path = os.path.join(path, "exploit.yaml")
        so_path = os.path.join(path, f"{name}.so")
        
        # Debug logging for paths
        print(f"Checking meta_path: {os.path.abspath(meta_path)}")
        print(f"Checking so_path: {os.path.abspath(so_path)}")
        
        if not os.path.isfile(meta_path):
            print(f"Missing meta file: {meta_path}")
            continue
            
        if not os.path.isfile(so_path):
            print(f"Missing SO file: {so_path}")
            continue

        try:
            with open(meta_path, 'r') as f:
                meta = yaml.safe_load(f)
                print(f"Successfully loaded meta file: {meta_path}")
                print(f"Meta content: {meta}")
        except Exception as e:
            print(f"Error loading meta file {meta_path}: {str(e)}")
            continue

        required_keys = ["success_log", "entry_function", "plugin_path"]
        for key in required_keys:
            if key not in meta:
                raise ValueError(f"[plugin_loader] Missing key `{key}` in {meta_path}")
        meta["name"] = meta.get("name", name)
        meta["so_path"] = so_path
        meta.setdefault("cve", "N/A")
        meta.setdefault("arch", "unknown")
        plugins.append(meta)
        
    return plugins

PLUGIN_YAML_PATH = os.path.join("plugins", "plugins.yaml")

def load_plugins_v2(): # read from plugins.yaml
    with open(PLUGIN_YAML_PATH, "r") as f:
        plugins = yaml.safe_load(f)
    return plugins