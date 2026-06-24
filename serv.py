#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
import requests
import time
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
CORS(app)

cache = {}
CACHE_DURATION = 300  # 5 minutes

def get_cached_data(key, ttl=300):
    if key in cache:
        data, timestamp = cache[key]
        if (time.time() - timestamp) < ttl:
            return data
    return None

def set_cached_data(key, data):
    cache[key] = (data, time.time())

# Mapping des symboles CoinGecko
SYMBOL_TO_ID = {
    'BTC-USD': 'bitcoin',
    'ETH-USD': 'ethereum',
    'SOL-USD': 'solana',
    'ADA-USD': 'cardano',
    'DOGE-USD': 'dogecoin',
    'XRP-USD': 'ripple',
    'BNB-USD': 'binancecoin',
    'DOT-USD': 'polkadot',
    'LINK-USD': 'chainlink',
    'SHIB-USD': 'shiba-inu',
    'PEPE-USD': 'pepe',
    'AVAX-USD': 'avalanche-2',
    'MATIC-USD': 'matic-network',
}

# Prix de base pour les chandeliers (si API échoue)
BASE_PRICES = {
    'BTC-USD': 65000,
    'ETH-USD': 3500,
    'SOL-USD': 150,
    'ADA-USD': 0.45,
    'DOGE-USD': 0.15,
    'XRP-USD': 0.52,
    'BNB-USD': 600,
    'DOT-USD': 7,
    'LINK-USD': 14,
    'SHIB-USD': 0.000025,
    'PEPE-USD': 0.000012,
    'AVAX-USD': 35,
    'MATIC-USD': 0.60,
}

def safe_float(value, default=0):
    try:
        return float(value) if value else default
    except:
        return default

def get_market_chart(coin_id, days=7):
    """Récupère les données de prix depuis CoinGecko"""
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {'vs_currency': 'usd', 'days': days, 'interval': 'hourly'}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Erreur market_chart {coin_id}: {e}")
        return None

def get_coin_info(coin_id):
    """Récupère les informations d'une crypto"""
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        params = {'localization': 'false'}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Erreur info {coin_id}: {e}")
        return None

def generate_candles(base_price, count=100, volatility=0.02):
    """Génère des chandeliers simulés"""
    candles = []
    price = base_price
    for i in range(count):
        change = (i / count) * 0.1 - 0.05  # Tendance légère
        change += (random.random() - 0.5) * volatility * 2
        open_price = price
        close_price = open_price * (1 + change)
        high_price = max(open_price, close_price) * (1 + abs(change) * 0.5)
        low_price = min(open_price, close_price) * (1 - abs(change) * 0.5)
        volume = random.randint(1000000, 100000000)

        candles.append({
            'time': int(time.time()) - (count - i) * 3600,
            'open': round(open_price, 6),
            'high': round(high_price, 6),
            'low': round(low_price, 6),
            'close': round(close_price, 6),
            'volume': volume
        })
        price = close_price

    return candles

