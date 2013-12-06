# Do a yum update
execute "update package index" do
  command "yum update -y"
  ignore_failure true
  action :nothing
end.run_action(:run)