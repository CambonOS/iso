#!/usr/bin/env bash
# shellcheck disable=SC2034

iso_name="CambonOS"
iso_label="CambonOS_$(date +%Y.%m)"
iso_publisher="CambonOS <https://github.com/CambonOS/Linux>"
iso_application="CambonOS Installer"
iso_version="$(date +%Y.%m)"
install_dir="cambonos"
buildmodes=('iso')
bootmodes=('bios.syslinux'
           'uefi.grub')
arch="x86_64"
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'xz' '-Xbcj' 'x86' '-b' '1M' '-Xdict-size' '1M')
bootstrap_tarball_compression=('zstd' '-c' '-T0' '--auto-threads=logical' '--long' '-19')
file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/root"]="0:0:750"
)
