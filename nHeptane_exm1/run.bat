@CD "%~dp0"
@CALL C:\FlameMaster\Bin\bin\Source.BAT 1

@ECHO.
@ECHO.
@ECHO ###################################
@ECHO #        Running nHeptane         #
@ECHO ###################################
@ECHO.
@ECHO.

"%FM_BIN%\FlameMan.exe" -i nHeptane.input
pause