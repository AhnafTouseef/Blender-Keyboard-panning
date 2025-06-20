#NoTrayIcon
#NoEnv
#Warn
SendMode Input
SetWorkingDir %A_ScriptDir%

; --- Configuration ---
PanDelay := 15         ; Milliseconds between pan steps (lower = smoother/faster)
MaxPanSpeed := 20      ; Max pixels to move per step
AccelerationRate := 1  ; How much the pan speed increases per step

; --- Global Variables ---
global NumpadUpPressed := false
global NumpadDownPressed := false
global NumpadLeftPressed := false
global NumpadRightPressed := false

global CurrentPanSpeedUp := 1
global CurrentPanSpeedDown := 1
global CurrentPanSpeedLeft := 1
global CurrentPanSpeedRight := 1

; --- Function to check if the mouse is currently over Blender's window ---
IsMouseOverBlender() {
    MouseGetPos, , , OutputWinID, , 2 ; Get the ID of the window under the mouse
    WinGet, processName, ProcessName, ahk_id %OutputWinID%
    Return (processName = "blender.exe")
}

; --- Shared function to stop panning for a given direction ---
StopPanning(direction) {
    global NumpadUpPressed, NumpadDownPressed, NumpadLeftPressed, NumpadRightPressed
    global CurrentPanSpeedUp, CurrentPanSpeedDown, CurrentPanSpeedLeft, CurrentPanSpeedRight

    Send {MButton Up} ; Always ensure MButton is released when stopping

    If (direction = "Up") {
        NumpadUpPressed := false
        SetTimer, PanUp, Off
        CurrentPanSpeedUp := 1
    } Else If (direction = "Down") {
        NumpadDownPressed := false
        SetTimer, PanDown, Off
        CurrentPanSpeedDown := 1
    } Else If (direction = "Left") {
        NumpadLeftPressed := false
        SetTimer, PanLeft, Off
        CurrentPanSpeedLeft := 1
    } Else If (direction = "Right") {
        NumpadRightPressed := false
        SetTimer, PanRight, Off
        CurrentPanSpeedRight := 1
    }
}




; --- NumpadUp (2) Hotkey ---
#IfWinActive ahk_exe blender.exe ; Only allow hotkey to fire if Blender is active
NumpadDown::
    If (IsMouseOverBlender()) ; ONLY proceed if mouse is over Blender
    {
        If !NumpadUpPressed
        {
            NumpadUpPressed := true
            Send {MButton down}
            CurrentPanSpeedUp := 1
            SetTimer, PanUp, %PanDelay%
        }
    } Else {
        ; If Blender is active but mouse is not over it, block the key's default action
        ; and do nothing to avoid unintended behavior in other windows.
        Return
    }
return

NumpadDown Up::
    StopPanning("Up")
return


; --- NumpadDown (8) Hotkey ---
#IfWinActive ahk_exe blender.exe
NumpadUp::
    If (IsMouseOverBlender())
    {
        If !NumpadDownPressed
        {
            NumpadDownPressed := true
            Send {MButton down}
            CurrentPanSpeedDown := 1
            SetTimer, PanDown, %PanDelay%
        }
    } Else {
        Return
    }
return

NumpadUp Up::
    StopPanning("Down")
return




; --- NumpadLeft (6) Hotkey ---
#IfWinActive ahk_exe blender.exe
NumpadRight::
    If (IsMouseOverBlender())
    {
        If !NumpadLeftPressed
        {
            NumpadLeftPressed := true
            Send {MButton down}
            CurrentPanSpeedLeft := 1
            SetTimer, PanLeft, %PanDelay%
        }
    } Else {
        Return
    }
return

NumpadRight Up::
    StopPanning("Left")
return


; --- NumpadRight (4) Hotkey ---
#IfWinActive ahk_exe blender.exe
NumpadLeft::
    If (IsMouseOverBlender())
    {
        If !NumpadRightPressed
        {
            NumpadRightPressed := true
            Send {MButton down}
            CurrentPanSpeedRight := 1
            SetTimer, PanRight, %PanDelay%
        }
    } Else {
        Return
    }
return

NumpadLeft Up::
    StopPanning("Right")
return




PanUP:
    ; Stop if key is released OR if mouse moves outside Blender's window
    If (!NumpadUpPressed || !IsMouseOverBlender()) {
        StopPanning("Up")
        Return
    }
    ; Move mouse UP to pan view UP (content moves down)
    MouseMove, 0, -%CurrentPanSpeedUp%, 0, R
    If (CurrentPanSpeedUp < MaxPanSpeed)
        CurrentPanSpeedUp += AccelerationRate
return


PanDown:
    If (!NumpadDownPressed || !IsMouseOverBlender()) {
        StopPanning("Down")
        Return
    }
    ; Move mouse DOWN to pan view DOWN (content moves up)
    MouseMove, 0, %CurrentPanSpeedDown%, 0, R
    If (CurrentPanSpeedDown < MaxPanSpeed)
        CurrentPanSpeedDown += AccelerationRate
return

PanLeft:
    If (!NumpadLeftPressed || !IsMouseOverBlender()) {
        StopPanning("Left")
        Return
    }
    ; Move mouse LEFT to pan view LEFT (content moves right)
    MouseMove, -%CurrentPanSpeedLeft%, 0, 0, R
    If (CurrentPanSpeedLeft < MaxPanSpeed)
        CurrentPanSpeedLeft += AccelerationRate
return


PanRight:
    If (!NumpadRightPressed || !IsMouseOverBlender()) {
        StopPanning("Right")
        Return
    }
    ; Move mouse RIGHT to pan view RIGHT (content moves left)
    MouseMove, %CurrentPanSpeedRight%, 0, 0, R
    If (CurrentPanSpeedRight < MaxPanSpeed)
        CurrentPanSpeedRight += AccelerationRate
return


