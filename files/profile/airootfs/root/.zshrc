if ! ping -c 1 mirror.cambonos.org >/dev/null 2>&1; then
	systemctl start NetworkManager.service || true
	dialog --title 'CambonOS Installer' --msgbox 'Fallo en la conexion de red. Se lanzara nmtui para poder configurar la conexión.' 8 76 || true
	nmtui || true
	if ! ping -c 1 mirror.cambonos.org >/dev/null 2>&1; then
		dialog --title 'CambonOS Installer' --msgbox 'La comprobación de red sigue fallando. Se lanzara nmtui de nuevo para poder configurar la conexión.' 8 76 || true
		nmtui || true
	fi
fi

if ! pacman -Syu --noconfirm cambonos-installer; then
	printf '%s\n' 'No se pudo actualizar cambonos-installer desde el repositorio CambonOS.' >&2
fi

cambonos-installer

clear
cambonos-fastfetch
echo ""
echo "  To start the installation at any time, run:"
echo "    cambonos-installer"
echo ""
echo "  To shut down the system, run:"
echo "    poweroff"
echo ""
