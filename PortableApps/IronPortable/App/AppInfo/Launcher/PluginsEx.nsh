!include CallANSIPlugin.nsh

!define ChromePasswords::ImportPasswords `!insertmacro ChromePasswords::ImportPasswords`
!macro ChromePasswords::ImportPasswords _SOURCE _DEST _MASTERPASSWORD
	${PushAsANSI} `${_MASTERPASSWORD}`
	${PushAsUTF8} `${_DEST}`
	${PushAsUTF8} `${_SOURCE}`
	ChromePasswords::ImportPasswords ;/NOUNLOAD
!macroend

!define ChromePasswords::ExportPasswords `!insertmacro ChromePasswords::ExportPasswords`
!macro ChromePasswords::ExportPasswords _SOURCE _DEST _MASTERPASSWORD
	${PushAsANSI} `${_MASTERPASSWORD}`
	${PushAsUTF8} `${_DEST}`
	${PushAsUTF8} `${_SOURCE}`
	ChromePasswords::ExportPasswords ;/NOUNLOAD
!macroend

!define ChromePasswords::HashPassword `!insertmacro ChromePasswords::HashPassword`
!macro ChromePasswords::HashPassword _MASTERPASSWORD
	${PushAsANSI} `${_MASTERPASSWORD}`
	ChromePasswords::HashPassword ;/NOUNLOAD
	System::Call kernel32::MultiByteToWideChar(i${CP_ACP},,ts,i-1,t.s,i${NSIS_MAX_STRLEN})
!macroend

!define KillProc::FindProcesses `!insertmacro KillProc::FindProcesses`
!macro KillProc::FindProcesses
	${VarToUTF8} $0
	KillProc::FindProcesses ;/NOUNLOAD
	${VarFromANSI} $0
!macroend

!define KillProc::KillProcesses `!insertmacro KillProc::KillProcesses`
!macro KillProc::KillProcesses
	${VarToUTF8} $0
	KillProc::KillProcesses ;/NOUNLOAD
	${VarFromANSI} $0
	${VarFromANSI} $1
!macroend
