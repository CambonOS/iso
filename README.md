# iso
ISO CambonOS

## Paquete `cambonos-mkiso`

El `PKGBUILD` construye `cambonos-mkiso` e instala el perfil ArchISO incluido
en `/usr/share/cambonos-mkiso/iso/`. El builder conserva el directorio desde el
que se ejecuta como destino predeterminado de la imagen y utiliza el perfil
empaquetado; desde un checkout sin el paquete instalado sigue usando `./iso/`.
El perfil añade el repositorio CambonOS con `Required TrustedOnly` e instala
`cambonos-keyring` y `cambonos-installer` en la ISO. El flujo normal inicia el
launcher del paquete; `-t` y `-b` conservan la ejecución del checkout clonado para
respetar la revisión de installer seleccionada. El modo `-b` usa el repositorio
CambonOS `testing`; el modo normal y `-t` usan `stable`.

Requiere root y conexión a Internet; instala `archiso` durante la ejecución y
descarga las fuentes que el script ya clona. Se ejecuta desde un directorio de
trabajo dedicado:

```sh
sudo cambonos-mkiso
```

Las opciones actuales `-t` y `-b` se mantienen. El script elimina `/iso` al
preparar y limpiar el perfil; no lo ejecutes en un entorno donde esa ruta
contenga datos que deban conservarse.
