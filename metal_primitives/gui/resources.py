from pathlib import Path


def mod_root() -> Path:
    # .../Mod/MetalPrimitives
    return Path(__file__).resolve().parents[2]


def icons_dir() -> Path:
    return mod_root() / "metal_primitives" / "gui" / "icons"


def icon_path(name: str) -> str:
    return str(icons_dir() / name)
