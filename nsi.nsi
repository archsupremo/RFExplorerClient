;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Ejemplo de instalador NSIS
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;--------------------------------
;Include Modern UI

!include "MUI.nsh"

;Seleccionamos el algoritmo de compresi�n utilizado para comprimir nuestra aplicaci�n
SetCompressor lzma


;--------------------------------
;Con esta opcion alertamos al usuario y le pedimos confirmaci�n para abortar
;la instalaci�n
;Esta macro debe colocarse en esta posici�n del script sino no funcionara
!define mui_abortwarning

;Definimos el valor de la variable VERSION, en caso de no definirse en el script
;podria ser definida en el compilador
!define VERSION "0.1"

;--------------------------------
;Pages
  ;Mostramos la p�gina de bienvenida
  !insertmacro MUI_PAGE_WELCOME

  ;P�gina donde mostramos el contrato de licencia
  ;!insertmacro MUI_PAGE_LICENSE "licencia.txt"

  ;p�gina donde se muestran las distintas secciones definidas
  !insertmacro MUI_PAGE_COMPONENTS

  ;p�gina donde se selecciona el directorio donde instalar nuestra aplicacion
  !insertmacro MUI_PAGE_DIRECTORY

  ;p�gina de instalaci�n de ficheros
  !insertmacro MUI_PAGE_INSTFILES

  ;p�gina final
  !insertmacro MUI_PAGE_FINISH

;--------------------------------
;P�ginas referentes al desinstalador
  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "Spanish"

; Para generar instaladores en diferentes idiomas podemos escribir lo siguiente:
;  !insertmacro MUI_LANGUAGE ${LANGUAGE}
; De esta forma pasando la variable LANGUAGE al compilador podremos generar
; paquetes en distintos idiomas sin cambiar el script

;;;;;;;;;;;;;;;;;;;;;;;;;
; Configuration General ;
;;;;;;;;;;;;;;;;;;;;;;;;;
; Nuestro instalador se llamara si la version fuera la 1.0: Ejemplo-1.0-win32.exe
OutFile RFExplorer_Rentel-${VERSION}-win32.exe

; Aqui comprobamos que en la versi�n Inglesa se muestra correctamente el mensaje:
; Welcome to the $Name Setup Wizard

; Al tener reservado un espacio fijo para este mensaje, y al ser
; la frase en espa�ol mas larga:

; Bienvenido al Asistente de Instalaci�n de Aplicaci�n $Name
; no se ve el contenido de la variable $Name si el tama�o es muy grande

Name "Rentel"
Caption "Rentel ${VERSION} para Win32 Setup"
;Icon icono.ico

;Comprobacion de integridad del fichero activada
CRCCheck on

;Estilos visuales del XP activados
XPStyle on

/*
	Declaracion de variables a usar

*/
# tambi�n comprobamos los distintos
; tipos de comentarios que nos permite este lenguaje de script

Var PATH
Var PATH_ACCESO_DIRECTO
;Indicamos cual sera el directorio por defecto donde instalaremos nuestra
;aplicaci�n, el usuario puede cambiar este valor en tiempo de ejecuci�n.
InstallDir "$PROGRAMFILES\Rentel"

; check if the program has already been installed, if so, take this dir
; as install dir
InstallDirRegKey HKLM SOFTWARE\Rentel "Install_Dir"
;Mensaje que mostraremos para indicarle al usuario que seleccione un directorio
DirText "Elija un directorio donde instalar la aplicaci�n:"

;Indicamos que cuando la instalaci�n se complete no se cierre el instalador autom�ticamente
AutoCloseWindow false
;Mostramos todos los detalles del la instalaci�n al usuario.
ShowInstDetails show
;En caso de encontrarse los ficheros se sobreescriben
SetOverwrite on
;Optimizamos nuestro paquete en tiempo de compilaci�n, es �ltamente recomendable habilitar siempre esta opci�n
SetDatablockOptimize on
;Habilitamos la compresi�n de nuestro instalador
SetCompress auto
;Personalizamos el mensaje de desinstalaci�n
UninstallText "Super desinstalador al rescate!!!"


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Install settings                                                    ;
; En esta secci�n a�adimos los ficheros que forman nuestra aplicaci�n ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

