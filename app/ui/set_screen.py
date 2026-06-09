import sys


def set_screen(screen):
    for module_name in ("__main__", "main"):
        module = sys.modules.get(module_name)
        if module is not None and hasattr(module, "current_screen"):
            module.current_screen = screen
            return

    raise RuntimeError("Unable to locate the active main module for screen switching.")