# S2OS
![macOS](https://img.shields.io/badge/mac%20os-000000?style=plastic&logo=macos&logoColor=F0F0F0) 
![Linux](https://img.shields.io/badge/Linux-FCC624?style=plastic&logo=linux&logoColor=black)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=flat&logo=streamlit&logoColor=white)

>This guide explains how to run SimSecureOS on macOS (especially on Apple Silicon) using QEMU or Vagrant + QEMU, depending on your compatibility needs.

## Option 1: Run QEMU x86_64 VM directly on macOS

Requirements
- Homebrew
- QEMU installed via Homebrew

Command:
```
brew install qemu
```

🚀 Run the VM
If you already have vm/bzImage and vm/test_os.img:

Command:
```
./start-vm.osx.sh
```

View VM Output
Command:
```
tail -f vm/serial.log
```

Expected success message:
```
[VM] Mounted /mnt/host0
[VM] payload.txt found!
EXPLOIT_SUCCESS
```

### ⚠️ Common macOS Issues
Problem: rosetta error: unimplemented syscall
Cause: macOS kernel/QEMU syscall mismatch
Solution: Use Option 2 below

Problem: mount -t 9p fails
Cause: QEMU 9P support on macOS is flaky
Solution: Embed payload directly into rootfs via overlay

## Option 2: Use Vagrant + QEMU to run x86_64 Ubuntu VM

This option creates a clean x86 Ubuntu VM on Apple Silicon and runs QEMU inside that VM.

📦 Install Tools
Commands:
```
brew install vagrant qemu
vagrant plugin install vagrant-qemu
```

📁 Create a VM
Commands:
```
mkdir -p ~/VMs/simsecureos
cd ~/VMs/simsecureos
```

Create Vagrantfile:
```
Vagrant.configure("2") do |config|
  config.vm.box = "generic/ubuntu1804"
  config.vm.provider "qemu" do |qe|
    qe.arch = "x86_64"
    qe.machine = "q35"
    qe.cpu = "max"
    qe.net_device = "virtio-net-pci"
  end
end
```

Start and Access
Commands:
```
vagrant up --provider qemu
vagrant ssh
```

🧪 Run SimSecureOS in VM
Inside VM:
Commands:
```
cd /vagrant
sudo apt install qemu-system-x86
./start-vm.sh
```

### Transfer Built Images From Remote Server
If you built your VM image on a server:
Commands:
```
scp user@server:/path/to/bzImage ~/SimSecureOS/vm/
scp user@server:/path/to/test_os.img ~/SimSecureOS/vm/
```
Then run:
Command:
```
./start-vm.osx.sh
```

#### Tips
Manage multiple VM versions: use symlinks like ln -sf bzImage-20240526 bzImage
Customize overlays in vm-overlay/ and rebuild via ./build-vm.sh