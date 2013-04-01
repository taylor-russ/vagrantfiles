Vagrantfiles
============

Vagrant files for VM deployment

Steps for use
============
1. Install vagrant (http://www.vagrantup.com/) and virtualbox (https://www.virtualbox.org/)
2. Clone the repo (git@github.com:soondobu/vagrantfiles.git)
3. git submodule init && git submodule update
4. cd into the directory of the vm you wish to launch
5. run 'vagrant up'
6. once the command finishes, you should be able to ssh to the vagrant vm/guest on the port defined in the vagrantfile.
