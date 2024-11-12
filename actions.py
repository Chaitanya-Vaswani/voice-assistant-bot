import requests

class ActionFetchStockPrice:
    def name(self):
        return "action_fetch_stock_price"

    def run(self, stock_symbol):
        api_key = "HXQOCOECUIE7DD8K"  
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={api_key}'

        response = requests.get(url)
        data = response.json()

        if "Global Quote" in data:
            stock_price = data["Global Quote"]["05. price"]
            return f"The current price of {stock_symbol} is ${stock_price}."
        else:
            return "Sorry, I couldn't find the stock price for that symbol."
