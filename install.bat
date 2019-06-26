cls
echo OFF
echo OFF

echo ==================================================
ECHO =======Welcome to the GETatk Installer============
echo Installing Getronics Automation Tool Kit for 4690
echo ==================================================
:begin
if not exist f:\tools md f:\tools
goto install

:install
copy e:\000\GETatk\*.* f:\tools
del f:\tools\install.bat
echo ==================================================
echo Installing after.bat for existing ARTT Test Cases
echo ==================================================
python2 f:\tools\artt_after.py %1
goto end

:end
echo ==================================================
echo GETatk for 4690 Installed to F:\tools
f:
cd \
cd \
cd tools
echo ==================================================

pause
