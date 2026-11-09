if ! ping -c 1 mirror.cambonos.org >/dev/null 2>&1; then
	systemctl start NetworkManager.service || true
	dialog --title 'CambonOS Installer' --msgbox 'Fallo en la conexion de red. Se lanzara nmtui para poder configurar la conexión.' 8 76 || true
	nmtui || true
fi

if ! pacman -Syu --noconfirm cambonos-installer; then
	dialog --title 'Instalador de CambonOS' --msgbox 'No se pudo actualizar cambonos-installer desde el repositorio de CambonOS.' 8 76 || true
else
	cambonos-installer
fi

clear
cambonos-fastfetch
echo ""
echo "Para iniciar la instalación en cualquier momento, ejecuta:"
echo "    cambonos-installer"
echo ""
echo "Para configurar la red, ejecuta:"
echo "    nmtui"
echo ""
echo "Para apagar el equipo, ejecuta:"
echo "    poweroff"
echo ""
