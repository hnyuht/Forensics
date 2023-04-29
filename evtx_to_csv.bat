@echo off

REM Prompt user for input folders
set /p eventlogs_folder=Enter the path where the eventlogs folder: 
set /p endpoint_folder=Enter the path for the endpoint folder: 

REM Download and extract EvtxECmd.zip file
set url=https://f001.backblazeb2.com/file/EricZimmermanTools/net6/EvtxECmd.zip
set download_dir=%~dp0
set extract_dir=%~dp0\temp\extracted

echo Downloading file from %url% ...
bitsadmin.exe /transfer "Downloading EvtxECmd.zip" %url% %download_dir%\EvtxECmd.zip

echo Extracting files ...
mkdir %extract_dir%
powershell.exe -nologo -noprofile -command "Expand-Archive -LiteralPath '%download_dir%\EvtxECmd.zip' -DestinationPath '%extract_dir%'"

echo Copying EvtxECmd.exe to destination folder ...
copy /y %extract_dir%\EvtxECmd\EvtxECmd.exe %download_dir%\EvtxECmd.exe
copy /y %extract_dir%\EvtxECmd\EvtxECmd.dll %download_dir%\EvtxECmd.dll
copy /y %extract_dir%\EvtxECmd\EvtxECmd.runtimeconfig.json %download_dir%\EvtxECmd.runtimeconfig.json
copy /y %extract_dir%\EvtxECmd\Maps %download_dir%\Maps

REM Run EvtxECmd.exe
echo Running command ...
cd /d %download_dir%
start cmd /k "EvtxECmd.exe -d %eventlogs_folder% --csv %endpoint_folder% --csvf eventlogs.csv --vss"
