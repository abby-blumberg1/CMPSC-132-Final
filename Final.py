from datetime import date, datetime, timezone, timedelta
import requests                             #Use python -m pip install requests to install the requests library
import time          
import pandas as pd                         #Use pip install pandas to install the panda library
import matplotlib.pyplot as plt             #Use python -m pip install -U matplotlib to install the matplot library
import statistics
from scipy.stats import t as t_dist         #Use pip install scipy to install the scipy library


class Node: #Defines a node class
    def __init__(self, key, value, color='RED'):
        self.key = key #self.key stores a key value (A date) that is unique and is used to insert the node into the Red-Black tree
        self.value = value #self.value stores information (A Stock's price on a certain day)
        self.right = None #self.right is the pointer to the right child of this node
        self.left = None #self.left is the pointer to the left child of this node
        self.parent = None #self.parent is the pointer to the parent of this node
        self.color = color #self.color stores the color of the node, either red or black, which is used to balanced the Red-Black tree. The default color is red

class RBT: #Defines a Red-Black Tree class
    def __init__(self):
        self.root = None     #Self.root stores the root node of the Red-Black tree. The default value is None.

    def insert(self, key, value):
        if self.root is None: #Checks if self.root is None
            self.root = Node(key, value, 'BLACK') #If the self.root is None, a node object is created with the color being set to Black and that node is set as the root of the RBT.
        else:
            self._insert(self.root, key, value) #If the RBT already as a root, then self._insert is called to insert a new node into the RBT

    def _insert(self, node, key, value):
        if key < node.key:
            if node.left is None:
                print(f"  -> Inserted {key} as LEFT child of {node.key}")
                node.left = Node(key, value)
                node.left.parent = node
                self._fix_insert(node.left)
            else:
                self._insert(node.left, key, value)

        elif key > node.key:
            if node.right is None:
                node.right = Node(key, value)
                node.right.parent = node
                self._fix_insert(node.right)
            else:
                self._insert(node.right, key, value)
        else:
            node.value = value
   

    def _rotate_left(self, Xnode):
        Ynode = Xnode.right
        Xnode.right = Ynode.left
        if Ynode.left != None:
            Ynode.left.parent = Xnode

        Ynode.parent = Xnode.parent
        if Xnode.parent is None:
            self.root = Ynode
        elif Xnode == Xnode.parent.left:
            Xnode.parent.left = Ynode
        else:
            Xnode.parent.right = Ynode

        Ynode.left = Xnode
        Xnode.parent = Ynode

    def _rotate_right(self, Xnode):
        Ynode = Xnode.left
        Xnode.left = Ynode.right
        if Ynode.right != None:
            Ynode.right.parent = Xnode

        Ynode.parent = Xnode.parent
        if Xnode.parent is None:
            self.root = Ynode
        elif Xnode == Xnode.parent.right:
            Xnode.parent.right = Ynode
        else:
            Xnode.parent.left = Ynode

        Ynode.right = Xnode
        Xnode.parent = Ynode

    def _fix_insert(self, node):
        while node != self.root and node.parent.color == "RED":
            parent = node.parent
            grandparent = parent.parent

     
            if parent == grandparent.left:
                uncle = grandparent.right

                if uncle and uncle.color == "RED":
                    parent.color = "BLACK"
                    uncle.color = "BLACK"
                    grandparent.color = "RED"
                    node = grandparent

                else:
                    if node == parent.right:
                        node = parent
                        self._rotate_left(node)

                    parent.color = "BLACK"
                    grandparent.color = "RED"
                    self._rotate_right(grandparent)
            else:
                uncle = grandparent.left

                if uncle and uncle.color == "RED":
                    parent.color = "BLACK"
                    uncle.color = "BLACK"
                    grandparent.color = "RED"
                    node = grandparent

                else:
                    if node == parent.left:
                        node = parent
                        self._rotate_right(node)

                    parent.color = "BLACK"
                    grandparent.color = "RED"
                    self._rotate_left(grandparent)

        self.root.color = "BLACK"

       
    def validate_key(self, key):
        if type(key) != str:
            return(False)
       
        try:
            datetime.strptime(key, "%Y-%m-%d")
            return True
        except ValueError:
            return False
       
    def search(self, key):
        return(self._search_helper(self.root, key))
       
    def _search_helper(self, node, key):
        if node == None:
            return(None)
       
        if node.key == key:
            return(node.value)
        elif key > node.key:
            return(self._search_helper(node.right, key))
        else:
            return(self._search_helper(node.left, key))
       
    def search_value(self, value):
        return(self._search_value_helper(self.root, value))
   
    def _search_value_helper(self, node, value):
        if node == None:
            return([])

        result = []  

        result += self._search_value_helper(node.left, value)
        if node.value == value:
            result += [node.key]
        result += self._search_value_helper(node.right, value)
        return(result)
       
    def search_range(self, key1, key2):
        return(self._search_range_helper(self.root, key1, key2))
   
    def _search_range_helper(self, node, key1, key2):
        if node == None:
            return([])
       
        result = []
        if key1 < node.key:
            result += self._search_range_helper(node.left, key1, key2)
        if key1 <= node.key <= key2:
            result += [node.value]
        if key2 > node.key:
            result += self._search_range_helper(node.right, key1, key2)
        return(result)

    def getMin(self):
        return(self._get_min_helper(self.root))
   
    def _get_min_helper(self, node):
        if node == None:
            return(float('inf'))
       
        left_min = self._get_min_helper(node.left)
        right_min = self._get_min_helper(node.right)
        return(min(node.value, left_min, right_min))

    def getMax(self):
        return(self._get_max_helper(self.root))
   
    def _get_max_helper(self, node):
        if node == None:
            return(float('-inf'))
       
        left_max = self._get_max_helper(node.left)
        right_max = self._get_max_helper(node.right)
       
        return(max(node.value, left_max, right_max))
       
    def get_min_max_range(self):
        if self.root != None:
            min_node = self.root
            max_node = self.root

            while min_node.left != None:
                min_node = min_node.left

            while max_node.right != None:
                max_node = max_node.right

            return({'min_key': min_node.key , 'max_key': max_node.key})
        else:
            return(None)

    def delete_tree(self):
        self._delete_tree_helper(self.root)
        self.root = None
   
    def _delete_tree_helper(self, node):
        if node == None:
            return(None)
       
        self._delete_tree_helper(node.left)
        self._delete_tree_helper(node.right)

        node.right = None
        node.left = None

    def search_range_dict(self, key1, key2):
        return(self._search_range_dict_helper(self.root, key1, key2))
   
    def _search_range_dict_helper(self, node, key1, key2):
        if node == None:
            return({})
       
        result = {}
        if key1 < node.key:
            result.update(self._search_range_dict_helper(node.left, key1, key2))
        if key1 <= node.key <= key2:
            result.update({node.key: node.value})
        if key2 > node.key:
            result.update(self._search_range_dict_helper(node.right, key1, key2))
        return(result)

