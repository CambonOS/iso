# iso
ISO CambonOS

## Paquete `cambonos-mkiso`

El `PKGBUILD` construye `cambonos-mkiso` e instala el perfil ArchISO incluido
en `/usr/share/cambonos-mkiso/profile/`. El builder conserva el directorio desde el
que se ejecuta como destino predeterminado de la imagen y utiliza el perfil
empaquetado; desde un checkout sin el paquete instalado sigue usando `./files/profile/`.
El builder combina ese perfil con el perfil releng de ArchISO, añade el
repositorio CambonOS con `Required TrustedOnly`, instala
`cambonos-keyring` y `cambonos-base` en la ISO y actualiza `cambonos-installer`
antes de ejecutarlo desde el entorno live. XFCE y Qtile se preparan en `/root`
para que el instalador pueda configurarlos.

Por defecto usa el repositorio stable. Se puede seleccionar testing con:

```sh
sudo cambonos-mkiso --testing
```

Requiere root, `archiso` y conexión a Internet para clonar las fuentes de
escritorio y descargar los paquetes. Solicita el directorio de salida, usa un
directorio temporal propio y no elimina otros datos ni desinstala paquetes del
sistema anfitrión:

```sh
sudo cambonos-mkiso
```

Las antiguas opciones `-t` y `-b` no se admiten.
