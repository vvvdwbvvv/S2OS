#!/bin/bash
set -e

KERNEL_IMG="vm/buildroot-2024.02/output/images/bzImage"
ROOTFS_IMG="vm/buildroot-2024.02/output/images/rootfs.ext2"
LOG_FILE="vm/serial.log"

if [[ ! -f "$KERNEL_IMG" || ! -f "$ROOTFS_IMG" ]]; then
  echo "Cannot find kernel or rootfs image，execute build-vm.sh first"
  exit 1
fi

echo "Launch QEMU VM to simulate attack scenarios..."
echo "（Tip: Press Ctrl+A then X to exit QEMU）"
echo "------ VM OUTPUT START ------"

# Use QEMU to boot the kernel and rootfs
qemu-system-x86_64 \
  -kernel "$KERNEL_IMG" \
  -drive file="$ROOTFS_IMG",format=raw,if=virtio \
  -append "root=/dev/vda console=ttyS0" \
  -nographic \
  -virtfs local,path=./vm,mount_tag=host0,security_model=none \
  | tee "$LOG_FILE" | grep --line-buffered -m 1 "EXPLOIT_SUCCESS" \
  && echo "Attack successful! EXPLOIT_SUCCESS triggered"

echo "------ VM OUTPUT END ------"
