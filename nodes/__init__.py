"""ComfyUI-Pixal3D nodes — aggregated NODE_CLASS_MAPPINGS for register_nodes()."""

from .nodes_loader import (
    NODE_CLASS_MAPPINGS as loader_mappings,
    NODE_DISPLAY_NAME_MAPPINGS as loader_display,
)
from .nodes_inference import (
    NODE_CLASS_MAPPINGS as inference_mappings,
    NODE_DISPLAY_NAME_MAPPINGS as inference_display,
)

NODE_CLASS_MAPPINGS = {
    **loader_mappings,
    **inference_mappings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **loader_display,
    **inference_display,
}
