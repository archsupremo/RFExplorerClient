;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Ejemplo de instalador NSIS
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;--------------------------------
;Include Modern UI

!include "MUI.nsh"

;Include macros para instalacion de fuentes
!include FontReg.nsh
!include FontName.nsh
!include WinMessages.nsh

;Seleccionamos el algoritmo de compresi�n utilizado para comprimir nuestra aplicaci�n
SetCompressor lzma


;--------------------------------
;Con esta opcion alertamos al usuario y le pedimos confirmaci�n para abortar
;la instalaci�n
;Esta macro debe colocarse en esta posici�n del script sino no funcionara
!define mui_abortwarning

;Definimos el valor de la variable VERSION, en caso de no definirse en el script
;podria ser definida en el compilador
!define VERSION "1.3"

;--------------------------------
;Pages
	
  ;!define MUI_WELCOMEPAGE_TEXT "ATENCI�N: Si tiene ya el programa ejecutandose en su equipo, debe pararlo inmediatamente, si no, no se instalar� correctamente la nueva versi�n."

  !define MUI_PAGE_CUSTOMFUNCTION_LEAVE welcome_leave
  
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
  !define MUI_FINISHPAGE_TITLE "Fuentes"
  !define MUI_FINISHPAGE_TEXT "Recuerde que para poder utilizar su aplicacion correctamente, deber� tener configurado en su TPV con alguna las siguientes fuentes: \r\n\r\n- Droid Sans Mono, Fira Mono, Roboto Mono, Source Code Pro, Inconsolata o Cousine.\r\n\r\nSe recomienda encarecidamente que se escoja la primera, Droid Sans Mono."
  !define MUI_FINISHPAGE_TEXT_LARGE
  !define MUI_FINISHPAGE_RUN
  !define MUI_FINISHPAGE_RUN_FUNCTION Ticket

  !insertmacro MUI_PAGE_FINISH

;--------------------------------  
;p�ginas referentes al desinstalador
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
OutFile Rentel-${VERSION}-win32.exe

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

Section "Fonts"

	StrCpy $FONT_DIR $FONTS
	
	!insertmacro InstallTTFFont "fuentes\DroidSansMono.ttf"

	!insertmacro InstallTTFFont "fuentes\Cousine-Regular.ttf"
	
	!insertmacro InstallTTFFont "fuentes\FiraMono-Regular.ttf"
	
	!insertmacro InstallTTFFont "fuentes\Inconsolata-Regular.ttf"
	
	!insertmacro InstallTTFFont "fuentes\RobotoMono-Regular.ttf"
	
	!insertmacro InstallTTFFont "fuentes\SourceCodePro-Regular.ttf"
	
	SendMessage ${HWND_BROADCAST} ${WM_FONTCHANGE} 0 0 /TIMEOUT=5000

SectionEnd

Section "Programa"
	StrCpy $PATH "Rentel"
	StrCpy $PATH_ACCESO_DIRECTO "Rentel"
	
	
	SetOutPath $INSTDIR\$PATH
	File  "Ticket.exe"
	;File  "jre.exe"
	;File  "loading.gif"
	;File  "tray.gif"
	;File  "tep.png"
	;File  "json.json"
	;File  "droidsansmono.ttf"
	
	SetOutPath $INSTDIR\$PATH\lib
	File  "lib\*"
	
	SetOutPath $INSTDIR\$PATH\config
	File  "config\*"
	
	SetOutPath $INSTDIR\$PATH\imagenes
	File  "imagenes\*"
	
	SetOutPath $INSTDIR\$PATH\fuentes
	File  "fuentes\*"
	
	SetOutPath $INSTDIR\$PATH
	

;Hacemos que la instalaci�n se realice para todos los usuarios del sistema
        SetShellVarContext all

;Creamos los directorios, acesos directos y claves del registro que queramos...
	CreateDirectory "$SMPROGRAMS\$PATH_ACCESO_DIRECTO"
	
	CreateShortCut  "$SMPROGRAMS\$PATH_ACCESO_DIRECTO\Ticket.lnk" \
                        "$INSTDIR\Rentel\Ticket.exe"
	
	CreateShortCut  "$DESKTOP\Ticket.lnk" \
                        "$INSTDIR\Rentel\Ticket.exe"

;Creamos tambi�n el aceso directo al desinstalador
	CreateShortCut "$SMPROGRAMS\$PATH_ACCESO_DIRECTO\Desinstalar.lnk" \
                       "$INSTDIR\uninstall.exe"

        WriteRegStr HKLM \
            SOFTWARE\Microsoft\Windows\CurrentVersion\Run \
            "Rentel" "$INSTDIR\Rentel\Ticket.exe"
        
	WriteRegStr HKLM \
            SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$PATH \
            "DisplayName" "Aplicaci�n para Rentel ${VERSION}"
        WriteRegStr HKLM \
            SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$PATH \
            "UninstallString" '"$INSTDIR\uninstall.exe"'
	WriteUninstaller "uninstall.exe"

	WriteRegStr HKLM SOFTWARE\$PATH "InstallDir" $INSTDIR
	WriteRegStr HKLM SOFTWARE\$PATH "Version" "${VERSION}"
	
	;ExecWait "$INSTDIR\Rentel\jre.exe /s"
	;Exec "explorer $INSTDIR\Rentel"
	;Delete "$INSTDIR\Rentel\jre.exe"
	
	;Exec "cmd /c reg ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f"
	;Exec "cmd /c copy $INSTDIR\Rentel\droidsansmono.ttf C:\Windows\Fonts\droidsansmono.ttf"
	;Exec 'cmd /c reg ADD "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "Droid Sans Mono Normal (TrueType)" /t REG_SZ /d droidsansmono.ttf /f'
	
	;Ejecuta el programa
	;Exec "$INSTDIR\Rentel\Ticket.exe"
	
SectionEnd

Function Ticket
	Exec "$INSTDIR\Rentel\Ticket.exe"
FunctionEnd

Function welcome_leave
  MessageBox MB_OK "Si ya tiene una version anterior de este programa en su equipo ejecutandose, debe pararla, si no, no se instalarar correctamente la nueva versi�n."
  Exec "cmd /c del $TEMP\rentel2016Stop"
  Exec "cmd /c help > $TEMP\rentel2016Stop"
FunctionEnd

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
	Delete "$DESKTOP\Ticket.lnk"
	DeleteRegKey HKLM SOFTWARE\$PATH
        DeleteRegKey HKLM \
            Software\Microsoft\Windows\CurrentVersion\Uninstall\$PATH
	
	;DeleteRegKey HKLM SOFTWARE\Microsoft\Windows\CurrentVersion\Run \ "Rentel"
SectionEnd

