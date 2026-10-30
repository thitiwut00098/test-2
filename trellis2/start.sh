#!/bin/bash
# make the image's ENV (PYTHONPATH, HF_HOME, ...) visible to ssh sessions too
env | grep -E '^(PYTHONPATH|HF_HOME|HF_TOKEN|ATTN_BACKEND|OPENCV_IO_ENABLE_OPENEXR|PATH|LD_LIBRARY_PATH|CUDA_HOME|TORCH_CUDA_ARCH_LIST)=' | sed 's/^/export /' > /etc/profile.d/trellis.sh
echo '. /etc/profile.d/trellis.sh' >> /root/.bashrc
# RunPod passes the SSH public key in $PUBLIC_KEY
mkdir -p /root/.ssh /run/sshd
[ -n "$PUBLIC_KEY" ] && echo "$PUBLIC_KEY" >> /root/.ssh/authorized_keys && chmod 600 /root/.ssh/authorized_keys
ssh-keygen -A >/dev/null 2>&1; /usr/sbin/sshd
sleep infinity
