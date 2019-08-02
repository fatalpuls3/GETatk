cls
echo OFF
echo OFF

echo ===============================
echo Beginning RTM Test Case Backup
echo ===============================
:begin
if not exist e:\000 GOTO quit
if not exist e:\000\rtmzips md e:\000\rtmzips
if not exist e:\000\rtmzips\%2 md e:\000\rtmzips\%2
if not exist e:\000\rtmzips\%2\archive md e:\000\rtmzips\%2\archive
echo Backup Directories Created


:backup
echo =================================
echo Backing up ARTT cases directories
echo =================================
e:
cd \
cd \
cd 000
cd rtmzips
cd %2
adxzudir -c %1 c:\regressn\

echo ============================================
echo Backing up item record file from C or D file
echo ============================================
c:
cd \
cd \
if exist c:\adx_idt1\eamitemr.dat copy c:\adx_idt1\eamitemr.dat e:\000\rtmzips\%2\eamitemc.dat
if exist d:\adx_idt1\eamitemr.dat copy d:\adx_idt1\eamitemr.dat e:\000\rtmzips\%2\eamitemd.dat
GOTO end

:end
echo ============================================
echo RTM Artt cases backed up
echo Item file backed up
echo Location: e:\000\rtmzips\
e:
cd \
cd \
cd 000
cd rtmzips
echo ============================================


pause
