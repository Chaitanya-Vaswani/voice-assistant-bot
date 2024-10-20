from rasa_sdk import Action,Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict, List, Dict, Any
import yfinance as yf
import requests
import matplotlib.pyplot as plt
import json  
def extract_stock_symbol_from_input(input_text: str) -> str:
    stock_symbols_list = ['MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADBE', 'AMD', 'AES', 'AFL', 'A', 'APD', 'ABNB', 'AKAM', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AMTM', 'AEE', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'AON', 'APA', 'AAPL', 'AMAT', 'APTV', 'ACGL', 'ADM', 'ANET', 'AJG', 'AIZ', 'T', 'ATO', 'ADSK', 'ADP', 'AZO', 'AVB', 'AVY', 'AXON', 'BKR', 'BALL', 'BAC', 'BAX', 'BDX', 'BRK.B', 'BBY', 'TECH', 'BIIB', 'BLK', 'BX', 'BK', 'BA', 'BKNG', 'BWA', 'BSX', 'BMY', 'AVGO', 'BR', 'BRO', 'BF.B', 'BLDR', 'BG', 'BXP', 'CHRW', 'CDNS', 'CZR', 'CPT', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CARR', 'CTLT', 'CAT', 'CBOE', 'CBRE', 'CDW', 'CE', 'COR', 'CNC', 'CNP', 'CF', 'CRL', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CAG', 'COP', 'ED', 'STZ', 'CEG', 'COO', 'CPRT', 'GLW', 'CPAY', 'CTVA', 'CSGP', 'COST', 'CTRA', 'CRWD', 'CCI', 'CSX', 'CMI', 'CVS', 'DHR', 'DRI', 'DVA', 'DAY', 'DECK', 'DE', 'DELL', 'DAL', 'DVN', 'DXCM', 'FANG', 'DLR', 'DFS', 'DG', 'DLTR', 'D', 'DPZ', 'DOV', 'DOW', 'DHI', 'DTE', 'DUK', 'DD', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'ELV', 'EMR', 'ENPH', 'ETR', 'EOG', 'EPAM', 'EQT', 'EFX', 'EQIX', 'EQR', 'ERIE', 'ESS', 'EL', 'EG', 'EVRG', 'ES', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FDS', 'FICO', 'FAST', 'FRT', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', 'FI', 'FMC', 'F', 'FTNT', 'FTV', 'FOXA', 'FOX', 'BEN', 'FCX', 'GRMN', 'IT', 'GE', 'GEHC', 'GEV', 'GEN', 'GNRC', 'GD', 'GIS', 'GM', 'GPC', 'GILD', 'GPN', 'GL', 'GDDY', 'GS', 'HAL', 'HIG', 'HAS', 'HCA', 'DOC', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ', 'HUBB', 'HUM', 'HBAN', 'HII', 'IBM', 'IEX', 'IDXX', 'ITW', 'INCY', 'IR', 'PODD', 'INTC', 'ICE', 'IFF', 'IP', 'IPG', 'INTU', 'ISRG', 'IVZ', 'INVH', 'IQV', 'IRM', 'JBHT', 'JBL', 'JKHY', 'J', 'JNJ', 'JCI', 'JPM', 'JNPR', 'K', 'KVUE', 'KDP', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KKR', 'KLAC', 'KHC', 'KR', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LDOS', 'LEN', 'LLY', 'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW', 'LULU', 'LYB', 'MTB', 'MRO', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MTCH', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'META', 'MET', 'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 'MAA', 'MRNA', 'MHK', 'MOH', 'TAP', 'MDLZ', 'MPWR', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MSCI', 'NDAQ', 'NTAP', 'NFLX', 'NEM', 'NWSA', 'NWS', 'NEE', 'NKE', 'NI', 'NDSN', 'NSC', 'NTRS', 'NOC', 'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', 'NXPI', 'ORLY', 'OXY', 'ODFL', 'OMC', 'ON', 'OKE', 'ORCL', 'OTIS', 'PCAR', 'PKG', 'PLTR', 'PANW', 'PARA', 'PH', 'PAYX', 'PAYC', 'PYPL', 'PNR', 'PEP', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PNC', 'POOL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PTC', 'PSA', 'PHM', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTX', 'O', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RVTY', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX', 'SRE', 'NOW', 'SHW', 'SPG', 'SWKS', 'SJM', 'SW', 'SNA', 'SOLV', 'SO', 'LUV', 'SWK', 'SBUX', 'STT', 'STLD', 'STE', 'SYK', 'SMCI', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR', 'TRGP', 'TGT', 'TEL', 'TDY', 'TFX', 'TER', 'TSLA', 'TXN', 'TXT', 'TMO', 'TJX', 'TSCO', 'TT', 'TDG', 'TRV', 'TRMB', 'TFC', 'TYL', 'TSN', 'USB', 'UBER', 'UDR', 'ULTA', 'UNP', 'UAL', 'UPS', 'URI', 'UNH', 'UHS', 'VLO', 'VTR', 'VLTO', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VTRS', 'VICI', 'V', 'VST', 'VMC', 'WRB', 'GWW', 'WAB', 'WBA', 'WMT', 'DIS', 'WBD', 'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WST', 'WDC', 'WY', 'WMB', 'WTW', 'WYNN', 'XEL', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZTS'] 

    words = input_text.upper().split()

    for word in words:
        if word in stock_symbols_list:
            return word

    return None

