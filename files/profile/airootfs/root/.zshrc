dialog --title 'CambonOS Installer' --msgbox 'Welcome to the CambonOS installer. This is a live environment and any changes made here will not persist after reboot. Please ensure you have a stable internet connection before proceeding with the installation.' 8 76 || true

systemctl start NetworkManager.service >/dev/null 2>&1 || true
failed_network_checks=0
while true; do
	dialog --title ' CambonOS Network ' --sleep 1 --infobox '\nChecking network connection...' 5 64 || true
	if reflector -l 10 -f 5 --save /etc/pacman.d/mirrorlist; then
		break
	fi

	((failed_network_checks += 1))
	if ((failed_network_checks >= 5)); then
		dialog --title ' CambonOS Network ' --msgbox '\nNetwork is still unavailable. Configure it with nmtui.' 8 76 || true
		nmtui || true
		failed_network_checks=0
	fi
done

alias cambonos-installer="
if ! pacman -Syu --noconfirm cambonos-installer >/dev/null 2>&1; then
	dialog --title ' CambonOS Installer ' --msgbox '\nCould not update cambonos-installer from the CambonOS repository.' 8 76 || true
else
	/usr/bin/cambonos-installer
fi
"

cambonos-installer

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
