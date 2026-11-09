dialog --title 'CambonOS Installer' --msgbox 'Welcome to the CambonOS installer. This is a live environment and any changes made here will not persist after reboot. Please ensure you have a stable internet connection before proceeding with the installation.' 8 76 || true

if ! ping -c 1 mirror.cambonos.org >/dev/null 2>&1; then
	systemctl start NetworkManager.service >/dev/null 2>&1 || true
	dialog --title 'CambonOS Installer' --msgbox 'Network connection failed. nmtui will be launched so you can configure the connection.' 8 76 || true
	nmtui || true
fi

alias cambonos-installer="
if ! pacman -Syu --noconfirm cambonos-installer >/dev/null 2>&1; then
	dialog --title 'CambonOS Installer' --msgbox 'Could not update cambonos-installer from the CambonOS repository.' 8 76 || true
else
	/usr/bin/cambonos-installer
fi
"

clear
cambonos-fastfetch
echo ""
echo "To start the installation at any time, run:"
echo "    cambonos-installer"
echo ""
echo "To configure the network, run:"
echo "    nmtui"
echo ""
echo "To shut down the system, run:"
echo "    poweroff"
echo ""
