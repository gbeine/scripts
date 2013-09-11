@echo off
REM Automated WSUS offline update execution
REM See: http://forums.wsusoffline.net/viewtopic.php?f=7&t=120

cd \cmd

for %%i in (wxp w2k3 w2k3-x64) do (
  for %%j in (deu enu) do (
    echo Downloading updates for %%i %%j...
    call DownloadUpdates.cmd %%i %%j /includedotnet /includemsse /includewddefs /nocleanup /verify
  )
)

for %%i in (w60 w60-x64 w61 w61-x64 w62 w62-x64) do (
  echo Downloading updates for %%i glb...
  call DownloadUpdates.cmd %%i glb /includedotnet /includemsse /includewddefs /nocleanup /verify
)

for %%i in (ofc) do (
  echo Downloading updates for %%i glb...
  call DownloadUpdates.cmd %%i glb /nocleanup /verify
)

for %%i in (o2k3 o2k7 o2k10) do (
  for %%j in (deu enu) do (
    echo Downloading updates for %%i %%j...
    call DownloadUpdates.cmd %%i %%j /nocleanup /verify
  )
)

:CreateISO
for %%i in (wxp w2k3 w2k3-x64) do (
  for %%j in (deu enu) do (
    call CreateISOImage.cmd %%i %%j /includedotnet /includemsse /includewddefs
  )
)

for %%i in (w60 w60-x64 w61 w61-x64 w62 w62-x64) do (
  call CreateISOImage.cmd %%i /includedotnet /includemsse /includewddefs
)

for %%i in (ofc) do (
  for %%j in (deu enu) do (
    call CreateISOImage.cmd %%i %%j
  )
)

cd \

copy /Y iso\* I:\WSUS
