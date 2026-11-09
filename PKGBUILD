pkgname=cambonos-mkiso
pkgver=0.1.5
pkgrel=8
pkgdesc="Build CambonOS installation images from the included ArchISO profile"
arch=('any')
url="https://github.com/CambonOS/cambonos-mkiso"
license=('GPL-3.0-only')
depends=('archiso' 'bash' 'cambonos-keyring' 'coreutils' 'git' 'pacman')

package() {
  install -Dm644 "$startdir/LICENSE" \
    "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  install -Dm755 "$startdir/files/bin/cambonos-mkiso" \
    "$pkgdir/usr/bin/cambonos-mkiso"
  install -d "$pkgdir/usr/share/cambonos-mkiso/profile"
  cp -a "$startdir/files/profile/." "$pkgdir/usr/share/cambonos-mkiso/profile/"
}
