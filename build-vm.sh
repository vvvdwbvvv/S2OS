#!/bin/bash
set -e

cd /app
BR_URL="https://buildroot.org/downloads/buildroot-2024.02.tar.gz"
wget -nc "$BR_URL"
tar -xzf buildroot-2024.02.tar.gz

cd buildroot-2024.02
make qemu_x86_64_defconfig

# optional: 使用自定 fragment 自動開啟 9P
# cp ../fragments/9p_support.config fragment.config
# make BR2_LINUX_KERNEL_CUSTOM_CONFIG_FRAGMENT_FILES="fragment.config" olddefconfig

make

mkdir -p /app/vm
cp output/images/rootfs.ext2 /app/vm/test_os.img
cp output/images/bzImage /app/vm/bzImage

echo "[X] VM image ready at /app/vm/test_os.img"
