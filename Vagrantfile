Vagrant.configure("2") do |config|
  config.ssh.forward_agent = true
  
  config.vm.define "ditto" do |ditto|
    ditto.vm.box = "gugek/scientific-linux-7"
    ditto.vm.box_version = "7.2.0"
    ditto.vm.synced_folder "./ditto_web_api/DittoWebApi", "/home/vagrant/ditto_web_api/DittoWebApi"
    ditto.vm.synced_folder "./systemTests/testScenarios", "/home/vagrant/systemTests/testScenarios"
    ditto.vm.synced_folder "./systemTests/execution_space", "/home/vagrant/systemTests/execution_space"
    ditto.vm.network "private_network", ip: "172.28.129.160"
	
    ditto.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
    end
	
    ditto.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "dev-environment/ditto-dev.yml"
    end
  end
end
