

# install the xrdp package
package "xrdp" do
    action [:install]
end

# start the service
service "xrdp" do
    action [:enable,:start]
end