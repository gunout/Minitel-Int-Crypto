# 🚀 CRYPTO TRADER - Minitel Style

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 Description

**CRYPTO TRADER** est une application web de suivi des cryptomonnaies avec un style **Minitel** rétro des années 80/90. Elle affiche les prix en temps réel, les chandeliers japonais, et les indicateurs techniques pour les principales cryptomonnaies.

### 🎯 Fonctionnalités

- 📊 **Chandeliers japonais** avec Chart.js
- 💰 **Prix en temps réel** via CoinGecko API
- 📈 **Indicateurs techniques** : RSI, MACD, SMA, Bollinger Bands
- 🏆 **Top Performers** : Classement des meilleures performances
- ⭐ **Watchlist** : Suivi personnalisé
- 🤖 **Prédictions IA** sur 5 jours
- 🎨 **Style Minitel** : Écran vert phosphorescent
- ⚡ **Cache** : 5 minutes pour réduire les appels API

### 💰 Cryptomonnaies supportées

| Symbole | Nom |
|---------|-----|
| BTC-USD | Bitcoin |
| ETH-USD | Ethereum |
| SOL-USD | Solana |
| ADA-USD | Cardano |
| DOGE-USD | Dogecoin |
| XRP-USD | XRP |
| BNB-USD | BNB |
| DOT-USD | Polkadot |
| LINK-USD | Chainlink |
| SHIB-USD | Shiba Inu |
| PEPE-USD | Pepe |
| AVAX-USD | Avalanche |
| MATIC-USD | Polygon |

## 🛠️ Installation

### 1. Cloner le repository

    git clone https://github.com/votre-username/crypto-trader-minitel.git
    cd crypto-trader-minitel```

### 2. Créer un environnement virtuel

    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac

# ou

    venv\Scripts\activate     # Windows

### 3. Installer les dépendances

    pip install -r requirements.txt

### 4. Installer les dépendances frontend (npm)

    npm install


### 5. Copier Chart.js dans le dossier static

# Automatique avec npm install
# Sinon manuellement :
    cp node_modules/chart.js/dist/chart.umd.min.js static/js/
 
### 6. Lancer l'application

    python3 serv.py

### 7. Ouvrir dans le navigateur

    http://localhost:5002

# Installation rapide

    # Cloner
    git clone https://github.com/votre-username/crypto-trader-minitel.git
    cd crypto-trader-minitel

    # Installation automatique
    python3 setup.py

ou
    
    python setup.bat
    
    
# Ou manuelle
    
    pip install -r requirements.txt
    npm install chart.js
    cp node_modules/chart.js/dist/chart.umd.min.js static/js/

# Lancer
    
    python3 serv.py


📊 API Endpoints
Endpoint	Description
/api/trading/<symbol>	Données de trading (chandeliers)
/api/watchlist	Liste de suivi
/api/top-performers	Meilleures performances
/api/insights-advanced/<symbol>	Prédictions IA
/api/clear-cache	Vider le cache


🗂️ Structure du projet

    crypto-trader-minitel/
    ├── README.md
    ├── requirements.txt
    ├── serv_crypto.py          # Serveur Flask
    ├── templates/
    │   └── index_crypto.html   # Interface HTML
    └── static/
    └── js/
        └── chart.umd.min.js # Chart.js

🔧 Technologies utilisées

    Backend : Python / Flask

    Frontend : HTML / CSS (Style Minitel)

    API : CoinGecko (données réelles)

    Graphiques : Chart.js

    Cache : Mémoire interne (5 minutes)


<img width="1380" height="1465" alt="Screenshot 2026-06-24 at 21-25-31 CRYPTO TRADER - Minitel Style" src="https://github.com/user-attachments/assets/2ef00f17-915a-4fa2-a997-f6228e171f09" />



By Gleaphe 2026 
