-------------------------------------------------------------------------------
[ Nombre         ] Sylpheed 3.7-win32
[ Desarrollador  ] Hiroyuki Yamamoto
[ Ubicación      ] http://sylpheed.sraoss.jp/
[ Contacto       ] hiro-y@kcn.ne.jp
[ Necesario      ] Microsoft Windows 7 / 8 / 10
[ Categoría      ] Cliente de correo electrónico (software libre)
[ Compresión     ] ZIP
[ Redistribución ] GNU GPL (ver COPYING), etc.
[ Copyright      ] (C) 1999-2018 Hiroyuki Yamamoto
-------------------------------------------------------------------------------

[ Descripción ]
Sylpheed es un cliente de correo electrónico (MUA).
Es simple, ligero pero completo, y fácil de usar.

Soporta varios protocolos, como POP3, IMAP4rev1, y NNTP.
SSL también está soportado.

Sylpheed soporta también internacionalización (i18n) y multiples idiomas (m17n). 
Está actualmente traducido a más de 29 idiomas. El procesamiento del
japonés esta altamente soportado. Por ejemplo la deducción de codificaciones 
(ISO-2022-JP/EUC-JP/Shift_JIS/UTF-8), y el soporte para caracteres dependientes
del entorno.

Implementa funciones de búsqueda y filtrado avanzadas, así como control del 
correo basura a través de aprendizaje con programas externos.

Las funcionalidades de PGP están disponibles si se instala GnuPG.

[ Notas ]
En la versión actual algunas características disponibles en la versión Unix,
como las acciones, el icono en bandeja y el soporte de expresiones regulares
aún no están implementadas.

Cuando informe de errores por favor, proporcione la información de la ventana
"Herramientas/Ventana de traza" o los contenidos del fichero sylpheed.log
ubicado en el directorio de configuración.

[ Licencia ]
Sylpheed se distribuye bajo GNU GPL. Vea el fichero COPYING para los detalles.

Las bibliotecas GLib, GTK+, libiconv, y GPGME se distribuyen bajo to GNU LGPL. 
Vea COPYING.LIB para los detalles.

Vea LICENSE.SSL para la licencia de la biblioteca OpenSSL.

[ Instalar ]

(Versión con instalador)
Ejecute el fichero exe del instalador. Una vez iniciado siga las instrucciones.

(Versión en archivo Zip)
Descomprima el archivo zip en la ubicación adecuada.
Después ejecute sylpheed.exe.

Los ficheros de configuración y buzones se guardan por omisión en la siguiente 
ubicación (%APPDATA%\Sylpheed).

C:\Users\(nombre usuario)\AppData\Sylpheed

Si quiere cambiar la ubicación de los ficheros de configuración, puede indicarlo
como opción en la línea de órden: --configdir "nombre de directorio".
Cree un acceso directo a sylpheed.exe y agregue la opción al destino del enlace
como en el siguiente ejemplo:

"C:\Program Files\Sylpheed\sylpheed.exe" --configdir "D:\Sylpheed"

Sylpheed básicamente no utiliza el registro, por lo que puede instalarlo en
dispositivos desmontables, como una memoria USB.

(Nota: La versión de instalador, pero GnuPG y GPGME usan el registro)

Si desea habilitar el control del correo basura también debe instalar bsfilter
( http://bsfilter.org/index-e.html ). Como instalación fácil puede copiar
bsfilterw.exe en el directorio en el que esta contenido sylpheed.exe.

Si desea habilitar la funcionalidad PGP debe instalar GnuPG
( http://www.gnupg.org/(en)/download/index.html#auto-ref-1 ).

Si desea registrar Sylpheed como gestor del protocolo mailto: después de
haberlo instalado del archivo zip, agregue la entrada al registro haciendo
doble-clic en el fichero incluido "sylpheed-mailto-protocol.reg" (podrá
elegir esto mismo si lo instala con el instalador. Si instala Sylpheed en
una ubicación diferente de C:\Program Files\Sylpheed\sylpheed.exe,
deberá modificar la ruta dentro del fichero reg.

[ Desinstalación ]

(Versión con instalador)
Seleccione sylpheed en "Agregar o quitar programas" del Panel de control, y
pulse el botón "Cambiar o quitar".

(Aviso: todos los ficheros en la carpeta de instalación se eliminarán, por lo
que tenga cuidado si esta usando bsfilter, etc.)

(Versión en archivo Zip)
Borre todos los ficheros de la carpeta donde se descomprimió.
Borre los ficheros de configuración y buzones también si no son ya necesarios.

[ Notas adicionales ]
Sylpheed para Windows implementa la comunicación inter-proceso para operaciones
remotas usando un conector TCP. Por ello el puerto 50215 de la dirección de
retorno (127.0.0.1) permanecerá utilizado.

