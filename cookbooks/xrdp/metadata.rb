name              "xrdp"
description       "Installs xrdp for vagrant"
version           "1.0.0"

depends           "build-essential"


recipe "xrdp", "Installs XRDP"


%w{ debian ubuntu centos redhat fedora freebsd smartos }.each do |os|
  supports os
end
