@CD "%~dp0"
@CALL C:\FlameMaster\Bin\bin\Source.BAT 1


@ECHO.
@ECHO.
@ECHO Run unsteady diffusion flames...

@ECHO.
@ECHO.
@ECHO.
@ECHO #####################################
@ECHO #    Build initialization file      #
@ECHO #####################################
@ECHO.
@ECHO.
@ECHO.

"%FM_BIN%\FlameMan.exe" -i build_ini.input

pause