# iso
ISO CambonOS

## Paquete `cambonos-mkiso`

El `PKGBUILD` construye `cambonos-mkiso` e instala el perfil ArchISO incluido
en `/usr/share/cambonos-mkiso/profile/`. El builder conserva el directorio desde el
que se ejecuta como destino predeterminado de la imagen y utiliza el perfil
empaquetado; desde un checkout sin el paquete instalado sigue usando `./files/profile/`.
El perfil incluido es completo y se gestiona desde este repositorio; no depende
de copiar el perfil `releng` del host. Mantiene Syslinux para BIOS y usa GRUB
con el tema CambonOS para UEFI. El live contiene `cambonos-base`,
`cambonos-grub` y `cambonos-installer`, además del conjunto mínimo de arranque,
red y servicios de pacman. La live usa el mirror global de Arch
`https://geo.mirror.pkgbuild.com/$repo/os/$arch` para `[core]` y `[extra]`, sin
generar una mirrorlist al arrancar. Valida la conectividad tras una pausa de un
segundo; tras cinco fallos vuelve a abrir `nmtui` y reintenta hasta validar la
conexión. La configuración live no añade repositorios CambonOS; el builder sí
configura el canal CambonOS elegido en el perfil de construcción para resolver
los paquetes incluidos en la ISO. El perfil define los hooks `mkinitcpio-archiso`
necesarios para montar y arrancar el sistema live. El instalador incluido se
ejecuta directamente desde la imagen.
XFCE y Qtile se siguen clonando en `/root` para que el instalador pueda
configurarlos; no se instalan como escritorios del entorno live.

Por defecto usa el repositorio stable. Se puede seleccionar testing con:

```sh
sudo cambonos-mkiso --testing
```

Requiere root, `archiso`, `grub` y conexión a Internet para clonar las fuentes
de escritorio y descargar los paquetes. La configuración de Arch live no depende
de `pacman-mirrorlist` y configura `dialog` con los colores ANSI de la
paleta CambonOS. Solicita el directorio de salida, usa un directorio temporal
propio y no elimina otros datos ni desinstala paquetes del sistema anfitrión:

```sh
sudo cambonos-mkiso
```

Las antiguas opciones `-t` y `-b` no se admiten.