class ActionGetStockPrice(Action):
    def name(self) -> str:
        return "action_get_stock_price"

    async def run(self, dispatcher: CollectingDispatcher, tracker, domain: DomainDict) -> List[Dict[str, Any]]:
        user_input = tracker.latest_message.get('text') 
        stock_symbol = extract_stock_symbol_from_input(user_input)

        try:
            stock_data = yf.Ticker(stock_symbol).history(period='1d')
            if stock_data.empty:
                dispatcher.utter_message("An error occurred while fetching stock data.")
                return []

            price = stock_data.iloc[-1]['Close']
            dispatcher.utter_message(f"The current price of {stock_symbol} is {price}")
        except Exception as e:
            dispatcher.utter_message(f"An error occurred while fetching stock data: {str(e)}")

    

class ActionGetStockNews(Action):
    def name(self) -> str:
        return "action_get_stock_news"

    def run(self, dispatcher: CollectingDispatcher, Tracker: Tracker, domain: dict) -> list:
        api_key = "2a214762e9c644de9631c192191a7f33" 
        stock_news = self.get_stock_news(api_key)
        dispatcher.utter_message(text=stock_news)
        return []

    def get_stock_news(self, api_key, category="business", country="us", num_articles=10):
        main_url = f"https://newsapi.org/v2/top-headlines?apiKey={api_key}&category={category}&country={country}"
        try:
            response = requests.get(main_url)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles")
            if articles:
                stock_news = ""
                for article in articles[:num_articles]:
                    title = article.get("title")
                    description = article.get("description")
                    url = article.get("url")
                    if title and description and url:
                        stock_news += f"Title: {title}\nDescription: {description}\nURL: {url}\n\n"
                return stock_news
            else:
                return "No stock news articles found for the specified criteria.\n"
        except requests.exceptions.RequestException as e:
            return f"An error occurred while fetching news: {str(e)}\n"
class ActionCalculateSMA(Action):
    def name(self) -> str:
        return "action_calculate_sma"

    async def run(self, dispatcher: CollectingDispatcher, tracker, domain: DomainDict) -> List[Dict[str, Any]]:
        stock_symbol = extract_stock_symbol_from_input(tracker.latest_message.get('text'))
        window_size = 20

        try:
            stock_data = yf.Ticker(stock_symbol).history(period='1y')
            sma = stock_data['Close'].rolling(window=window_size).mean().iloc[-1]

            dispatcher.utter_message(f"The {window_size}-day Simple Moving Average (SMA) for {stock_symbol} is {sma}")
        except Exception as e:
            dispatcher.utter_message(f"An error occurred while calculating SMA: {str(e)}")


class ActionCalculateEMA(Action):
    def name(self) -> str:
        return "action_calculate_ema"

    async def run(self, dispatcher: CollectingDispatcher, tracker, domain: DomainDict) -> List[Dict[str, Any]]:
        stock_symbol = extract_stock_symbol_from_input(tracker.latest_message.get('text'))
        window_size = 20

        try:
            stock_data = yf.Ticker(stock_symbol).history(period='1y')
            ema = stock_data['Close'].ewm(span=window_size, adjust=False).mean().iloc[-1]

            dispatcher.utter_message(f"The {window_size}-day Exponential Moving Average (EMA) for {stock_symbol} is {ema}")
        except Exception as e:
            dispatcher.utter_message(f"An error occurred while calculating EMA: {str(e)}")


class ActionCalculateRSI(Action):
    def name(self) -> str:
        return "action_calculate_rsi"

    async def run(self, dispatcher: CollectingDispatcher, tracker, domain: DomainDict) -> List[Dict[str, Any]]:
        stock_symbol = extract_stock_symbol_from_input(tracker.latest_message.get('text'))

        try:
            stock_data = yf.Ticker(stock_symbol).history(period='1y')
            delta = stock_data['Close'].diff()
            up = delta.clip(lower=0)
            down = -1 * delta.clip(upper=0)
            ema_up = up.ewm(com=14-1, adjust=False).mean()
            ema_down = down.ewm(com=14-1, adjust=False).mean()
            rs = ema_up / ema_down
            rsi = 100 - (100 / (1 + rs)).iloc[-1]

            dispatcher.utter_message(f"The Relative Strength Index (RSI) for {stock_symbol} is {rsi}")
        except Exception as e:
            dispatcher.utter_message(f"An error occurred while calculating RSI: {str(e)}")

        return [SlotSet("stock_symbol", None)]

