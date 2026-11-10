import struct
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MkisoPackageTests(unittest.TestCase):
    def test_package_metadata_and_profile(self):
        build = (ROOT / "PKGBUILD").read_text()
        script = (ROOT / "files" / "bin" / "cambonos-mkiso").read_text()
        self.assertIn("pkgname=cambonos-mkiso", build)
        self.assertIn("pkgver=0.2.1", build)
        self.assertIn("pkgrel=4", build)
        self.assertIn("'archiso'", build)
        self.assertIn("'grub'", build)
        self.assertIn("/usr/share/cambonos-mkiso/profile", build)
        self.assertIn("PACKAGED_PROFILE='/usr/share/cambonos-mkiso/profile'", script)
        self.assertIn("Required TrustedOnly", script)
        self.assertIn("https://mirror.cambonos.org/%s/$arch", script)
        self.assertIn("REPOSITORY_CHANNEL='stable'", script)
        profile = ROOT / "files" / "profile"
        package_manifest = (profile / "packages.x86_64").read_text()
        packages = package_manifest.splitlines()
        self.assertNotIn("*** Add File:", package_manifest)
        self.assertNotIn("xfce", packages)
        self.assertNotIn("qtile", packages)
        self.assertNotIn("*** Add File:", (profile / "pacman.conf").read_text())
        self.assertTrue((profile / "profiledef.sh").is_file())
        self.assertIn("'uefi.grub'", (profile / "profiledef.sh").read_text())
        self.assertIn("'bios.syslinux'", (profile / "profiledef.sh").read_text())
        for package in (
            "cambonos-base",
            "cambonos-grub",
            "cambonos-installer",
            "curl",
            "git",
            "mkinitcpio-archiso",
            "shadow",
            "sudo",
            "nano",
            "vim",
            "syslinux",
        ):
            self.assertIn(package, packages)
        self.assertTrue((profile / "grub" / "grub.cfg").is_file())
        self.assertTrue((profile / "syslinux" / "syslinux.cfg").is_file())
        syslinux_head = (profile / "syslinux" / "archiso_head.cfg").read_text()
        self.assertIn("MENU BACKGROUND splash.png", syslinux_head)
        self.assertIn("MENU COLOR title", syslinux_head)
        splash = (profile / "syslinux" / "splash.png").read_bytes()
        self.assertEqual(splash[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II", splash[16:24]), (640, 480))
        self.assertIn("copytoram=n", (profile / "syslinux" / "archiso_sys-linux.cfg").read_text())
        self.assertIn("copytoram=n", (profile / "grub" / "grub.cfg").read_text())
        self.assertIn("copytoram=n", (profile / "grub" / "loopback.cfg").read_text())
        firstboot_mask = profile / "airootfs" / "etc" / "systemd" / "system" / "systemd-firstboot.service"
        self.assertTrue(firstboot_mask.is_symlink())
        self.assertEqual(str(firstboot_mask.readlink()), "/dev/null")
        archiso_hooks = profile / "airootfs" / "etc" / "mkinitcpio.conf.d" / "archiso.conf"
        self.assertEqual(
            archiso_hooks.read_text().strip(),
            "HOOKS=(base udev modconf archiso block filesystems)",
        )
        self.assertTrue((profile / "airootfs" / "etc" / "systemd" / "system" / "pacman-init.service").is_file())
        self.assertTrue((profile / "airootfs" / "etc" / "systemd" / "system" / "multi-user.target.wants" / "pacman-init.service").is_symlink())
        self.assertTrue((profile / "airootfs" / "etc" / "systemd" / "system" / "multi-user.target.wants" / "NetworkManager.service").is_symlink())
        self.assertFalse((profile / "efiboot" / "loader" / "loader.conf").exists())
        self.assertNotIn("RELENG_PROFILE", script)
        self.assertNotIn("ensure_package", script)
        self.assertTrue((ROOT / "LICENSE").is_file())

    def test_builder_runs_only_the_installed_installer(self):
        script = (ROOT / "files" / "bin" / "cambonos-mkiso").read_text()
        self.assertNotIn("configure_live_startup", script)
        self.assertNotIn("cat > \"$PROFILE_DIR/airootfs/root/.zshrc\"", script)
        self.assertTrue((ROOT / "files" / "profile" / "airootfs" / "root" / ".zshrc").is_file())
        zshrc = (ROOT / "files" / "profile" / "airootfs" / "root" / ".zshrc").read_text()
        self.assertIn("sleep 2", zshrc)
        self.assertIn("https://geo.mirror.pkgbuild.com/core/os/x86_64/core.db", zshrc)
        self.assertIn("--programbox", zshrc)
        self.assertIn("alias cambonos-installer='update_cambonos_installer'", zshrc)
        self.assertIn("failed_network_checks=0", zshrc)
        self.assertIn("if ((failed_network_checks >= 5)); then", zshrc)
        self.assertNotIn("reflector", zshrc)
        self.assertNotIn("ping -c 1 google.com", zshrc)
        self.assertIn("systemctl start NetworkManager.service >/dev/null 2>&1 || true", zshrc)
        self.assertIn("nmtui || true", zshrc)
        self.assertLess(zshrc.index("if ((failed_network_checks >= 5)); then"), zshrc.index("nmtui || true"))
        self.assertLess(zshrc.index("nmtui || true"), zshrc.rindex("failed_network_checks=0"))
        self.assertIn("/usr/bin/cambonos-installer", zshrc)
        self.assertIn("pacman -Syu", zshrc)
        self.assertIn("clear\ncambonos-fastfetch", zshrc)
        self.assertIn("\tnmtui || true", zshrc)
        self.assertIn("alias cambonos-installer='update_cambonos_installer'", zshrc)
        self.assertIn("cambonos-fastfetch\necho", zshrc)
        self.assertIn('echo "To start the installation at any time, run:"', zshrc)
        self.assertIn('echo "To configure the network, run:"', zshrc)
        self.assertIn('echo "To shut down the system, run:"', zshrc)
        self.assertNotIn("if ! cambonos-installer; then", zshrc)
        self.assertNotIn("installer/dialog.sh", script)
        self.assertNotIn("/tmp/FIN_ERR", script)
        self.assertNotIn("git clone https://github.com/CambonOS/installer", script)

    def test_live_network_retries_nmtui_after_five_failures(self):
        zshrc = ROOT / "files" / "profile" / "airootfs" / "root" / ".zshrc"
        subprocess.run(
            [
                "bash",
                "-c",
                'network_checks=0; nmtui_calls=0; sleep_calls=0; networkmanager_started=0; '
                'dialog() { :; }; systemctl() { networkmanager_started=1; }; '
                'sleep() { test "$1" -eq 2 && sleep_calls=$((sleep_calls + 1)); }; '
                'curl() { network_checks=$((network_checks + 1)); [[ "$*" == *https://geo.mirror.pkgbuild.com/core/os/x86_64/core.db* ]] && ((network_checks > 5)); }; '
                'nmtui() { nmtui_calls=$((nmtui_calls + 1)); }; '
                'clear() { :; }; cambonos-fastfetch() { :; }; '
                'source "$1" >/dev/null; '
                'test "$network_checks" -eq 6 && test "$nmtui_calls" -eq 1 && '
                'test "$sleep_calls" -eq 1 && test "$networkmanager_started" -eq 1',
                "test-live-network",
                str(zshrc),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

    def test_installer_update_shows_pacman_output_and_preserves_failure(self):
        zshrc = ROOT / "files" / "profile" / "airootfs" / "root" / ".zshrc"
        result = subprocess.run(
            [
                "bash",
                "-c",
                'dialog() { if [[ "$*" == *--programbox* ]]; then cat; fi; }; '
                'systemctl() { :; }; sleep() { :; }; curl() { return 0; }; '
                'nmtui() { :; }; clear() { :; }; cambonos-fastfetch() { :; }; '
                'pacman() { printf "download progress\\n"; return 42; }; '
                'source "$1" >/dev/null; update_cambonos_installer; result=$?; '
                'test "$result" -eq 42',
                "test-update-progress",
                str(zshrc),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("download progress", result.stdout)

    def test_testing_option_writes_testing_repository_configuration(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            pacman_conf = Path(temporary_directory) / "pacman.conf"
            subprocess.run(
                [
                    "bash",
                    "-c",
                    'source "$1"; select_repository "$2"; append_repository_configuration "$3"',
                    "test-builder",
                    str(ROOT / "files" / "bin" / "cambonos-mkiso"),
                    "--testing",
                    str(pacman_conf),
                ],
                check=True,
            )
            self.assertEqual(
                pacman_conf.read_text(),
                "\n[cambonos-testing]\n"
                "SigLevel = Required TrustedOnly\n"
                "Server = https://mirror.cambonos.org/testing/$arch\n",
            )

    def test_no_option_keeps_stable_repository(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            pacman_conf = Path(temporary_directory) / "pacman.conf"
            subprocess.run(
                [
                    "bash",
                    "-c",
                    'source "$1"; select_repository; append_repository_configuration "$2"',
                    "test-builder",
                    str(ROOT / "files" / "bin" / "cambonos-mkiso"),
                    str(pacman_conf),
                ],
                check=True,
            )
            self.assertIn("[cambonos]\n", pacman_conf.read_text())
            self.assertIn("https://mirror.cambonos.org/stable/$arch", pacman_conf.read_text())

    def test_live_pacman_configuration_uses_arch_mirror_without_cambonos_repository(self):
        for option, repository, channel in (
            ("", "cambonos", "stable"),
            ("--testing", "cambonos-testing", "testing"),
        ):
            with self.subTest(channel=channel), tempfile.TemporaryDirectory() as temporary_directory:
                subprocess.run(
                    [
                        "bash",
                        "-c",
                        'source "$1"; PROFILE_DIR="$2"; select_repository "${3:-}"; write_live_repository_configuration',
                        "test-builder",
                        str(ROOT / "files" / "bin" / "cambonos-mkiso"),
                        temporary_directory,
                        option,
                    ],
                    check=True,
                )
                pacman_conf = Path(temporary_directory) / "airootfs" / "etc" / "pacman.conf"
                configuration = pacman_conf.read_text()
                mirror = "Server = https://geo.mirror.pkgbuild.com/$repo/os/$arch"
                self.assertIn(f"[core]\n{mirror}", configuration)
                self.assertIn(f"[extra]\n{mirror}", configuration)
                self.assertNotIn("mirrorlist", configuration)
                self.assertNotIn("[cambonos]", configuration)
                self.assertNotIn("[cambonos-testing]", configuration)
                self.assertNotIn(f"https://mirror.cambonos.org/{channel}/$arch", configuration)

    def test_builder_rejects_removed_options_without_building(self):
        for option in ("-t", "-b"):
            with self.subTest(option=option):
                result = subprocess.run(
                    [str(ROOT / "files" / "bin" / "cambonos-mkiso"), option],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 2)

    def test_builder_is_executable_from_checkout(self):
        result = subprocess.run(
            [str(ROOT / "files" / "bin" / "cambonos-mkiso"), "--help"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("[--testing]", result.stdout)

    def test_builder_sets_testing_iso_name_and_year_month_version(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            profile_directory = Path(temporary_directory) / "profile"
            profile_directory.mkdir()
            profile_def = profile_directory / "profiledef.sh"
            profile_def.write_text(
                '#!/usr/bin/env bash\n'
                'iso_name="CambonOS"\n'
                'iso_label="CambonOS_$(date +%Y.%m)"\n'
                'iso_version="$(date +%Y.%m.%d)"\n'
            )
            subprocess.run(
                [
                    "bash",
                    "-c",
                    'source "$1"; PROFILE_DIR="$2"; REPOSITORY_CHANNEL="testing"; write_iso_metadata',
                    "test-builder",
                    str(ROOT / "files" / "bin" / "cambonos-mkiso"),
                    str(profile_directory),
                ],
                check=True,
            )
            content = profile_def.read_text()
            self.assertIn('iso_name="CambonOS-testing"', content)
            self.assertIn('iso_label="CambonOS-testing_$(date +%Y.%m)"', content)
            self.assertIn('iso_version="$(date +%Y.%m)"', content)

    def test_builder_does_not_remove_host_data_or_archiso(self):
        script = (ROOT / "files" / "bin" / "cambonos-mkiso").read_text()
        self.assertIn('mktemp -d /tmp/cambonos-mkiso.XXXXXX', script)
        self.assertNotIn("rm -rf /iso", script)
        self.assertNotIn("pacman --noconfirm -Rns archiso", script)

    def test_builder_and_package_have_valid_bash_syntax(self):
        for path in (ROOT / "PKGBUILD", ROOT / "files" / "bin" / "cambonos-mkiso"):
            with self.subTest(path=path.name):
                subprocess.run(["bash", "-n", str(path)], check=True)


if __name__ == "__main__":
    unittest.main()