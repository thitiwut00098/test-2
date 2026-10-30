# test-2
Ready-to-run Docker images for image-to-3D models, built by GitHub Actions.
- `trellis2/` → `ghcr.io/thitiwut00098/trellis2:latest` (TRELLIS.2, xformers instead of flash-attn, BiRefNet instead of gated RMBG-2.0)

Model weights are not baked in; they download to `/workspace/hf-cache` on first run.
No keys or tokens are stored in this repo or in the image; pass them as environment variables at run time.
