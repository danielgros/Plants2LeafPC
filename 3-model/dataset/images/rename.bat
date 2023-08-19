@echo off
setlocal EnableExtensions EnableDelayedExpansion
for %%I in ("*_*") do (
    set "FileName=%%~nI"
    ren "%%I" "!FileName:_=;!%%~xI"
)
endlocal