class Stock(RBT):
    def __init__(self, ticker_symbol):
        super().__init__()
        self.ticker_symbol = ticker_symbol
        self.current_price = None

    def update_current_price(self):
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{self.ticker_symbol}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            result = data["chart"]["result"]
            meta = result[0]["meta"]
            current_price = meta["regularMarketPrice"]
            self.current_price = current_price
            return(current_price)

        except:
            return("Not a valid ticker symbol")
       
    def _get_first_day_of_trading(self):
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{self.ticker_symbol}"
        params = {"interval": "1d", "range": "max"}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        result = data["chart"]["result"][0]
        first_ts = result["timestamp"][0]
        first_date_str = time.strftime("%Y-%m-%d", time.gmtime(first_ts))
        first_date = datetime.strptime(first_date_str, "%Y-%m-%d").date()

        return(first_date)

    def update_historical_prices(self):
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{self.ticker_symbol}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
        }

        start = self._get_first_day_of_trading()
        end = date.today()

        self.delete_tree()

        while start < end:
            window_end = start + timedelta(days=92)
            if window_end > end:
                window_end = end

            period1 = int(datetime(start.year, start.month, start.day, tzinfo=timezone.utc).timestamp())
            period2 = int(datetime(window_end.year, window_end.month, window_end.day, tzinfo=timezone.utc).timestamp())

            params = {
                "interval": "1d",
                "period1": period1,
                "period2": period2
            }

            try:
                response = requests.get(url, params=params, headers=headers)
                data = response.json()

                result_list = data["chart"]["result"]

                valid_result = (
                    result_list
                    and "timestamp" in result_list[0]
                    and "indicators" in result_list[0]
                    and "adjclose" in result_list[0]["indicators"]
                )

                if valid_result:
                    result = result_list[0]
                    timestamps = result["timestamp"]
                    closes = result["indicators"]["adjclose"][0]["adjclose"]

                    for ts, close in zip(timestamps, closes):
                        if close is not None:
                            date_key = datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat()
                            self.insert(date_key, close)

            except:
                pass

            start = window_end

        return("Daily historical prices inserted into BST")

   
    def get_price_at_date(self, date_key):
        if super().validate_key(date_key) == False:
            return('The date is not valid')
       
        range_dict = super().get_min_max_range()
        if not(range_dict['min_key'] <= date_key <= range_dict['max_key']):
            return("The date is outside of the range")
       
        return(super().search(date_key))
   
    def get_highest_price(self):
        highest_price = super().getMax()
        dates = super().search_value(highest_price)
        return((highest_price, dates))
   
    def get_lowest_price(self):
        lowest_price = super().getMin()
        dates = super().search_value(lowest_price)
        return((lowest_price, dates))
   
    def get_price_range(self, start_date, end_date):
        if super().validate_key(start_date) == False:
            return('The start date is not valid')
        elif super().validate_key(end_date) == False:
            return('The end date is not valid')
       
        range_dict = super().get_min_max_range()
        if start_date > end_date:
            return "The start date must be less than the end date"
        elif not(range_dict['min_key'] <= start_date <= range_dict['max_key']):
            return("The start date is out side of the range")
        elif not(range_dict['min_key'] <= end_date <= range_dict['max_key']):
            return("The end date is outside of the range")
       
        return(super().search_range(start_date, end_date))
   
    def get_price_range_dict(self, start_date, end_date):
        if super().validate_key(start_date) == False:
            return('The start date is not valid')
        elif super().validate_key(end_date) == False:
            return('The end date is not valid')
       
        range_dict = super().get_min_max_range()
        if start_date > end_date:
            return "The start date must be less than the end date"
        elif not(range_dict['min_key'] <= start_date <= range_dict['max_key']):
            return("The start date is out side of the range")
        elif not(range_dict['min_key'] <= end_date <= range_dict['max_key']):
            return("The end date is outside of the range")
       
        return(super().search_range_dict(start_date, end_date))
   
    def get_highest_price_from_range(self, start_date, end_date):
        price_range = self.get_price_range(start_date, end_date)
        if type(price_range) == str:
            return(price_range)
        else:
            return(max(price_range))
       
    def get_lowest_price_from_range(self, start_date, end_date):
        price_range = self.get_price_range(start_date, end_date)
        if type(price_range) == str:
            return(price_range)
        else:
            return(min(price_range))
       
    def get_average_price_from_range(self, start_date, end_date):
        price_range = self.get_price_range(start_date, end_date)
        if type(price_range) == str:
            return(price_range)
        else:
            average = sum(price_range) / len(price_range)
            return(average)
   
    def make_graph(self, start_date, end_date):
        price_dict = self.get_price_range_dict(start_date, end_date)
        x_values = []
        y_values = []
        for key, price in price_dict.items():
            x_values += [key]
            y_values += [price]
        plt.figure(figsize=(10, 5))
        plt.plot(x_values, y_values, marker='o', linestyle='-')        
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Price Graph')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
   
    def get_returns(self, start_date, end_date):                                            
        price_range = self.get_price_range(start_date, end_date)
        if type(price_range) == str:
            return(price_range)
        else:
            result = []
            for i in range(1, len(price_range)):
                daily_return = (price_range[i] - price_range[i-1]) / price_range[i-1]
                result += [daily_return]
            return(result)
       
    def get_volatility(self, start_date, end_date):
        returns = self.get_returns(start_date, end_date)
        if type(returns) == str:
            return(returns)
        else:
            daily_vol = statistics.stdev(returns)
            range_vol = daily_vol * (252 ** 0.5)
            return(range_vol)

    def get_max_Drawdown(self, start_date, end_date):
        price_range = self.get_price_range(start_date, end_date)
        if type(price_range) == str:
            return(price_range)
        else:
            max_price = price_range[0]
            max_drawdown = 0    
            for price in price_range:
                if price > max_price:
                    max_price = price

                drawdown = (price - max_price) / max_price
                if drawdown < max_drawdown:
                    max_drawdown = drawdown
            return(max_drawdown)  

    def Rolling_Averages_of_Returns(self, start_date, end_date, window):
        returns = self.get_returns(start_date, end_date)
        if type(returns) == str:
            return(returns)
        else:
            if len(returns) < window:
                return "Not enough data to compute rolling averages"
            else:
                result = []
                for i in range(len(returns) - window + 1):
                    average = sum(returns[i:i + window]) / window
                    result += [average]
                return(result)

    def Moving_Averages(self, start_date, end_date, window):
        price_range = self.get_price_range(start_date, end_date)
        if type(price_range) == str:
            return(price_range)
        else:
            if len(price_range) < window:
                return "Not enough data to compute moving averages"
            else:
                result = []
                for i in range(len(price_range) - window + 1):
                    average = sum(price_range[i:i + window]) / window
                    result += [average]
                return(result)

    def Compare_Two_Stocks(self, stock2, Stat_func, *args):
        if isinstance(stock2, Stock) != True:
            return('The second stock must be a stock object')
       
        statOne = Stat_func(*args)
        statTwo =  getattr(stock2, Stat_func.__name__)(*args)

        if type(statOne) == str:
            return(statOne)
        elif type(statTwo) == str:
            return(statTwo)
       
        if type(statOne) == list and type(statTwo) == list:
            n = min(len(statOne), len(statTwo))
            statOne = statOne[:n]
            statTwo = statTwo[:n]

            mean1 = statistics.mean(statOne)
            mean2 = statistics.mean(statTwo)
            sd1 = statistics.stdev(statOne)
            sd2 = statistics.stdev(statTwo)
            t_stat = (mean1 - mean2) / (((sd1**2 / n) + (sd2**2 / n)) ** 0.5)
            p_value = 2 * (1 - t_dist.cdf(abs(t_stat), df=n-1))
            if p_value < 0.05:
                return(f'The two stocks differ significantly at the 5% level\nMean-1: {mean1}\nMean-2: {mean2}\nt-statistic: {t_stat}\np-value: {p_value}')
            else:
                return(f'The two stocks do not differ significantly at the 5% level\nMean-1: {mean1}\nMean-2: {mean2}\nt-statistic: {t_stat}\np-value: {p_value}')
        return('Statistics are not comparable')


