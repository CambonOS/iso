dialog --title ' CambonOS Installer ' --msgbox '\nWelcome to the CambonOS installer. This is a live environment and any changes made here will not persist after reboot.' 8 76 || true

systemctl start NetworkManager.service >/dev/null 2>&1 || true
failed_network_checks=0
while true; do
	dialog --title ' CambonOS Installer ' --sleep 1 --infobox '\nChecking network connection...' 5 64 || true
	if ping -c 1 google.com >/dev/null 2>&1; then
		break
	fi

	((failed_network_checks += 1))
	if ((failed_network_checks >= 5)); then
		dialog --title ' CambonOS Installer ' --msgbox '\nNetwork is still unavailable. Configure it with nmtui.' 8 76 || true
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
