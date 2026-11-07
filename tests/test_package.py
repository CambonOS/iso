import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MkisoPackageTests(unittest.TestCase):
    def test_package_metadata_and_profile(self):
        build = (ROOT / "PKGBUILD").read_text()
        script = (ROOT / "cambonos-mkiso").read_text()
        self.assertIn("pkgname=cambonos-mkiso", build)
        self.assertIn("/usr/share/cambonos-mkiso/iso", build)
        self.assertIn('PROFILE_SOURCE="/usr/share/cambonos-mkiso/iso"', script)
        self.assertIn('SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"', script)
        self.assertIn("Required TrustedOnly", script)
        self.assertIn("REPOSITORY_CHANNEL=stable", script)
        self.assertIn("REPOSITORY_CHANNEL=testing", script)
        self.assertIn("https://mirror.cambonos.org/%s/$arch", script)
        self.assertIn("cambonos-installer", (ROOT / "iso/packages.x86_64").read_text())
        self.assertIn("cambonos-keyring", (ROOT / "iso/packages.x86_64").read_text())
        self.assertTrue((ROOT / "iso/profiledef.sh").is_file())
        self.assertTrue((ROOT / "LICENSE").is_file())

    def test_builder_and_package_have_valid_bash_syntax(self):
        for path in (ROOT / "PKGBUILD", ROOT / "cambonos-mkiso"):
            with self.subTest(path=path.name):
                subprocess.run(["bash", "-n", str(path)], check=True)


if __name__ == "__main__":
    unittest.main()