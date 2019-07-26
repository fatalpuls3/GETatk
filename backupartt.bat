cls
echo OFF
echo OFF

echo ===============================
echo Beginning RTM Test Case Backup
echo ===============================
:begin
if not exist f:\rtmzips md f:\rtmzips
if not exist f:\rtmzips\archive md f:\rtmzips\archive

:usbCheck
if not exist e:\000 GOTO clearing
if not exist e:\000\rtmzips md e:\000\rtmzips
if not exist e:\000\rtmzips\%2 md e:\000\rtmzips\%2
if not exist e:\000\rtmzips\%2\archive md e:\000\rtmzips\%2\archive
echo Backup Directories Created

:clearing
echo ===============================	
echo Clearing and archiving
echo ===============================
echo Clearing f:\rtmzips\archive\
del f:\rtmzips\archive\*.*
echo Copying current backup on F to archive
copy f:\rtmzips\*.* f:\rtmzips\archive

if not exist e:\000 GOTO backup
echo Clearing e:\000\rtmzips\%2\archive\
del e:\000\rtmzips\%2\archive\*.*
echo Copying current backup on E to archive
copy e:\000\rtmzips\%2\*.* e:\000\rtmzips\%2\archive


:backup
echo =================================
echo Backing up ARTT cases directories
echo =================================
F:
cd \
cd \
cd rtmzips
cd %2
adxnszzl -c  -AD -r %1 c:\regressn\*.*

echo ============================================
echo Backing up item record file from C or D file
echo ============================================
c:
cd \
cd \
if exist c:\adx_idt1\eamitemr.dat copy c:\adx_idt1\eamitemr.dat f:\rtmzips\%2\eamitemc.dat
if exist d:\adx_idt1\eamitemr.dat copy d:\adx_idt1\eamitemr.dat f:\rtmzips\%2\eamitemd.dat

if not exist e:\000 GOTO end
echo ==========================
echo Copying files to usb drive
echo ==========================
copy f:\rtmzips\*.* e:\000\rtmzips\
goto end

:end
echo ============================================
echo RTM Artt cases backed up
echo Item file backed up
echo Location: f:\rtmzips\
if exist e:\000 echo and e:\000\rtmzips\%2
f:
cd \
cd \
cd rtmzips
echo ============================================

pause
