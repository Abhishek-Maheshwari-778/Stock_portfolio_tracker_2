import requests

# Alpha Vantage API Configuration
API_KEY = 'your_alpha_vantage_api_key'  # Replace with your API key from Alpha Vantage
BASE_URL = 'https://www.alphavantage.co/query'

# Portfolio dictionary to hold stock symbol and the number of shares
portfolio = {}

def add_stock(symbol, shares):
    """Add a stock to the portfolio."""
    if symbol in portfolio:
        portfolio[symbol]['shares'] += shares
    else:
        portfolio[symbol] = {
            'shares': shares,
            'initial_price': get_stock_price(symbol)
        }
    print(f"Added {shares} shares of {symbol} to the portfolio.")

def remove_stock(symbol):
    """Remove a stock from the portfolio."""
    if symbol in portfolio:
        del portfolio[symbol]
        print(f"Removed {symbol} from the portfolio.")
    else:
        print(f"{symbol} is not in the portfolio.")

def get_stock_price(symbol):
    """Fetch real-time stock price from Alpha Vantage."""
    url = f'{BASE_URL}?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url).json()
    try:
        daily_data = response['Time Series (Daily)']
        latest_date = list(daily_data.keys())[0]
        latest_price = daily_data[latest_date]['4. close']
        return float(latest_price)
    except KeyError:
        print(f"Failed to retrieve data for {symbol}. Check if the symbol is correct.")
        return 0

def calculate_portfolio_value():
    """Calculate the total value of the portfolio based on real-time stock prices."""
    total_value = 0
    for symbol, stock_data in portfolio.items():
        current_price = get_stock_price(symbol)
        total_value += current_price * stock_data['shares']
    return total_value

def show_portfolio():
    """Display the current portfolio with stock information."""
    print("\n--- Portfolio ---")
    if not portfolio:
        print("The portfolio is empty.")
    for symbol, stock_data in portfolio.items():
        current_price = get_stock_price(symbol)
        print(f"{symbol}: {stock_data['shares']} shares @ ${current_price:.2f} (Initial price: ${stock_data['initial_price']:.2f})")
    total_value = calculate_portfolio_value()
    print(f"\nTotal Portfolio Value: ${total_value:.2f}")

def track_performance(symbol):
    """Calculate and show the performance of a specific stock."""
    if symbol in portfolio:
        initial_price = portfolio[symbol]['initial_price']
        current_price = get_stock_price(symbol)
        performance = ((current_price - initial_price) / initial_price) * 100
        print(f"{symbol} Performance: {performance:.2f}% (Initial: ${initial_price:.2f}, Current: ${current_price:.2f})")
    else:
        print(f"{symbol} is not in the portfolio.")

def main():
    """Main function to interact with the user."""
    while True:
        print("\nOptions:")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Show Portfolio")
        print("4. Track Stock Performance")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == '1':
            symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
            shares = input("Enter the number of shares: ")
            try:
                shares = int(shares)
            except ValueError:
                shares = 1  # Default number of shares if input is invalid
                print("Invalid number of shares entered. Defaulting to 1 share.")
            add_stock(symbol, shares)
        
        elif choice == '2':
            symbol = input("Enter the stock symbol to remove (e.g., AAPL): ").upper()
            remove_stock(symbol)
        
        elif choice == '3':
            show_portfolio()
        
        elif choice == '4':
            symbol = input("Enter the stock symbol to track performance (e.g., AAPL): ").upper()
            track_performance(symbol)
        
        elif choice == '5':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid option. Please choose a number between 1 and 5.")

# Example Usage
if __name__ == "__main__":
    main()
