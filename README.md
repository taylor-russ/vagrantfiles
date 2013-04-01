Vagrantfiles
============

Vagrant files for VM deployment

Steps for use
============
1. Install vagrant (http://www.vagrantup.com/) and virtualbox (https://www.virtualbox.org/)
2. If you are using 1.1 or later (vagrant version):

  ```bash
  $ vagrant gem install vagrant-vbguest
  ```

  If you installed vagrant using RubyGems, use:

  ```bash
  $ gem install vagrant-vbguest
  ```
3. Clone the repo (git@github.com:soondobu/vagrantfiles.git)
4. git submodule init && git submodule update
5. cd into the directory of the vm you wish to launch
6. run 'vagrant up'
7. once the command finishes, you should be able to ssh to the vagrant vm/guest on the port defined in the vagrantfile.
