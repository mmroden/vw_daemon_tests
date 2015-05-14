# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.network :forwarded_port, guest: 26542, host: 26542

  config.vm.provider :virtualbox do |vb|
    config.vm.box = "ubuntu/trusty64"
    vb.memory = 2048
    vb.cpus = 2  # since we'll be standing up three boxes for testing
  end

  config.vm.provider :aws do |aws, override|
    override.vm.box = "dummy"
    aws.instance_type = "m3.large"
    aws.ami = "ami-29ebb519"  # from http://cloud-images.ubuntu.com/locator/ec2/
    aws.region = "us-west-2"
    aws.availability_zone = "us-west-2a"
    aws.access_key_id = ENV['AWS_ACCESS_KEY_ID']
    aws.secret_access_key = ENV['AWS_SECRET_KEY']
    aws.keypair_name = ENV['AWS_KEY_NAME']
    aws.security_groups = [ 'endpoint', 'vagrant-dev' ]
    override.ssh.username = "ubuntu"
    override.ssh.private_key_path = ENV['AWS_KEY_PATH']
    # see http://stackoverflow.com/questions/21274437/vagrant-install-chef-client-on-top-of-base-image
    aws.block_device_mapping = [{ 'DeviceName' => '/dev/sda1', 'Ebs.VolumeSize' => 50 }]
  end

  # It's looking like we really don't want a cluster for vw, that a beefy box should even
  # be able to handle production traffic.  We'll have to determine if that's not actually true
  # during staging, though.
  config.vm.provision "shell", path: "provision.sh"
  config.vm.provision "shell", path: "start_vw.sh"

  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
  end
end