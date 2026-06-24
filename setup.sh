#!/bin/bash
# setup.sh - Installation complète pour Linux/Mac

echo "🚀 Installation de CRYPTO TRADER - Minitel Style"

# 1. Installer les dépendances Python
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# 2. Vérifier si npm est installé
if ! command -v npm &> /dev/null; then
    echo "❌ npm n'est pas installé"
    echo "📥 Installation de npm..."
    # Ubuntu/Debian
    sudo apt update
    sudo apt install npm -y
    # Ou pour Mac
    # brew install npm
fi

# 3. Installer les dépendances frontend
echo "📦 Installation des dépendances frontend..."
npm install chart.js

# 4. Créer le dossier static/js
mkdir -p static/js

# 5. Copier Chart.js
echo "📄 Copie de Chart.js..."
cp node_modules/chart.js/dist/chart.umd.min.js static/js/

echo "✅ Installation terminée !"
echo "🌐 Lancez l'application avec : python3 serv_crypto.py"
