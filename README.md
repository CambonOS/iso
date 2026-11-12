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
generar una mirrorlist al arrancar. Al ejecutar el instalador, este comprueba la
red y actualiza los paquetes antes de continuar; muestra la salida de Pacman en
un diálogo y se reinicia para usar la versión instalada. Las entradas
BIOS y UEFI desactivan la copia automática de la imagen live a RAM: el medio debe
permanecer conectado durante la sesión y el arranque puede ser más lento. La
configuración live no añade repositorios CambonOS; el builder sí
configura el canal CambonOS elegido en el perfil de construcción para resolver
los paquetes incluidos en la ISO. El perfil define los hooks `mkinitcpio-archiso`
necesarios para montar y arrancar el sistema live. El instalador incluido se
ejecuta directamente desde la imagen. Para generar imágenes con este perfil debe
estar disponible en el canal elegido `cambonos-installer` 0.1.6-4 o posterior,
que incluye la preparación de red y la actualización. Publique primero esa
versión del instalador en el mismo canal.
XFCE y Qtile se siguen clonando en `/root` para que el instalador pueda
configurarlos; no se instalan como escritorios del entorno live.
Al iniciar la sesión live se muestra una advertencia de que los cambios no
persisten tras reiniciar, junto con los comandos para instalar, configurar la
red y apagar el sistema. `dialog` es una dependencia del instalador, no una
dependencia directa del perfil live.

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

## CI entre repositorios

Los pushes a `dev` y `main` ejecutan los tests de este repositorio. Si pasan,
GitHub Actions envía a `cambonos-packages` el evento `external-package-updated`
con el repositorio, la rama y el commit como metadatos. El workflow receptor de
`cambonos-packages` debe aceptar ese evento para iniciar la reconstrucción.

Configura en este repositorio el secreto `CAMBONOS_PACKAGES_DISPATCH_TOKEN` con
un fine-grained personal access token limitado al repositorio
`CambonOS/cambonos-packages` y permiso `Contents: write`. Protege las ramas
`dev` y `main`; el token solo se utiliza en el paso de notificación, después de
que terminen los tests.