@app.route('/api/trading/<symbol>')
def get_trading_data(symbol):
    try:
        cache_key = f"trading_{symbol}"
        cached = get_cached_data(cache_key)
        if cached:
            return jsonify(cached)

        coin_id = SYMBOL_TO_ID.get(symbol)
        if not coin_id:
            return jsonify({'error': 'Symbole non supporté'}), 404

        # Récupérer les données
        chart_data = None
        for _ in range(3):  # 3 tentatives
            chart_data = get_market_chart(coin_id, 7)
            if chart_data:
                break
            time.sleep(2)

        prices = []
        volumes = []

        if chart_data:
            prices = chart_data.get('prices', [])
            volumes = chart_data.get('total_volumes', [])

        # Si pas de données, générer des chandeliers simulés
        base_price = BASE_PRICES.get(symbol, 100)

        if not prices:
            candles = generate_candles(base_price, 150, 0.03)
            current_price = candles[-1]['close']
            prev_price = candles[-2]['close'] if len(candles) > 1 else current_price
            high = max([c['high'] for c in candles])
            low = min([c['low'] for c in candles])
            volume = sum([c['volume'] for c in candles])
            price_change = ((current_price - prev_price) / prev_price * 100) if prev_price else 0
        else:
            # Construire les chandeliers
            candles = []
            for i in range(len(prices)):
                if i == 0:
                    open_price = prices[i][1]
                    close_price = prices[i][1]
                    high_price = prices[i][1]
                    low_price = prices[i][1]
                else:
                    open_price = prices[i-1][1]
                    close_price = prices[i][1]
                    high_price = max(prices[i-1][1], prices[i][1])
                    low_price = min(prices[i-1][1], prices[i][1])

                candles.append({
                    'time': int(prices[i][0] / 1000),
                    'open': round(open_price, 6),
                    'high': round(high_price, 6),
                    'low': round(low_price, 6),
                    'close': round(close_price, 6),
                    'volume': int(volumes[i][1]) if i < len(volumes) else 0
                })

            current_price = candles[-1]['close']
            prev_price = candles[-2]['close'] if len(candles) > 1 else current_price
            high = max([c['high'] for c in candles])
            low = min([c['low'] for c in candles])
            volume = sum([c['volume'] for c in candles])
            price_change = ((current_price - prev_price) / prev_price * 100) if prev_price else 0

        # Récupérer les informations
        info_data = None
        for _ in range(3):
            info_data = get_coin_info(coin_id)
            if info_data:
                break
            time.sleep(2)

        name = symbol.replace('-USD', '')
        market_cap = 0

        if info_data:
            market_data = info_data.get('market_data', {})
            name = info_data.get('name', name)
            market_cap = safe_float(market_data.get('market_cap', {}).get('usd', 0))
            # Récupérer le vrai price_change
            price_change = safe_float(market_data.get('price_change_percentage_24h', price_change))

        result = {
            'symbol': symbol,
            'name': name,
            'exchange': 'CRYPTO',
            'currency': 'USD',
            'data': {
                '1d': {
                    'candles': candles[-200:],
                    'indicators': {
                        'ma_20': [],
                        'ma_50': [],
                        'ma_200': [],
                        'bb_upper': [],
                        'bb_lower': [],
                        'rsi': [],
                        'macd': [],
                        'macd_signal': []
                    },
                    'stats': {
                        'current_price': current_price,
                        'change': current_price - prev_price,
                        'change_percent': price_change,
                        'high': high,
                        'low': low,
                        'volume': volume,
                        'rsi_current': 50,
                        'macd_current': 0,
                        'macd_signal_current': 0
                    }
                }
            },
            'info': {
                'sector': 'Crypto',
                'industry': 'Cryptomonnaie',
                'market_cap': market_cap,
                'pe_ratio': None,
                'dividend_yield': 0,
                'beta': 0
            }
        }

        set_cached_data(cache_key, result)
        return jsonify(result)

    except Exception as e:
        print(f"Erreur trading {symbol}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/watchlist')
def get_watchlist():
    try:
        results = []
        watchlist_symbols = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'ADA-USD',
                            'DOGE-USD', 'XRP-USD', 'BNB-USD', 'DOT-USD',
                            'LINK-USD', 'SHIB-USD']

        for symbol in watchlist_symbols:
            cache_key = f"watchlist_{symbol}"
            cached = get_cached_data(cache_key, 300)
            if cached:
                results.append(cached)
                continue

            base_price = BASE_PRICES.get(symbol, 100)
            change = (random.random() - 0.5) * 10

            # Essayer de récupérer les vraies données
            coin_id = SYMBOL_TO_ID.get(symbol)
            if coin_id:
                info = get_coin_info(coin_id)
                if info:
                    market_data = info.get('market_data', {})
                    current_price = safe_float(market_data.get('current_price', {}).get('usd', base_price))
                    price_change = safe_float(market_data.get('price_change_percentage_24h', change))
                else:
                    current_price = base_price * (1 + change / 100)
                    price_change = change
            else:
                current_price = base_price * (1 + change / 100)
                price_change = change

            item = {
                'symbol': symbol,
                'name': symbol.replace('-USD', ''),
                'price': current_price,
                'change': current_price * price_change / 100,
                'changePercent': price_change,
                'currency': 'USD'
            }
            set_cached_data(cache_key, item)
            results.append(item)

        return jsonify(results)
    except Exception as e:
        print(f"Erreur watchlist: {e}")
        return jsonify([])