ticker_symbol = input("Please input a ticker symbol: ")

import tkinter as tk
class Scrrens:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to Stock Comparisons")
        self.root.geometry("500x500")

        # Create the Menu Frame
        self.main_menu = tk.Frame(self.root)
        self.main_menu.pack(expand=True, fill="both")

        tk.Label(self.main_menu, text="Please enter the Ticker of the stock here: ", font=("Arial", 10)).pack(pady=20)
        self.stock_input = tk.Entry(self.main_menu, font=("Arial", 12))
        self.stock_input.pack(pady=10)
        tk.Button(
            self.main_menu,
            text="Click Me",
            command=self.confirmation_window
        ).pack()

    def clear_screen(self):
        """Helper to clear all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.pack_forget()
           
    def confirmation_window(self):
        # Hide the main menu
        ticker = self.stock_input.get().upper()
        if ticker == "":
            print("no stock")
            return
       
        self.main_menu.pack_forget()

        # Create the Second Window Frame
        self.second_window = tk.Frame(self.root)
        self.second_window.pack(expand=True, fill="both")

        tk.Label(self.second_window, text="Confirmation Window", font=("Arial", 10)).pack(pady=20)
       
        # Display the text from the first window
        tk.Label(self.second_window, text=f"Are you sure you want to select: {ticker}?", wraplength=250).pack(pady=10)

        # Buttons Frame (to sit side-by-side)
        button_frame = tk.Frame(self.second_window)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Yes", width=10, bg="green", fg="white",
                  command=lambda: self.action_menu(ticker)).pack(side="left", padx=5) #print(f"Confirmed: {ticker}")).pack(side="left", padx=5)
       
        tk.Button(button_frame, text="No", width=10, bg="red", fg="white",
                  command=self.back_to_menu).pack(side="left", padx=5)

    def back_to_menu(self):
        # Remove second window and show main menu again
        self.second_window.destroy() # Using destroy to clear memory since it's recreated every time
        self.main_menu.pack(expand=True, fill="both")

    def action_menu(self, ticker):
        self.clear_screen()
        self.third_window = tk.Frame(self.root)
        self.third_window.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(self.third_window, text=f"Actions for: {ticker}", font=("Arial", 14, "bold")).pack(pady=10)

        # Container for the functional buttons
        grid_frame = tk.Frame(self.third_window)
        grid_frame.pack(fill="both", expand=True)

        # List of button texts and placeholder commands
        # Replace 'print' with your actual function calls from the other file
        buttons = [
            ("Get Returns", lambda: print("Fetching returns...")),
            ("Avg Price Range", lambda: print("Calculating avg range...")),
            ("Lowest in Range", lambda: print("Finding lowest in range...")),
            ("Highest in Range", lambda: print("Finding highest in range...")),
            ("Price Range", lambda: print("Getting price range...")),
            ("Lowest (All Time)", lambda: print("Fetching all-time low...")),
            ("Price at Date", lambda: print("Prompting for date...")),
            ("Highest Price", lambda: print("Fetching highest price...")),
        ]

        # Arrange buttons in 2 columns
        for i, (text, cmd) in enumerate(buttons):
            btn = tk.Button(grid_frame, text=text, command=cmd, height=2)
            btn.grid(row=i//2, column=i%2, sticky="nsew", padx=5, pady=5)
            grid_frame.grid_columnconfigure(i%2, weight=1)

        tk.Button(self.third_window, text="Back to Main Menu", bg="gray", fg="white",
                  command=self.show_main_menu).pack(pady=20)

    def show_main_menu(self):
        self.clear_screen()
        self.main_menu.pack(expand=True, fill="both")
if __name__ == "__main__":
    root = tk.Tk()
    app = Scrrens(root)
    root.mainloop()
