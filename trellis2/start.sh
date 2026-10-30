#!/bin/bash
# RunPod passes the SSH public key in $PUBLIC_KEY
mkdir -p /root/.ssh /run/sshd
[ -n "$PUBLIC_KEY" ] && echo "$PUBLIC_KEY" >> /root/.ssh/authorized_keys && chmod 600 /root/.ssh/authorized_keys
ssh-keygen -A >/dev/null 2>&1; /usr/sbin/sshd
sleep infinity
