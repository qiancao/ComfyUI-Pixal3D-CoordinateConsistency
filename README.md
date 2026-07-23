> [!WARNING]
> Warning, uses experimental package `comfy-env` to attempt a one click isolated install. Will download and use pixi package manager.

# ComfyUI-Pixal3D

## Installation

Three options, in order of speed → reliability:

1. **ComfyUI Manager (recommended)** — search for `Pixal3D` in the Manager and click Install from the highest version displayed. If that doesn't work, try nightly.
2. **Manager via Git URL** — in ComfyUI Manager: "Install via Git URL" with `https://github.com/PozzettiAndrea/ComfyUI-Pixal3D.git`.
3. **Manual (most reliable)**:
   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/PozzettiAndrea/ComfyUI-Pixal3D.git
   cd ComfyUI-Pixal3D
   pip install -r requirements.txt --upgrade
   python install.py
   ```

> **Please report any problems** you hit during installation or use of my nodes — open a [Discussion](https://github.com/PozzettiAndrea/ComfyUI-Pixal3D/discussions) or [Issue](https://github.com/PozzettiAndrea/ComfyUI-Pixal3D/issues). Very grateful for your help! 🙏

---


<div align="center">
<a href="https://pozzettiandrea.github.io/ComfyUI-Pixal3D/">
<img src="https://pozzettiandrea.github.io/ComfyUI-Pixal3D/gallery-preview.png" alt="Workflow Test Gallery" width="800">
</a>
<br>
<b><a href="https://pozzettiandrea.github.io/ComfyUI-Pixal3D/">View Live Test Gallery →</a></b>
</div>

ComfyUI nodes for **Pixal3D** (SIGGRAPH 2026, TencentARC) — pixel-aligned image-to-3D generation. Single image in, textured GLB out.

- Project page: <https://ldyang694.github.io/projects/pixal3d/>
- Paper: <https://arxiv.org/abs/2605.10922>
- Upstream code: <https://github.com/TencentARC/Pixal3D>
- Model weights: <https://huggingface.co/TencentARC/Pixal3D>

## Nodes (MVP)

| Node | Purpose |
|------|---------|
| `Pixal3DLoadPipeline` | Loads the cascade pipeline + four DinoV3 cond models. Auto-downloads Pixal3D weights. |
| `Pixal3DLoadMoGe` | Loads MoGe-2 for camera-intrinsic estimation. |
| `Pixal3DPreprocessImage` | Background removal + alpha bbox crop + 1024-max resize. |
| `Pixal3DEstimateCamera` | Runs MoGe-2 to estimate camera_angle_x and distance from the input image. |
| `Pixal3DGenerate` | Runs the four-stage cascade (SS → shape LR 512 → shape HR 1024 → texture 1024). |
| `Pixal3DExtractGLB` | Extracts a textured GLB via `o_voxel.postprocess.to_glb`. Saves to `output/`. |
| `Pixal3DCoordinateTracker` | Pass-through for coordinate transform data. |
| `Pixal3DInverseTransform` | Restores global coordinates using the inverse of the preprocessing transform. |
| `Pixal3DMeshAssembler` | Merges multiple transformed meshes into one unified mesh. |

## Coordinate Consistency for Multi-Component Generation

This repository includes an extension to support generating multiple distinct components of a scene and reassembling them into a single, globally aligned 3D model.

### 1. The Problem: The Centering Assumption
The Pixal3D generator operates in a **Canonical Space**. It assumes that the subject of the input image is perfectly centered in the crop. Consequently, it implicitly maps the center of the input image to the origin $(0,0,0)$ of the 3D world. 

When generating multiple components (e.g., different parts of a machine) using separate crops, each component is generated at the origin, causing them to overlap and lose their relative spatial positions from the original image.

### 2. Technical Math
To restore the global position, we use a **Pinhole Camera Model** to invert the centering transform.

**Focal Length Recovery**
The focal length $f$ (in pixels) is derived from the horizontal FOV ($\text{fov\_x}$) and the image resolution:
$$f = \frac{16.0}{\tan(\text{fov\_x} / 2)} \cdot \frac{\text{resolution}}{32}$$

**Perspective Shift**
Let $\Delta u$ and $\Delta v$ be the pixel offsets of the crop center relative to the original image origin. For every vertex $V = (x, y, z)$ in the generated mesh, we apply a depth-dependent shift:
$$\Delta X = \frac{\Delta u \cdot Z}{f}, \quad \Delta Y = \frac{\Delta v \cdot Z}{f}$$
This ensures the transformation is a true perspective shift, maintaining pixel-alignment with the original image regardless of the vertex depth $Z$.

### 3. Our Approach
We introduce a coordinate tracking pipeline:
1. **Capture**: The preprocessing node now exports the `transform_data` (crop center, scale, and original size).
2. **Track**: A tracker node carries this data across the ComfyUI graph.
3. **Invert**: An inverse transform node applies the scale and perspective shift to the generated mesh vertices.
4. **Assemble**: An assembler node concatenates the resulting globally-aligned meshes into a single unified object.

### 4. Modifications
- **`nodes/stages.py`**: Updated `preprocess_image` to calculate and return the spatial transformation parameters (`cx`, `cy`, `scale`).
- **`nodes/nodes_inference.py`**: 
    - Updated `Pixal3DPreprocessImage` to output `PIXAL3D_TRANSFORM`.
    - Implemented `Pixal3DCoordinateTracker` for data persistence.
    - Implemented `Pixal3DInverseTransform` to execute the perspective shift math.
    - Implemented `Pixal3DMeshAssembler` to merge resulting `TRIMESH` objects.

## Hardware

- NVIDIA GPU with **SM ≥ 8.0** (Ampere/Ada/Hopper/Blackwell). flash-attn-3 has no fallback for older GPUs.
- ≥24 GB VRAM recommended for `1024_cascade` with `low_vram=True`. More for `1536_cascade`.
- ~30 GB free disk for model weights.

## Community

Questions or feature requests? Open a [Discussion](https://github.com/PozzettiAndrea/ComfyUI-Pixal3D/discussions) on GitHub.

Join the [Comfy3D Discord](https://discord.gg/bcdQCUjnHE) for help, updates, and chat about 3D workflows in ComfyUI.

## Credits

Built on the work of the Pixal3D authors (Li, Zhao, Chen, Hu, Guo, Zhang, Shan, Hu — Tsinghua / Tencent ARC / Victoria University of Wellington), Microsoft TRELLIS.2, Direct3D-S2, MoGe (Microsoft), and DINOv3 (Meta).

Built with DINOv3.

Wrapper authored by Andrea Pozzetti.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
