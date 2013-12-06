# Do an apt-get update first
execute "update package index" do
  command "apt-get update"
  ignore_failure true
  action :nothing
end.run_action(:run)

# install the desktop
package "ubuntu-desktop" do
    action [:install]
end
