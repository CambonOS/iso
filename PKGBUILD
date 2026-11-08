pkgname=cambonos-mkiso
pkgver=0.1.2
pkgrel=6
pkgdesc="Build CambonOS installation images from the included ArchISO profile"
arch=('any')
url="https://github.com/CambonOS/iso"
license=('GPL-3.0-only')
depends=('archiso' 'bash' 'cambonos-keyring' 'coreutils' 'git' 'pacman')

package() {
  install -Dm644 "$startdir/LICENSE" \
    "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  install -Dm755 "$startdir/cambonos-mkiso" \
    "$pkgdir/usr/bin/cambonos-mkiso"
  install -d "$pkgdir/usr/share/cambonos-mkiso/iso"
  cp -a "$startdir/iso/." "$pkgdir/usr/share/cambonos-mkiso/iso/"
}