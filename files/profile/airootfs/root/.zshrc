if ! ping -c 1 mirror.cambonos.org >/dev/null 2>&1; then
	systemctl start NetworkManager.service || true
	nmtui || true
	if ! ping -c 1 mirror.cambonos.org >/dev/null 2>&1; then
		nmtui || true
	fi
fi

if ! pacman -Syu --noconfirm cambonos-installer; then
	printf '%s\n' 'No se pudo actualizar cambonos-installer desde el repositorio CambonOS.' >&2
fi

if ! cambonos-installer; then
	dialog --title 'CambonOS Installer' --msgbox 'La instalación devolvió un error. Consulte el registro mostrado por el instalador antes de reiniciar.' 8 76 || true
fi
