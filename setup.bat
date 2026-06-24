@echo off
echo Installation de CRYPTO TRADER - Minitel Style

echo Installation des dépendances Python...
pip install -r requirements.txt

echo Installation des dépendances frontend...
call npm install chart.js

echo Copie de Chart.js...
mkdir static\js
copy node_modules\chart.js\dist\chart.umd.min.js static\js\

echo Installation terminée !
echo Lancez l'application avec : python serv_crypto.py
pause
