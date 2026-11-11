dialog --title ' CambonOS Installer ' --msgbox '\nWelcome to the CambonOS installer. This is a live environment and any changes made here will not persist after reboot.' 8 76 || true

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
