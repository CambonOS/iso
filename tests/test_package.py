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
        self.assertIn("pkgrel=10", build)
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
            "git",
            "mkinitcpio-archiso",
            "shadow",
            "sudo",
            "syslinux",
        ):
            self.assertIn(package, packages)
        self.assertTrue((profile / "grub" / "grub.cfg").is_file())
        self.assertTrue((profile / "syslinux" / "syslinux.cfg").is_file())
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
        self.assertIn("ping -c 1 mirror.cambonos.org", script)
        self.assertIn("nmtui || true", script)
        self.assertIn("if ! ping -c 1 mirror.cambonos.org >/dev/null 2>&1; then", script)
        self.assertIn("if ! pacman -Syu --noconfirm cambonos-installer; then", script)
        self.assertIn("\ncambonos-installer\n", script)
        self.assertTrue((ROOT / "files" / "profile" / "airootfs" / "root" / ".zshrc").is_file())
        self.assertIn("nmtui || true", (ROOT / "files" / "profile" / "airootfs" / "root" / ".zshrc").read_text())
        self.assertNotIn("installer/dialog.sh", script)
        self.assertNotIn("/tmp/FIN_ERR", script)
        self.assertNotIn("git clone https://github.com/CambonOS/installer", script)

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