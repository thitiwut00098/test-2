# TRELLIS.2 ready-to-run image for RunPod (built on GitHub Actions, no GPU needed to build)
FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive PIP_NO_CACHE_DIR=1 PIP_ROOT_USER_ACTION=ignore \
    TORCH_CUDA_ARCH_LIST="8.0;8.6;8.9;9.0" FORCE_CUDA=1 \
    ATTN_BACKEND=xformers OPENCV_IO_ENABLE_OPENEXR=1 HF_HOME=/workspace/hf-cache \
    PYTHONPATH=/opt/TRELLIS.2
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3.10 python3.10-dev python3-pip git wget curl ninja-build build-essential \
      libegl1 libgl1 libgles2 libusb-1.0-0 libjpeg-dev zlib1g-dev openssh-server \
    && ln -sf /usr/bin/python3.10 /usr/bin/python \
    && printf '#!/bin/sh\nexec "$@"\n' > /usr/local/bin/sudo && chmod +x /usr/local/bin/sudo \
    && rm -rf /var/lib/apt/lists/*
RUN pip install torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu124 \
 && pip install xformers==0.0.29.post3 --index-url https://download.pytorch.org/whl/cu124
RUN git clone -b main --recursive https://github.com/microsoft/TRELLIS.2.git /opt/TRELLIS.2
WORKDIR /opt/TRELLIS.2
# setup.sh flags as in the README, minus flash-attn (hours to compile; xformers is used instead)
RUN bash -c ". ./setup.sh --basic --nvdiffrast --nvdiffrec --cumesh --o-voxel --flexgemm" \
 && pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python || true \
 && pip install opencv-python-headless==4.10.0.84 \
 && rm -rf /tmp/extensions /root/.cache
# RMBG-2.0 is gated; use the open BiRefNet weights instead
RUN grep -rl "briaai/RMBG-2.0" /opt/TRELLIS.2 | xargs -r sed -i "s#briaai/RMBG-2.0#ZhengPeng7/BiRefNet#g" || true
RUN python -c "import torch, trellis2, o_voxel; print('import ok (no GPU at build time)')" || true
COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]
