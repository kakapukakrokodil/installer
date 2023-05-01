echo off
::Enter code to download all your dependencies
IF NOT EXIST %ALLUSERSPROFILE%\chocolatey (
@powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
)
IF NOT EXIST %ALLUSERSPROFILE%\chocolatey\lib\mingw (
choco install mingw -y
refreshenv
)