class ActionCalculateMACD(Action):
    def name(self) -> str:
        return "action_calculate_macd"

    async def run(self, dispatcher: CollectingDispatcher, tracker, domain: DomainDict) -> List[Dict[str, Any]]:
        stock_symbol = extract_stock_symbol_from_input(tracker.latest_message.get('text'))

        try:
            stock_data = yf.Ticker(stock_symbol).history(period='1y')
            short_ema = stock_data['Close'].ewm(span=12, adjust=False).mean()
            long_ema = stock_data['Close'].ewm(span=26, adjust=False).mean()
            macd = short_ema - long_ema
            signal = macd.ewm(span=9, adjust=False).mean()
            macd_histogram = macd - signal

            dispatcher.utter_message(f"The MACD for {stock_symbol} is: {macd.iloc[-1]}, {signal.iloc[-1]}, {macd_histogram.iloc[-1]}")
        except Exception as e:
            dispatcher.utter_message(f"An error occurred while calculating MACD: {str(e)}")

        return [SlotSet("stock_symbol", None)]

class ActionAddToPortfolio(Action):
    def name(self) -> str:
        return "action_add_to_portfolio"

    async def run(self, dispatcher: CollectingDispatcher, tracker, domain: DomainDict) -> List[Dict[str, Any]]:
        stock_symbol = extract_stock_symbol_from_input(tracker.latest_message.get('text'))
        portfolio_file = "portfolio.txt"

        try:
            with open(portfolio_file, "r") as f:
                portfolio = json.load(f)

            portfolio.append(stock_symbol)

            with open(portfolio_file, "w") as f:
                json.dump(portfolio, f)

            dispatcher.utter_message(f"Added {stock_symbol} to your portfolio.")
        except Exception as e:
            dispatcher.utter_message(f"An error occurred while adding to portfolio: {str(e)}")

        return [SlotSet("portfolio", portfolio), SlotSet("stock_symbol", None)]

class ActionRemoveFromPortfolio(Action):
    def name(self) -> str:
        return "action_remove_from_portfolio"

    async def run(self, dispatcher: CollectingDispatcher, tracker, domain: DomainDict) -> List[Dict[str, Any]]:
        stock_symbol = extract_stock_symbol_from_input(tracker.latest_message.get('text'))
        portfolio_file = "portfolio.txt"

        try:
            with open(portfolio_file, "r") as f:
                portfolio = json.load(f)

            if stock_symbol in portfolio:
                portfolio.remove(stock_symbol)
                with open(portfolio_file, "w") as f:
                    json.dump(portfolio, f)
                dispatcher.utter_message(f"Removed {stock_symbol} from your portfolio.")
            else:
                dispatcher.utter_message(f"{stock_symbol} is not in your portfolio.")
        except Exception as e:
            dispatcher.utter_message(f"An error occurred while removing from portfolio: {str(e)}")

        return [SlotSet("portfolio", portfolio), SlotSet("stock_symbol", None)]

class ActionViewPortfolio(Action):
    def name(self) -> str:
        return "action_view_portfolio"

    async def run(self, dispatcher: CollectingDispatcher, tracker, domain: DomainDict) -> List[Dict[str, Any]]:
        portfolio_file = "portfolio.txt"

        try:
            with open(portfolio_file, "r") as f:
                portfolio = json.load(f)

            if portfolio:
                portfolio_str = ", ".join(portfolio)
                dispatcher.utter_message(f"Your portfolio contains: {portfolio_str}")
            else:
                dispatcher.utter_message("Your portfolio is empty.")
        except Exception as e:
            dispatcher.utter_message(f"An error occurred while viewing portfolio: {str(e)}")

        return []

class ActionPlotStockPrice(Action):
    def name(self) -> str:
        return "action_plot_stock_price"

    async def run(self, dispatcher: CollectingDispatcher, tracker, domain: DomainDict) -> List[Dict[str, Any]]:
        stock_symbol = extract_stock_symbol_from_input(tracker.latest_message.get('text'))

        try:
            stock_data = yf.Ticker(stock_symbol).history(period='1y')

            plt.figure(figsize=(10, 5))
            plt.plot(stock_data.index, stock_data['Close'])  
            plt.title(f"{stock_symbol} Stock Price of {stock_symbol} Over Last Year")
            plt.xlabel('Date')
            plt.ylabel('Stock Price ($)')
            plt.grid(True)
            plt.savefig('stock.png')
            plt.close()

            dispatcher.utter_message("Stock price plot saved as 'stock.png'")
        except Exception as e:
            dispatcher.utter_message(f"An error occurred while plotting stock price: {str(e)}")

        return [SlotSet("stock_symbol", None)]
class ActionIntroduce(Action):
    def name(self) -> str:
        return "action_introduce"

    async def run(self, dispatcher: CollectingDispatcher, tracker, domain: DomainDict) -> List[Dict[str, Any]]:
        dispatcher.utter_message("I'm a chatbot designed to assist you with financial information and tasks.")
        return []


class ActionAskDemat(Action):
    def name(self) -> str:
        return "action_ask_demat"

    async def run(self, dispatcher: CollectingDispatcher, tracker, domain: DomainDict) -> List[Dict[str, Any]]:
        demat_info = "A demat account is an account that holds shares and securities in an electronic format."
        dispatcher.utter_message(demat_info)
        return []