import os
import yaml
import logging
from utils.fake_server import append_serial_log

def load_plugins(plugin_root="plugins"):
    plugins = []
    # Ensure plugin_root exists
    if not os.path.exists(plugin_root):
        msg = f"Plugin directory not found: {os.path.abspath(plugin_root)}"
        logging.error(msg)
        append_serial_log(msg)
        return plugins

    for name in os.listdir(plugin_root):
        path = os.path.join(plugin_root, name)
        meta_path = os.path.join(path, "exploit.yaml")
        so_path = os.path.join(path, f"{name}.so")
        
        # Debug logging for paths
        log1 = f"Checking meta_path: {os.path.abspath(meta_path)}"
        log2 = f"Checking so_path: {os.path.abspath(so_path)}"
        print(log1); append_serial_log(log1)
        print(log2); append_serial_log(log2)
        
        if not os.path.isfile(meta_path):
            msg = f"Missing meta file: {meta_path}"
            print(msg); append_serial_log(msg)
            continue
            
        if not os.path.isfile(so_path):
            msg = f"Missing SO file: {so_path}"
            print(msg); append_serial_log(msg)
            continue

        try:
            with open(meta_path, 'r') as f:
                meta = yaml.safe_load(f)
                msg1 = f"Successfully loaded meta file: {meta_path}"
                msg2 = f"Meta content: {meta}"
                print(msg1); append_serial_log(msg1)
                print(msg2); append_serial_log(msg2)
        except Exception as e:
            msg = f"Error loading meta file {meta_path}: {str(e)}"
            print(msg); append_serial_log(msg)
            continue

        required_keys = ["success_log", "entry_function", "plugin_path"]
        for key in required_keys:
            if key not in meta:
                err = f"[plugin_loader] Missing key `{key}` in {meta_path}"
                print(err); append_serial_log(err)
                raise ValueError(err)
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
