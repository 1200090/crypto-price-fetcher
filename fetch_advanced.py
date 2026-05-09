import ccxt
import pandas as pd
import json
from datetime import datetime
import time

# تنظیمات - میتونی بعداً عوضش کنی
SYMBOL = 'BTC/USDT'
TIMEFRAMES = ['1m', '5m', '1h']  # 1 دقیقه، 5 دقیقه، 1 ساعت
EXCHANGES = ['binance', 'kucoin', 'bybit']  # سه صرافی مختلف

def fetch_candles(exchange_id, symbol, timeframe):
    """دریافت شمع‌ها از یک صرافی"""
    try:
        # ساخت شیء صرافی
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({
            'enableRateLimit': True,
            'timeout': 30000,
        })
        
        # دریافت 100 شمع آخر
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=100)
        
        # تبدیل به جدول
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        return df
        
    except Exception as e:
        print(f"❌ خطا در {exchange_id}: {e}")
        return None

def main():
    print("🚀 شروع دریافت داده...")
    all_data = {}
    
    # دریافت از همه صرافی‌ها و همه تایم‌فریم‌ها
    for exchange_id in EXCHANGES:
        for timeframe in TIMEFRAMES:
            print(f"📥 در حال دریافت {exchange_id} - {timeframe}...")
            df = fetch_candles(exchange_id, SYMBOL, timeframe)
            
            if df is not None:
                filename = f"{exchange_id}_{timeframe}.csv"
                df.to_csv(filename, index=False)
                all_data[filename] = len(df)
                print(f"   ✅ {len(df)} شمع ذخیره شد")
    
    # ساختن فایل خلاصه
    summary = {
        'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'symbol': SYMBOL,
        'exchanges': EXCHANGES,
        'timeframes': TIMEFRAMES,
        'files': all_data
    }
    
    with open('summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n🎉 موفق! {len(all_data)} فایل ذخیره شد.")

if __name__ == "__main__":
    main()
