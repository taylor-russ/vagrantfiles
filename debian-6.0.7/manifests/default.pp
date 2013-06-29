# Default (read: test) puppet manifest for debian dev box
exec { "apt-get update":
	path => "/usr/bin",
}

# install xinit for basic window system
package { "xinit":
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

