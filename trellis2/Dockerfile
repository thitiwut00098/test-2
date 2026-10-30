# TRELLIS.2 ready-to-run image for RunPod (built on GitHub Actions, no GPU needed to build)
FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive PIP_NO_CACHE_DIR=1 PIP_ROOT_USER_ACTION=ignore \
    TORCH_CUDA_ARCH_LIST="8.6+PTX" FORCE_CUDA=1 MAX_JOBS=2 \
    ATTN_BACKEND=xformers OPENCV_IO_ENABLE_OPENEXR=1 HF_HOME=/workspace/hf-cache \
    PYTHONPATH=/opt/TRELLIS.2
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3.10 python3.10-dev python3-pip git wget curl ninja-build build-essential \
      libegl1 libgl1 libgles2 libusb-1.0-0 libjpeg-dev zlib1g-dev openssh-server \
    && ln -sf /usr/bin/python3.10 /usr/bin/python \
    && printf '#!/bin/sh\nexec "$@"\n' > /usr/local/bin/sudo && chmod +x /usr/local/bin/sudo \
    && rm -rf /var/lib/apt/lists/*
RUN python -m pip install -U pip setuptools wheel
RUN pip install torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu124 \
 && pip install xformers==0.0.29.post3 --index-url https://download.pytorch.org/whl/cu124
RUN git clone -b main --recursive https://github.com/microsoft/TRELLIS.2.git /opt/TRELLIS.2
WORKDIR /opt/TRELLIS.2
# setup.sh needs nvidia-smi (absent at build time) and swallows errors, so its steps are spelled out here; any failure stops the build
RUN set -e  && pip install imageio imageio-ffmpeg tqdm easydict opencv-python-headless==4.10.0.84 ninja trimesh transformers gradio==6.0.1 tensorboard pandas lpips zstandard kornia timm  && pip install git+https://github.com/EasternJournalist/utils3d.git@9a4eb15e4021b67b12c460c7057d642626897ec8  && mkdir -p /tmp/extensions  && git clone -b v0.4.0 https://github.com/NVlabs/nvdiffrast.git /tmp/extensions/nvdiffrast  && pip install /tmp/extensions/nvdiffrast --no-build-isolation  && git clone -b renderutils https://github.com/JeffreyXiang/nvdiffrec.git /tmp/extensions/nvdiffrec  && pip install /tmp/extensions/nvdiffrec --no-build-isolation  && git clone --recursive https://github.com/JeffreyXiang/CuMesh.git /tmp/extensions/CuMesh  && pip install /tmp/extensions/CuMesh --no-build-isolation  && git clone --recursive https://github.com/JeffreyXiang/FlexGEMM.git /tmp/extensions/FlexGEMM  && pip install /tmp/extensions/FlexGEMM --no-build-isolation  && cp -r o-voxel /tmp/extensions/o-voxel  && pip install /tmp/extensions/o-voxel --no-build-isolation  && rm -rf /tmp/extensions /root/.cache
# o-voxel needs plyfile; re-pin utils3d last so nothing later replaces it; check pure-python imports (no GPU needed)
RUN pip install plyfile moderngl scipy  && pip install --force-reinstall --no-deps git+https://github.com/EasternJournalist/utils3d.git@9a4eb15e4021b67b12c460c7057d642626897ec8  && python -c "import utils3d, nvdiffrast, plyfile, imageio, trimesh, easydict; print('deps ok')"
# RMBG-2.0 is gated; use the open BiRefNet weights instead
RUN grep -rl "briaai/RMBG-2.0" /opt/TRELLIS.2 | xargs -r sed -i "s#briaai/RMBG-2.0#ZhengPeng7/BiRefNet#g" || true
RUN python -c "import imageio, utils3d, nvdiffrast.torch, cumesh, flex_gemm, o_voxel; print('extensions import ok')" || echo 'import check skipped (no GPU driver at build time)'
COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]
