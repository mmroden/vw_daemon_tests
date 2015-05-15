# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

$before_script = <<SCRIPT
  echo # vagrant profile script > /etc/profile.d/vagrant.sh
  echo export VW_COMMIT_HASH="#{ENV['VW_COMMIT_HASH']}" >> /etc/profile.d/vagrant.sh
  chmod +x /etc/profile.d/vagrant.sh
SCRIPT

$after_script = <<SCRIPT
  rm -rf /etc/profile.d/vagrant.sh
SCRIPT

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

  # if you're reprovisioning, you have to stop any running instances of vw
  config.vm.provision "shell", path: "stop_vw.sh"

  # this will fetch the git repo and then checkout the appropriate commit specified in
  # VW_COMMIT_HASH.
  config.vm.provision "shell", inline: $before_script
  config.vm.provision "shell", path: "provision.sh"
  config.vm.provision "shell", inline: $after_script

  # This next line will automatically start vw on the target box.  The tests will first kill all
  # running instances of vw if they are run, but if they are not, then the provisioned box will
  # be ready to accept incoming information.
  config.vm.provision "shell", path: "start_vw.sh"

  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
  end
end