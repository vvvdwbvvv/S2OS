#!/bin/bash
set -e
# export PATH="/Users/eddietsai/Workspace/projects/SimSecureOS/gnu-bin:$PATH"
export TRUE=/usr/bin/true

cd vm
BR_URL="https://buildroot.org/downloads/buildroot-2024.02.tar.gz"
wget -nc $BR_URL && tar -xzf buildroot-2024.02.tar.gz

cd buildroot-2024.02
make qemu_x86_64_defconfig || make menuconfig
make TRUE=/usr/bin/true

cp output/images/rootfs.ext2 ../../vm/test_os.img
cd ../..
echo "[X] VM image ready at vm/test_os.img"
