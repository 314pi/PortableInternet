!macro CustomCodePreInstall
	${If} ${FileExists} "$INSTDIR\Data\settings"
	${AndIfNot} ${FileExists} "$INSTDIR\Data\Downloads"
		CreateDirectory "$INSTDIR\Data\Downloads"
	${EndIf}
!macroend