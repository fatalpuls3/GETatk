cls
echo OFF
echo OFF

echo ===============================
echo Beginning RTM Test Case Deploy
echo ===============================

:deploy
echo =================================
echo Deploying ARTT cases directories
echo =================================
c:
cd \
cd \
cd regressn
cd cases
adxzudir -x e:\000\rtmzips\%2\%1 c:\regressn\

echo =================================
echo Deploying ARTT cases complete!
echo =================================
