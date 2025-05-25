import argparse
import json
import os
import sys
from datetime import datetime

import yfinance as yf


def export_ticker_data(tickers, output_dir="output", error_log="error.log"):
    os.makedirs(output_dir, exist_ok=True)
    total = len(tickers)
    any_errors = False

    with open(error_log, "a") as log:
        for i, ticker in enumerate(tickers, 1):
            try:
                print(f"📥 [{i}/{total}] Fetching data for {ticker}...")
                yf_ticker = yf.Ticker(ticker)
                info = yf_ticker.info
                result = {
                    "tickerCode": ticker,
                    "info": {
                        "companyName": info.get("companyName", "")
                    }
                }

                output_path = os.path.join(output_dir, f"{ticker}.json")
                with open(output_path, "w") as f:
                    json.dump(result, f, indent=4)

                percent = int((i / total) * 100)
                print(f"✅ Saved: {output_path} | Progress: {percent:.2f}%")
            except Exception as e:
                timestamp = datetime.now().isoformat()
                error_msg = f"[{timestamp}] Error fetching data for {ticker}: {str(e)}\n"
                log.write(error_msg)
                print(f"❌ {error_msg}", file=sys.stderr)
                any_errors = True

    print("✅ Export complete. All files processed.")
    if any_errors:
        print("⚠️ Some tickers failed. See 'errors.log' for details.")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch stock data using yfinance."
    )
    parser.add_argument(
        "--tickers", required=True, type=str,
        help="Comma-separated list of ticker symbols (e.g. AAPL, MSFT, etc.)"
    )
    args = parser.parse_args()
    ticker_list = [
        t.strip().upper()
        for t in args.tickers.split(",")
        if t.strip()
    ]
    export_ticker_data(ticker_list)
