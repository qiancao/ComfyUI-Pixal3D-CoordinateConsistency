"""ComfyUI-Pixal3D prestartup script.

Builds the isolated pixi env (via comfy-env) and stages the GLB viewer.
"""

from pathlib import Path
from comfy_env import setup_env, copy_files
from comfy_3d_viewers import copy_viewer

setup_env()

SCRIPT_DIR = Path(__file__).resolve().parent
COMFYUI_DIR = SCRIPT_DIR.parent.parent

copy_viewer("viewer", SCRIPT_DIR / "web")

copy_files(SCRIPT_DIR / "assets", COMFYUI_DIR / "input")
