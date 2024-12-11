# Citation for the usage of financial statements in python from using Polygon.io
# Date Nov/30/2024
# Adapted From
#https://www.youtube.com/watch?v=KzI97NuSFqk&t=193s

# Citation for polygon api documentation
# Date Nov/30/2024
# Adapted from
# https://polygon.io/docs/stocks/get_v2_snapshot_locale_us_markets_stocks_tickers__stocksticker

from flask import Flask, request, jsonify
from polygon import RESTClient

app = Flask(__name__)

client = RESTClient("")

@app.route('/microservice_d', methods=['GET'])
def get_revenue_gp():
    '''Get revenue and gross profit'''
    ticker = request.args.get('ticker')
    
    if not ticker:
        return jsonify({"error": "Ticker is required"})
    # Fetch financial data from Polygon API for Ticker
    data = list(client.vx.list_stock_financials(ticker=ticker, filing_date_gte='2024-01-01'))
    
    # Get income statement 
    if data:
        income_statement = data[0].financials.income_statement
        income_data = {
            "revenues": income_statement.revenues.value,
            "gross_profit": income_statement.gross_profit.value,
        }
        return jsonify(income_data)
    else:
        return jsonify({"error": "Cannot find Ticker."})

if __name__ == '__main__':
    app.run(port=50018)





