import yfinance as yf
from rasa_sdk import Action

class ActionGetStockPrice(Action):

    def name(self):
        return "action_get_stock_price"

    def run(self, dispatcher, tracker, domain):
        stock_symbol = tracker.get_slot("stock_symbol")
        if stock_symbol:
            stock = yf.Ticker(stock_symbol)
            stock_price = stock.history(period="1d")["Close"].iloc[0]
            dispatcher.utter_message(text=f"The current price of {stock_symbol.upper()} is ${stock_price:.2f}.")
        else:
            dispatcher.utter_message(text="Please provide a valid stock symbol.")
        return []







# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
