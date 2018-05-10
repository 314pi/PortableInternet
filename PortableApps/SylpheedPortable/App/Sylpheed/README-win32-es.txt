-------------------------------------------------------------------------------
[ Nombre         ] Sylpheed 3.7-win32
[ Desarrollador  ] Hiroyuki Yamamoto
[ Ubicaci�n      ] http://sylpheed.sraoss.jp/
[ Contacto       ] hiro-y@kcn.ne.jp
[ Necesario      ] Microsoft Windows 7 / 8 / 10
[ Categor�a      ] Cliente de correo electr�nico (software libre)
[ Compresi�n     ] ZIP
[ Redistribuci�n ] GNU GPL (ver COPYING), etc.
[ Copyright      ] (C) 1999-2018 Hiroyuki Yamamoto
-------------------------------------------------------------------------------

[ Descripci�n ]
Sylpheed es un cliente de correo electr�nico (MUA).
Es simple, ligero pero completo, y f�cil de usar.

Soporta varios protocolos, como POP3, IMAP4rev1, y NNTP.
SSL tambi�n est� soportado.

Sylpheed soporta tambi�n internacionalizaci�n (i18n) y multiples idiomas (m17n). 
Est� actualmente traducido a m�s de 29 idiomas. El procesamiento del
japon�s esta altamente soportado. Por ejemplo la deducci�n de codificaciones 
(ISO-2022-JP/EUC-JP/Shift_JIS/UTF-8), y el soporte para caracteres dependientes
del entorno.

Implementa funciones de b�squeda y filtrado avanzadas, as� como control del 
correo basura a trav�s de aprendizaje con programas externos.

Las funcionalidades de PGP est�n disponibles si se instala GnuPG.

[ Notas ]
En la versi�n actual algunas caracter�sticas disponibles en la versi�n Unix,
como las acciones, el icono en bandeja y el soporte de expresiones regulares
a�n no est�n implementadas.

Cuando informe de errores por favor, proporcione la informaci�n de la ventana
"Herramientas/Ventana de traza" o los contenidos del fichero sylpheed.log
ubicado en el directorio de configuraci�n.

[ Licencia ]
Sylpheed se distribuye bajo GNU GPL. Vea el fichero COPYING para los detalles.

Las bibliotecas GLib, GTK+, libiconv, y GPGME se distribuyen bajo to GNU LGPL. 
Vea COPYING.LIB para los detalles.

Vea LICENSE.SSL para la licencia de la biblioteca OpenSSL.

[ Instalar ]

(Versi�n con instalador)
Ejecute el fichero exe del instalador. Una vez iniciado siga las instrucciones.

(Versi�n en archivo Zip)
Descomprima el archivo zip en la ubicaci�n adecuada.
Despu�s ejecute sylpheed.exe.

Los ficheros de configuraci�n y buzones se guardan por omisi�n en la siguiente 
ubicaci�n (%APPDATA%\Sylpheed).

C:\Users\(nombre usuario)\AppData\Sylpheed

Si quiere cambiar la ubicaci�n de los ficheros de configuraci�n, puede indicarlo
como opci�n en la l�nea de �rden: --configdir "nombre de directorio".
Cree un acceso directo a sylpheed.exe y agregue la opci�n al destino del enlace
como en el siguiente ejemplo:

"C:\Program Files\Sylpheed\sylpheed.exe" --configdir "D:\Sylpheed"

Sylpheed b�sicamente no utiliza el registro, por lo que puede instalarlo en
dispositivos desmontables, como una memoria USB.

(Nota: La versi�n de instalador, pero GnuPG y GPGME usan el registro)

Si desea habilitar el control del correo basura tambi�n debe instalar bsfilter
( http://bsfilter.org/index-e.html ). Como instalaci�n f�cil puede copiar
bsfilterw.exe en el directorio en el que esta contenido sylpheed.exe.

Si desea habilitar la funcionalidad PGP debe instalar GnuPG
( http://www.gnupg.org/(en)/download/index.html#auto-ref-1 ).

Si desea registrar Sylpheed como gestor del protocolo mailto: despu�s de
haberlo instalado del archivo zip, agregue la entrada al registro haciendo
doble-clic en el fichero incluido "sylpheed-mailto-protocol.reg" (podr�
elegir esto mismo si lo instala con el instalador. Si instala Sylpheed en
una ubicaci�n diferente de C:\Program Files\Sylpheed\sylpheed.exe,
deber� modificar la ruta dentro del fichero reg.

[ Desinstalaci�n ]

(Versi�n con instalador)
Seleccione sylpheed en "Agregar o quitar programas" del Panel de control, y
pulse el bot�n "Cambiar o quitar".

(Aviso: todos los ficheros en la carpeta de instalaci�n se eliminar�n, por lo
que tenga cuidado si esta usando bsfilter, etc.)

(Versi�n en archivo Zip)
Borre todos los ficheros de la carpeta donde se descomprimi�.
Borre los ficheros de configuraci�n y buzones tambi�n si no son ya necesarios.

[ Notas adicionales ]
Sylpheed para Windows implementa la comunicaci�n inter-proceso para operaciones
remotas usando un conector TCP. Por ello el puerto 50215 de la direcci�n de
retorno (127.0.0.1) permanecer� utilizado.

