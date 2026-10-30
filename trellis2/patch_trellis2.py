# Fixes found on the first real run (2026-10-30). Each replacement must hit, or the build stops.
import sys
R = "/opt/TRELLIS.2/trellis2/"
fixes = [
    # The model's own pipeline.json (downloaded at run time) still names gated briaai/RMBG-2.0
    (R + "pipelines/trellis2_image_to_3d.py",
     "(**args['rembg_model']['args'])",
     "(**{**args['rembg_model']['args'], 'model_name': 'ZhengPeng7/BiRefNet'})"),
    # BiRefNet loads in fp16; feed it the model's dtype and return fp32
    (R + "pipelines/rembg/BiRefNet.py",
     '.unsqueeze(0).to("cuda")',
     '.unsqueeze(0).to("cuda", dtype=next(self.model.parameters()).dtype)'),
    (R + "pipelines/rembg/BiRefNet.py",
     ".sigmoid().cpu()",
     ".sigmoid().float().cpu()"),
    # transformers 5.x keeps DINOv3 layers at model.model.layer
    (R + "modules/image_feature_extractor.py",
     "enumerate(self.model.layer)",
     'enumerate(self.model.model.layer if hasattr(self.model, "model") else self.model.layer)'),
]
for path, old, new in fixes:
    s = open(path).read()
    if old not in s:
        sys.exit(f"patch target not found in {path}: {old}")
    open(path, "w").write(s.replace(old, new))
    print("patched", path)
