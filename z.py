import pandas as pd
import yaml
import re

# Load the CSV file (replace with actual file path)
file_path = 'data.csv'  
df = pd.read_csv(file_path)

# Helper function to clean and escape problematic characters
def clean_text(text):
    text = re.sub(r'[\"\'\\]', '', text)  # Remove both " and '
    return text.strip()

# Function to generate domain.yml, nlu.yml, rules.yml, and stories.yml
def generate_rasa_files(df):
    domain_data = {
        'version': '3.1',
        'intents': [],
        'responses': {},
        'actions': []
    }
    
    nlu_data = {
        'version': '3.1',
        'nlu': []
    }
    
    rules_data = {
        'version': '3.1',
        'rules': []
    }
    
    stories_data = {
        'version': '3.1',
        'stories': []
    }

    existing_intents = set()

    # Process each term from CSV
    for _, row in df.iterrows():
        term = clean_text(row['terms'])
        definition = clean_text(row['definitions'])

        # Generate unique intent and response names
        intent_key = f'get_def_of_{term.replace(" ", "_").lower()}'
        response_key = f'utter_defof_{term.replace(" ", "_").lower()}'

        # Sanitize intent key to remove any invalid characters
        intent_key = re.sub(r'[^a-zA-Z0-9_]', '_', intent_key)  # Replace invalid chars with '_'

        # Check for duplicate intents
        if intent_key in existing_intents:
            print(f"Duplicate intent found: {intent_key}. Skipping this term.")
            continue

        # Add intents and responses to domain.yml
        existing_intents.add(intent_key)
        domain_data['intents'].append(intent_key)
        domain_data['responses'][response_key] = [{'text': f"The definition of {term} is: {definition}"}]
        
        # Add NLU training data
        nlu_data['nlu'].append({
            'intent': intent_key,
            'examples': f"- What is {term}?\n- Define {term}.\n- Explain {term}."
        })
        
        # Create rules for answering the question
        rules_data['rules'].append({
            'rule': f"Provide definition for {term}",
            'steps': [{'intent': intent_key}, {'action': response_key}]
        })
        
        # Create stories for the interaction
        stories_data['stories'].append({
            'story': f"User asks about {term}",
            'steps': [{'intent': intent_key}, {'action': response_key}]
        })
    
    # Add your old intents, responses, and actions
    domain_data['intents'].extend([
        'greet', 'goodbye', 'introduce', 'ask_demat', 'ask_mutual_funds',
        'stock_price', 'get_stock_news', 'add_stock_to_portfolio', 'remove_stock_from_portfolio',
        'show_portfolio', 'plot_stock_chart', 'ask_rsi', 'ask_macd', 'ask_sma', 'ask_ema'
    ])
    
    domain_data['responses'].update({
        'utter_greet': [{'text': "Hello! How can I assist you today?"}],
        'utter_goodbye': [{'text': "Goodbye! Have a great day!"}],
        'utter_ask_demat': [{'text': "A demat account holds your securities in electronic form."}],
        'utter_ask_mutual_funds': [{'text': "Mutual funds pool money from multiple investors to purchase securities."}],
        'utter_ask_sp500': [{'text': "The S&P 500 is an index of 500 of the largest companies listed on stock exchanges in the U.S."}],
    })
    
    domain_data['actions'].extend([
        'action_get_stock_price', 'action_get_stock_news', 'action_view_portfolio',
        'action_add_to_portfolio', 'action_remove_from_portfolio', 'action_plot_stock_price',
        'action_calculate_sma', 'action_calculate_ema', 'action_calculate_rsi', 'action_calculate_macd'
    ])

    # Add NLU training data for stock-related intents
    nlu_data['nlu'].extend([
        {'intent': 'greet', 'examples': "- hello\n- hi\n- good morning\n- hey there\n- what's up?"},
        {'intent': 'goodbye', 'examples': "- bye\n- see you later\n- goodbye\n- take care\n- have a nice day"},
        {'intent': 'stock_price', 'examples': "- what's the price of apple stock?\n- how much is microsoft trading at?\n- give me the stock price of google\n- what is the current price of tesla?\n- tell me the latest price for amazon stock"},
        {'intent': 'get_stock_news', 'examples': "- what's the latest news about tesla?\n- any news on apple?\n- tell me the news for microsoft\n- what are the updates for google?\n- give me the latest news on amazon"},
        {'intent': 'ask_rsi', 'examples': "- what is the RSI for AAPL?\n- calculate the RSI for TSLA\n- can you tell me the RSI of GOOGL?\n- what’s the RSI value for AMZN?\n- find the RSI for MSFT"},
        {'intent': 'ask_macd', 'examples': "- what is the MACD for AAPL?\n- calculate the MACD for TSLA\n- can you tell me the MACD of GOOGL?\n- what’s the MACD value for AMZN?\n- find the MACD for MSFT"},
        {'intent': 'ask_sma', 'examples': "- what is the SMA for AAPL?\n- calculate the SMA for TSLA\n- can you tell me the SMA of GOOGL?\n- what’s the SMA value for AMZN?\n- find the SMA for MSFT"},
        {'intent': 'ask_ema', 'examples': "- what is the EMA for AAPL?\n- calculate the EMA for TSLA\n- can you tell me the EMA of GOOGL?\n- what’s the EMA value for AMZN?\n- find the EMA for MSFT"},
        {'intent': 'add_stock_to_portfolio', 'examples': "- add apple to my portfolio\n- I want to buy microsoft shares\n- can you add google to my stocks?\n- I’d like to include tesla in my portfolio\n- please add amazon to my investment list"},
        {'intent': 'remove_stock_from_portfolio', 'examples': "- sell my apple shares\n- remove microsoft from my portfolio\n- I want to get rid of google stocks\n- can you delete tesla from my stocks?\n- please remove amazon from my investment list"},
        {'intent': 'show_portfolio', 'examples': "- show me my portfolio\n- what stocks do I own?\n- can you list my investments?\n- I want to see my stock holdings\n- tell me about my portfolio"},
        {'intent': 'plot_stock_chart', 'examples': "- plot the stock price of apple\n- show me the chart for microsoft stock\n- can I see a graph for tesla's stock price?\n- display the price chart for google\n- give me the historical chart for amazon stock"}
    ])

    # Add rules for basic and stock-related actions
    rules_data['rules'].extend([
        {'rule': 'Greet user', 'steps': [{'intent': 'greet'}, {'action': 'utter_greet'}]},
        {'rule': 'Say goodbye', 'steps': [{'intent': 'goodbye'}, {'action': 'utter_goodbye'}]},
        {'rule': 'Provide stock price when asked', 'steps': [{'intent': 'stock_price'}, {'action': 'action_get_stock_price'}]},
        {'rule': 'Provide stock news when asked', 'steps': [{'intent': 'get_stock_news'}, {'action': 'action_get_stock_news'}]},
        {'rule': 'Add stock to portfolio', 'steps': [{'intent': 'add_stock_to_portfolio'}, {'action': 'action_add_to_portfolio'}]},
        {'rule': 'Remove stock from portfolio', 'steps': [{'intent': 'remove_stock_from_portfolio'}, {'action': 'action_remove_from_portfolio'}]},
        {'rule': 'Show portfolio', 'steps': [{'intent': 'show_portfolio'}, {'action': 'action_view_portfolio'}]},
        {'rule': 'Plot stock price chart', 'steps': [{'intent': 'plot_stock_chart'}, {'action': 'action_plot_stock_price'}]},
        {'rule': 'Calculate RSI', 'steps': [{'intent': 'ask_rsi'}, {'action': 'action_calculate_rsi'}]},
        {'rule': 'Calculate MACD', 'steps': [{'intent': 'ask_macd'}, {'action': 'action_calculate_macd'}]},
        {'rule': 'Calculate SMA', 'steps': [{'intent': 'ask_sma'}, {'action': 'action_calculate_sma'}]},
        {'rule': 'Calculate EMA', 'steps': [{'intent': 'ask_ema'}, {'action': 'action_calculate_ema'}]}
    ])

    # Add stories for stock-related interactions
    stories_data['stories'].extend([
        {'story': 'User asks for stock price', 'steps': [{'intent': 'stock_price'}, {'action': 'action_get_stock_price'}]},
        {'story': 'User asks for stock news', 'steps': [{'intent': 'get_stock_news'}, {'action': 'action_get_stock_news'}]},
        {'story': 'User adds stock to portfolio', 'steps': [{'intent': 'add_stock_to_portfolio'}, {'action': 'action_add_to_portfolio'}]},
        {'story': 'User removes stock from portfolio', 'steps': [{'intent': 'remove_stock_from_portfolio'}, {'action': 'action_remove_from_portfolio'}]},
        {'story': 'User views portfolio', 'steps': [{'intent': 'show_portfolio'}, {'action': 'action_view_portfolio'}]},
        {'story': 'User plots stock chart', 'steps': [{'intent': 'plot_stock_chart'}, {'action': 'action_plot_stock_price'}]},
        {'story': 'User asks for RSI', 'steps': [{'intent': 'ask_rsi'}, {'action': 'action_calculate_rsi'}]},
        {'story': 'User asks for MACD', 'steps': [{'intent': 'ask_macd'}, {'action': 'action_calculate_macd'}]},
        {'story': 'User asks for SMA', 'steps': [{'intent': 'ask_sma'}, {'action': 'action_calculate_sma'}]},
        {'story': 'User asks for EMA', 'steps': [{'intent': 'ask_ema'}, {'action': 'action_calculate_ema'}]}
    ])

    # Save the generated data to YAML files
    with open('domain.yml', 'w') as domain_file:
        yaml.dump(domain_data, domain_file, sort_keys=False)

    with open('nlu.yml', 'w') as nlu_file:
        yaml.dump(nlu_data, nlu_file, sort_keys=False)

    with open('rules.yml', 'w') as rules_file:
        yaml.dump(rules_data, rules_file, sort_keys=False)

    with open('stories.yml', 'w') as stories_file:
        yaml.dump(stories_data, stories_file, sort_keys=False)

# Run the function to generate the Rasa files
generate_rasa_files(df)
print("Rasa files generated successfully!")
