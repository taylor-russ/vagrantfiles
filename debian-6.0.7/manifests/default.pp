# Default (read: test) puppet manifest for debian dev box
# Mirroring a test setup (done manually) for now.
# TODO:
#  - better way to create parent directories?
#  - variablize username and configure box to add user
#

######################################################
# EXEC COMMANDS
######################################################

exec { "apt-get update":
	path => "/usr/bin",
}

# ugly but works - TODO fix this later
exec{'mkdir -p /root/.idlerc':
				path => "/bin",
}

######################################################
# PACKAGES
######################################################


# install xinit for basic window system
package { "xinit":
	ensure  => present,
	require => Exec["apt-get update"],
}

# install  x11-xserver-utils 
package { "x11-xserver-utils":
	ensure  => present,
	require => Exec["apt-get update"],
}

# install  x11-xserver-utils 
package { "build-essential":
	ensure  => present,
	require => Exec["apt-get update"],
}

# install xmonad for tiling
package { "xmonad":
	ensure  => present,
	require => Exec["apt-get update"],
}

# fluxbox for fun
package { "fluxbox":
	ensure  => present,
	require => Exec["apt-get update"],
}

# ..and sakura for easy pretty colors
package { "sakura":
	ensure  => present,
	require => Exec["apt-get update"],
}

# Development - install IDLE
package { "idle":
	ensure  => present,
	require => Exec["apt-get update"],
}

# Development - install eclipse
package { "eclipse":
	ensure  => present,
	require => Exec["apt-get update"],
}

# Development - install VIM
package { "vim":
	ensure  => present,
	require => Exec["apt-get update"],
}


######################################################
# CONFIGURATION FILES
######################################################


# deploy .xinitrc to start xmonad
file { '.xinitrc':
  name          => '/root/.xinitrc',
  ensure        => present,
  source        => '/vagrant/files/xinitrc',
  owner         => root,
  group         => root,
  mode          => 0640,
}

# deploy IDLE skins to prevent eye bleeds
file { 'config-highlight.cfg':
  name          => '/root/.idlerc/config-highlight.cfg',
  ensure        => present,
  source        => '/vagrant/files/config-highlight.cfg',
  owner         => root,
  group         => root,
  mode          => 0640,
	require				=> Exec['mkdir -p /root/.idlerc'],
}

# point IDLE to correct skin
file { 'config-main.cfg':
  name          => '/root/.idlerc/config-main.cfg',
  ensure        => present,
  source        => '/vagrant/files/config-main.cfg',
  owner         => root,
  group         => root,
  mode          => 0640,
  require				=> Exec['mkdir -p /root/.idlerc'],
}