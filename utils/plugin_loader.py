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