Section "Interprete de Python y demas"
	StrCpy $PATH "Rentel"
	StrCpy $PATH_ACCESO_DIRECTO "Rentel"


	SetOutPath $INSTDIR\$PATH
	File  "python-2.7.12.msi"
	File  "PyQt4.exe"
	File  "pyqtgraph.exe"
	File  "get-pip.py"

        SetShellVarContext all

	WriteUninstaller "uninstall.exe"

;Creamos los directorios, acesos directos y claves del registro que queramos...
	CreateDirectory "$SMPROGRAMS\$PATH_ACCESO_DIRECTO"

	CreateShortCut  "$SMPROGRAMS\$PATH_ACCESO_DIRECTO\Init.lnk" \
                        "$INSTDIR\Rentel\init.py"

	CreateShortCut  "$DESKTOP\Init.lnk" \
                        "$INSTDIR\Rentel\init.py"

;Creamos tambi�n el aceso directo al desinstalador
	CreateShortCut "$SMPROGRAMS\$PATH_ACCESO_DIRECTO\Desinstalar.lnk" \
                       "$INSTDIR\uninstall.exe"

	ExecWait "$INSTDIR\Rentel\python-2.7.12.msi /s"
	ExecWait "$INSTDIR\Rentel\PyQt4.exe /s"
	ExecWait "$INSTDIR\Rentel\pyqtgraph.exe /s"

	;ReadEnvStr $R0 "PATH"
	;StrCpy $R0 "$R0;C:\EjemploDeQueEstoFunciona"
	;System::Call 'Kernel32::SetEnvironmentVariableA(t, t) i("PATH", R0).r0'


	Exec "explorer $INSTDIR\Rentel"
	;Delete "$INSTDIR\Rentel\jre.exe"

	;Exec "cmd /c reg ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f"
	;Exec "cmd /c copy $INSTDIR\Rentel\droidsansmono.ttf C:\Windows\Fonts\droidsansmono.ttf"
	;Exec 'cmd /c reg ADD "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "Droid Sans Mono Normal (TrueType)" /t REG_SZ /d droidsansmono.ttf /f'

	;Ejecuta el programa
	;Exec "$INSTDIR\Rentel\Ticket.exe"

SectionEnd

!include WriteEnvStr.nsh
Section "Add Env Var"
  !ifdef ALL_USERS
    !define ReadEnvStr_RegKey \
       'HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"'
  !else
    !define ReadEnvStr_RegKey 'HKCU "Environment"'
  !endif

  Push JAVA_HOME
  Push '${JAVA_HOME}'
  Call WriteEnvStr

  ReadEnvStr $R0 "PATH"
  messagebox mb_ok '$R0'
  ;ensure that is written valid for NT only
  ReadRegStr $0 ${ReadEnvStr_RegKey} 'JAVA_HOME'
  ReadRegStr $1 ${ReadEnvStr_RegKey} 'APP_HOME'
  StrCpy $R0 "$R0;$0;$1"
  ;or just this
  ;StrCpy $R0 "$R0;${JAVA_HOME};${APP_HOME}"
  System::Call 'Kernel32::SetEnvironmentVariableA(t, t) i("PATH", R0).r2'
  ReadEnvStr $R0 "PATH"
  messagebox mb_ok '$R0'
  writeuninstaller '$EXEDIR\uninst.exe'
SectionEnd
;;;;;;;;;;;;;;;;;;;;;;
; Uninstall settings ;
;;;;;;;;;;;;;;;;;;;;;;

Section "Uninstall"
	StrCpy $PATH "Rentel"
	StrCpy $PATH_ACCESO_DIRECTO "Rentel"
        SetShellVarContext all
	RMDir /r $SMPROGRAMS\$PATH_ACCESO_DIRECTO
	RMDir /r $INSTDIR\$PATH
	RMDir /r $INSTDIR
	Delete "$DESKTOP\Init.lnk"
	Delete "$SMPROGRAMS\$PATH_ACCESO_DIRECTO\Init.lnk"
SectionEnd