@app.route('/api/top-performers')
def get_top_performers():
    try:
        performers = []
        top_symbols = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'ADA-USD',
                       'DOGE-USD', 'XRP-USD', 'BNB-USD', 'DOT-USD',
                       'LINK-USD', 'SHIB-USD']

        for symbol in top_symbols:
            base_price = BASE_PRICES.get(symbol, 100)
            change = (random.random() - 0.5) * 15

            coin_id = SYMBOL_TO_ID.get(symbol)
            if coin_id:
                info = get_coin_info(coin_id)
                if info:
                    market_data = info.get('market_data', {})
                    current_price = safe_float(market_data.get('current_price', {}).get('usd', base_price))
                    price_change = safe_float(market_data.get('price_change_percentage_24h', change))
                else:
                    current_price = base_price * (1 + change / 100)
                    price_change = change
            else:
                current_price = base_price * (1 + change / 100)
                price_change = change

            performers.append({
                'symbol': symbol,
                'name': symbol.replace('-USD', ''),
                'price': current_price,
                'changePercent': price_change,
                'currency': 'USD'
            })

        performers.sort(key=lambda x: x.get('changePercent', -100), reverse=True)
        return jsonify(performers[:10])
    except Exception as e:
        print(f"Erreur top-performers: {e}")
        return jsonify([])

@app.route('/api/insights-advanced/<symbol>')
def get_insights(symbol):
    base_price = BASE_PRICES.get(symbol, 100)
    current_price = base_price * (1 + (random.random() - 0.5) * 0.1)
    price_change = (random.random() - 0.5) * 10

    coin_id = SYMBOL_TO_ID.get(symbol)
    if coin_id:
        info = get_coin_info(coin_id)
        if info:
            market_data = info.get('market_data', {})
            current_price = safe_float(market_data.get('current_price', {}).get('usd', current_price))
            price_change = safe_float(market_data.get('price_change_percentage_24h', price_change))

    return jsonify({
        'current_price': current_price,
        'volatility': abs(price_change) * 2 + 10,
        'momentum': price_change,
        'supports': [current_price * 0.95, current_price * 0.90],
        'resistances': [current_price * 1.05, current_price * 1.10],
        'predictions': [current_price * (1 + 0.01 * i) for i in range(1, 6)],
        'recommendation': 'NEUTRE' if abs(price_change) < 2 else ('ACHAT' if price_change > 0 else 'VENTE'),
        'confidence': min(90, 50 + abs(price_change) * 2),
        'stop_loss': current_price * 0.95,
        'take_profit': current_price * 1.08,
        'rsi': 50 + price_change * 0.5,
        'macd': price_change * 0.1
    })

@app.route('/api/clear-cache')
def clear_cache():
    global cache
    cache = {}
    return jsonify({'status': 'ok', 'message': 'Cache vidé avec succès'})

@app.route('/')
def index():
    return render_template('index_crypto.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)

    print("=" * 60)
    print("🚀 CRYPTO TRADER - CoinGecko Optimisé")
    print("=" * 60)
    print(f"🌐 http://localhost:5002")
    print("=" * 60)
    print("💰 Cryptomonnaies disponibles:")
    for sym in SYMBOL_TO_ID.keys():
        print(f"   {sym}")
    print("=" * 60)
    print("💡 Cache: 5 minutes")
    print("💡 Fallback: données simulées si API indisponible")
    print("=" * 60)

    import random
    app.run(host='0.0.0.0', port=5002, debug=True)
