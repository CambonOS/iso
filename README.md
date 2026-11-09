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
red y servicios de pacman. Al arrancar, `reflector` actualiza la mirrorlist de
Arch y valida la conectividad tras una pausa de un segundo; tras cinco fallos se
vuelve a abrir `nmtui` y se reintenta hasta validar la conexión. La configuración live activa
los repositorios de Arch y el canal CambonOS elegido. El perfil define los hooks `mkinitcpio-archiso`
necesarios para montar y arrancar el sistema live. El builder añade el repositorio CambonOS con
`Required TrustedOnly` y actualiza `cambonos-installer` antes de ejecutarlo.
XFCE y Qtile se siguen clonando en `/root` para que el instalador pueda
configurarlos; no se instalan como escritorios del entorno live.

Por defecto usa el repositorio stable. Se puede seleccionar testing con:

```sh
sudo cambonos-mkiso --testing
```

Requiere root, `archiso`, `grub` y conexión a Internet para clonar las fuentes
de escritorio y descargar los paquetes. La imagen incluye `pacman-mirrorlist`
para los repositorios de Arch y configura `dialog` con los colores ANSI de la
paleta CambonOS. Solicita el directorio de salida, usa un directorio temporal
propio y no elimina otros datos ni desinstala paquetes del sistema anfitrión:

```sh
sudo cambonos-mkiso
```

Las antiguas opciones `-t` y `-b` no se admiten.
