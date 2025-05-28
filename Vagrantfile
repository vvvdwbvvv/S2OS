Vagrant.configure("2") do |config|
  config.vm.box = "roboxes/ubuntu1804"

  # Remove the network configuration since QEMU provider doesn't support it
  # config.vm.network "forwarded_port", guest: 22, host: 52222

  config.vm.synced_folder ".", "/vagrant",
    type: "rsync",
    rsync__exclude: [
      ".vagrant/",
      "gnu-bin/",  # Exclude the problematic symbolic links
      ".git/",
      "*.log"
    ],
    rsync__args: ["--verbose", "--archive", "--delete", "-z", "--links"]

  config.vm.provider "qemu" do |qe|
    qe.arch = "x86_64"
    qe.machine = "q35"
    qe.cpu = "max"
    qe.net_device = "virtio-net-pci"
    
    # Configure memory and CPU
    qe.memory = "4G"
    qe.smp = "2"

    # Configure SSH port (only specify once)
    qe.ssh_port = 52222
    qe.ssh_timeout = 300

    # Add disk configuration
    qe.disk_driver = "virtio-blk-pci"
    qe.disk_size = "20G"
  end

  # Configure SSH settings
  config.ssh.username = "vagrant"
  config.ssh.password = "vagrant"
  config.ssh.insert_key = true
end