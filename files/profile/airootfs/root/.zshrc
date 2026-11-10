dialog --title ' CambonOS Installer ' --msgbox '\nWelcome to the CambonOS installer. This is a live environment and any changes made here will not persist after reboot.' 8 76 || true

systemctl start NetworkManager.service >/dev/null 2>&1 || true
sleep 2
failed_network_checks=0
while true; do
	dialog --title ' CambonOS Installer ' --sleep 1 --infobox '\nChecking Arch Linux mirror connection...' 5 72 || true
	if curl --fail --silent --show-error --head --connect-timeout 5 --max-time 10 'https://geo.mirror.pkgbuild.com/core/os/x86_64/core.db' >/dev/null 2>&1; then
		break
	fi

	((failed_network_checks += 1))
	if ((failed_network_checks >= 5)); then
		dialog --title ' CambonOS Installer ' --msgbox '\nNetwork is still unavailable. Configure it with nmtui.' 8 76 || true
		nmtui || true
		failed_network_checks=0
	fi
done

update_cambonos_installer() {
	local update_dir update_pid update_status
	update_dir=$(mktemp -d) || return 1
	if ! mkfifo "$update_dir/pacman-output"; then
		rmdir -- "$update_dir"
		return 1
	fi

	pacman -Syu --noconfirm cambonos-installer >"$update_dir/pacman-output" 2>&1 &
	update_pid=$!
	dialog --title ' CambonOS Installer ' --programbox '\nUpdating CambonOS installer...' 20 76 < "$update_dir/pacman-output" || true
	wait "$update_pid"
	update_status=$?
	rm -f -- "$update_dir/pacman-output"
	rmdir -- "$update_dir"

	if ((update_status != 0)); then
		dialog --title ' CambonOS Installer ' --msgbox '\nCould not update cambonos-installer from the CambonOS repository.' 8 76 || true
		return "$update_status"
	fi
	/usr/bin/cambonos-installer
}

alias cambonos-installer='update_cambonos_installer'

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
