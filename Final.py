from datetime import date, datetime, timezone, timedelta
import requests                             #Use 'python -m pip install requests' to install the requests library
import time          
import pandas as pd                         #Use 'pip install pandas' to install the panda library
import matplotlib.pyplot as plt             #Use 'python -m pip install -U matplotlib' to install the matplot library
import statistics
from scipy.stats import t as t_dist         #Use 'pip install scipy' to install the scipy library


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
        if key < node.key: #Checks if the new key is smaller than the key stored in the node, if it is then the new node belongs in the left subtree.
            if node.left is None: #If the left child doesn't exist, insert the new node into the left subtree.
                node.left = Node(key, value) #Sets the node.left pointer equal to the new node
                node.left.parent = node #Sets the node.left.parent pointer equal to the current node
                self._fix_insert(node.left) #Calls the _fix_insert() method to testore the Red-Black Tree properties
            else:
                self._insert(node.left, key, value) #If the left child node does exist keep searching down the left subtree.

        elif key > node.key: #Checks if the new key is greater than the key stored in the node, if it is then the new node belongs in the right subtree.
            if node.right is None: #If the right child doesn't exist, insert the new node into the right subtree.
                node.right = Node(key, value) #Sets the node.right pointer equal to the new node
                node.right.parent = node #Sets the node.right.parent pointer equal to the current node
                self._fix_insert(node.right) #Calls the _fix_insert() method to testore the Red-Black Tree properties
            else:
                self._insert(node.right, key, value) #If the right child node does exist keep searching down the right subtree.
        else:
            node.value = value #If the key already exists, update the stored value in the node.
   

    def _rotate_left(self, Xnode):
        Ynode = Xnode.right  #The Ynode becomes the new parent after rotation.
        Xnode.right = Ynode.left #Move the Ynode's left subtree to Xnode's right subtree.
        if Ynode.left != None: #Checks if the Ynode has a left child node
            Ynode.left.parent = Xnode  #Updates the parent pointer of the moved subtree.

        Ynode.parent = Xnode.parent  #The Ynode takes the Xnode's old parent.
        if Xnode.parent is None: #Checks if the Xnode does not have a parent node
            self.root = Ynode  #If the Xnode was the root, the Ynode becomes the new root.
        elif Xnode == Xnode.parent.left: #Checks If the Xnode was the left child of its parent
            Xnode.parent.left = Ynode #replaces the Xnode's left child pointer with Ynode after rotation.
        else:
            Xnode.parent.right = Ynode  #Update the Xnode's parent's right pointer to point at the Ynode.

        #Finalizes rotation: the Xnode becomes left child of the Ynode.
        Ynode.left = Xnode
        Xnode.parent = Ynode

    def _rotate_right(self, Xnode):
        Ynode = Xnode.left  #The Ynode becomes the new parent after rotation.
        Xnode.left = Ynode.right #Move the Ynode's right subtree to X's left subtree.
        if Ynode.right != None: #Checks if the Ynode has a right child node
            Ynode.right.parent = Xnode  #Updates the parent pointer of the moved subtree.

        Ynode.parent = Xnode.parent #The Ynode takes the Xnode's old parent.
        if Xnode.parent is None: #Checks if the Xnode does not have a parent node
            self.root = Ynode  #If the Xnode was the root, the Ynode becomes the new root.
        elif Xnode == Xnode.parent.right: #Checks If the Xnode was the right child of its parent
            Xnode.parent.right = Ynode #replaces the Xnode's right child pointer with Ynode after rotation.
        else:
            Xnode.parent.left = Ynode #Update the Xnode's parent's left pointer to point at the Ynode.

        #Finalizes rotation: the Xnode becomes right child of the Ynode.
        Ynode.right = Xnode
        Xnode.parent = Ynode

    def _fix_insert(self, node):
        while node != self.root and node.parent.color == "RED": #Loops while the node is not the root of the RBT and if the parent node is RED
            parent = node.parent  #Stores the parent node.
            grandparent = parent.parent #Stores the grandparent node.

            if parent == grandparent.left: #Checks if the parent node is the left child of the grandparent node.
                uncle = grandparent.right #stores the uncle which is the opposite child of the grandparent.

                if uncle and uncle.color == "RED": #Checks if the uncle node exists and that the node's color is red
                    parent.color = "BLACK" #Sets the parent node's color to black
                    uncle.color = "BLACK" #Sets the uncle node's color to black
                    grandparent.color = "RED" #Sets the grandparent node's color to red
                    node = grandparent #Makes the current node the grandparent node to move up the Red-Black Tree and to continue checking.
                else:
                    if node == parent.right: #Checks if the newly inserted node is the right child of its parent
                        node = parent #Moves the pointer up the Red-Black Tree so that the rotation happens around the parent.
                        self._rotate_left(node)  #Calls the _rotate_left() method to Perform a left rotation which transform the structure into a left‑left case, which can then be corrected with a right rotation

                    parent.color = "BLACK" #Sets the parent node's color to black
                    grandparent.color = "RED" #Sets the grandparent node's color to red
                    self._rotate_right(grandparent) #Calls the _rotate_right() method to fix the violation.
            else:
                uncle = grandparent.left #stores the uncle which is the opposite child of the grandparent.

                if uncle and uncle.color == "RED": #Checks if the uncle node exists and that the node's color is red
                    parent.color = "BLACK" #Sets the parent node's color to black
                    uncle.color = "BLACK" #Sets the uncle node's color to black
                    grandparent.color = "RED" #Sets the grandparent node's color to red
                    node = grandparent #Makes the current node the grandparent node to move up the Red-Black Tree and to continue checking.
                else:
                    if node == parent.left:  #Checks if the newly inserted node is the left child of its parent
                        node = parent  #Moves the pointer up the Red-Black Tree so that the rotation happens around the parent.
                        self._rotate_right(node)  #Calls the _rotate_right() method to Perform a right rotation which transform the structure into a right-right case, which can then be corrected with a left rotation

                    parent.color = "BLACK" #Sets the parent node's color to black
                    grandparent.color = "RED"  #Sets the grandparent node's color to red
                    self._rotate_left(grandparent) #Calls the _rotate_left() method to fix the violation.
        self.root.color = "BLACK"  #Ensures the root node's colro is always black

       
    def validate_key(self, key): #validates that the key is in the correct format
        if type(key) != str: #Checks if the key's type is a string
            return(False) #Return False becuase the key is not the correct type therefore the key is not valid
       
        try:
            datetime.strptime(key, "%Y-%m-%d")  #Attempts to convert the key into a date string in the format YYYY‑MM‑DD.
            return(True) #Returns True because the key is a valid date string.
        except ValueError:
            return(False) #Returns Flase because the key is not a valid date string.
       
    def search(self, key):  #Returns the value from the node with the corresponding key
        return(self._search_helper(self.root, key)) #Returns the result of calling the _search_helper() method
       
    def _search_helper(self, node, key):
        if node == None: #Checks if the node is None
            return(None) #Returns None if the node is None
       
        if node.key == key: #Checks if the key stored at the node is equal to the key that was inputed by the user
            return(node.value) #If the two keys match the value at the node is returned
        elif key > node.key: #Checks If the key that was inputed by the user is greater than the key stored at the node
            return(self._search_helper(node.right, key)) #Recursively calls the _search_helper() method to check if the correct node is stored in the right subtree
        else:
            return(self._search_helper(node.left, key)) #Recursively calls the _search_helper() method to check if the correct node is stored in the left subtree
       
    def search_value(self, value): #Finds the nodes that store the corresponding value and returns the nodes' keys
        return(self._search_value_helper(self.root, value)) #Returns the result of calling the _search_value_helper() method
   
    def _search_value_helper(self, node, value):
        if node == None: #Checks if the node is None
            return([]) #Returns an empty list if the node is None

        result = []  #initialize result as empty list
        result += self._search_value_helper(node.left, value) #Recursively calls the _search_value_helper() method to check if the correct node is stored in the left subtree
        if node.value == value: #Checks if the value stored at the node is equal to the value that was inputed by the user
            result += [node.key] #Adds the node's key to the result list if the value stored at the node is equal to the value that was inputed by the user
        result += self._search_value_helper(node.right, value) #Recursively calls the _search_value_helper() method to check if the correct node is stored in the right subtree
        return(result) #Returns the result list which contains the keys of all node's whose value match the value that was inputed by the user
       
    def search_range(self, key1, key2): #Gets all the values stored at the nodes' whose key is in the key range
        return(self._search_range_helper(self.root, key1, key2))  #Returns the result of calling the _search_range_helper() method
   
    def _search_range_helper(self, node, key1, key2):
        if node == None: #Checks if the node is None
            return([]) #Returns an empty list if the node is None
       
        result = [] #initialize result as empty list
        if key1 < node.key: #Checks if the node's key is greater than key1
            result += self._search_range_helper(node.left, key1, key2)  #Recursively calls the _search_range_helper() method to check if a node's whose key is in the key range is stored in the left subtree
        if key1 <= node.key <= key2: #Checks if the node's key is in between key1 and key2
            result += [node.value] #Adds the node's value to the result list if nodes' key is in the key range
        if key2 > node.key:  #Checks if the node's key less than key2
            result += self._search_range_helper(node.right, key1, key2)   #Recursively calls the _search_range_helper() method to check if a node's whose key is in the key range is stored in the right subtree
        return(result)  #Returns the result list which contains the values of all node's whose key are in the key range

    def getMin(self): #Gets the minimum value stored in the Red-Black Tree
        return(self._get_min_helper(self.root)) #returns the result of calling the _get_min_helper() method
   
    def _get_min_helper(self, node):
        if node == None: #Checks If the node is None
            return(float('inf')) #If the node is None, return positive infinity.
       
        left_min = self._get_min_helper(node.left) #Recursively calls the _get_min_helper() method to find the minimum value in the left subtree.
        right_min = self._get_min_helper(node.right) #Recursively calls the _get_min_helper() method to find the minimum value in the right subtree.
        return(min(node.value, left_min, right_min)) #Returns the smallest value among the current node's value, the minimum value found in the left subtree, and the minimum value found in the right subtree

    def getMax(self): #Gets the maximum value stored in the Red-Black Tree
        return(self._get_max_helper(self.root)) #returns the result of calling the _get_max_helper() method
   
    def _get_max_helper(self, node):
        if node == None: #Checks If the node is None
            return(float('-inf')) #If the node is None, return negative infinity.
       
        left_max = self._get_max_helper(node.left) #Recursively calls the _get_max_helper() method to find the maximum value in the left subtree.
        right_max = self._get_max_helper(node.right) #Recursively calls the _get_max_helper() method to find the maximum value in the right subtree.
        return(max(node.value, left_max, right_max))  #Returns the largest value among the current node's value, the maximum value found in the left subtree, and the maximum value found in the right subtree
       
    def get_min_max_range(self): #Returns a dictionary containing the minimum key and the maximum key stored in the Red-Black Tree
        if self.root != None: #Checks if self.root is not equal to None
            min_node = self.root #Sets the min_node equal to the node stored at self.root
            max_node = self.root #Sets the max_node equal to the node stored at self.root

            while min_node.left != None:
                min_node = min_node.left #Traverses through the left children to find the smallest key in the BST.

            while max_node.right != None:
                max_node = max_node.right #Traverses through the right children to find the largest key in the BST.

            return({'min_key': min_node.key , 'max_key': max_node.key}) #Returns a dictionary containing both the minimum and maximum keys found in the tree.
        else:
            return(None) #If the tree is empty, return None since no minimum or maximum keys exist.

    def delete_tree(self): #Deletes the Red-Black tree
        self._delete_tree_helper(self.root) #Calls the _delete_tree_helper() method to delete the RBT
        self.root = None #Sets self.root equal to None
   
    def _delete_tree_helper(self, node):
        if node == None: #checks if the node is equal to None
            return(None) #Returns none if the node does not exist
       
        self._delete_tree_helper(node.left) #Recursively calls the _delete_tree_helper() method to remove all the nodes left subtree.
        self._delete_tree_helper(node.right) #Recursively calls the _delete_tree_helper() method to remove all the nodes right subtree.

        node.right = None #Sets the pointer to the right child node equal to None
        node.left = None #Sets the pointer to the left child node equal to None

    def search_range_dict(self, key1, key2): #Creates a dictionary containg the key values pairs from the node's whose key is in the key range
        return(self._search_range_dict_helper(self.root, key1, key2)) #Returns the result of calling the _search_range_dict_helper() method
   
    def _search_range_dict_helper(self, node, key1, key2):
        if node == None: #Checks if the node is None
            return({}) #Returns an empty dictionary if the node is None
       
        result = {} #initialize result as empty dictionary
        if key1 < node.key:  #Checks if the node's key is greater than key1
            result.update(self._search_range_dict_helper(node.left, key1, key2))  #Recursively calls the _search_range_dict_helper() method to check if a node's whose key is in the key range is stored in the left subtree
        if key1 <= node.key <= key2:  #Checks if the node's key is in between key1 and key2
            result.update({node.key: node.value}) #Adds the node's key and value to the result dictionary if nodes' key is in the key range
        if key2 > node.key:  #Checks if the node's key less than key2
            result.update(self._search_range_dict_helper(node.right, key1, key2)) #Recursively calls the _search_range_dict_helper() method to check if a node's whose key is in the key range is stored in the right subtree
        return(result)  #Returns the result dictionary which contains the keys and values of all node's whose key are in the key range

class Stock(RBT): #Defines a Stock class. The Stock class is a child class of the RBT class, and inherits the parent class's methods.
    def __init__(self, ticker_symbol):
        super().__init__() #Calls the parent class's __init__() method to set self.root to None
        self.ticker_symbol = ticker_symbol #Self.ticker_symbol stores the ticker_symbol of the stock
        self.current_price = self.update_current_price() #Self.current_price stores the current price of the stock.

    def update_current_price(self):
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{self.ticker_symbol}"   #Constructs the Yahoo Finance API URL using the stock's ticker symbol.
        headers = {                                                                       #Sets a User-Agent header to mimic a real browser.
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers) #Sends an HTTP GET request to Yahoo Finance with the custom headers.
            data = response.json()  #Converts the API response from JSON text into a Python dictionary.
            result = data["chart"]["result"]  #Enters into the JSON structure to access the chart result section.
            meta = result[0]["meta"]  #Gets the metadata for the stock
            current_price = meta["regularMarketPrice"]  #Gets the current market price of the stock from the metadata.
            self.current_price = current_price #Sets self.current_price equal to the current market price of the stock
            return(current_price) #Returns the current market price of the stock

        except:
            return("Not a valid ticker symbol") #If an except is raised a string is returned to the user telling them that the ticker symbol is not valid
       
    def _get_first_day_of_trading(self):
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{self.ticker_symbol}" #Constructs the Yahoo Finance API URL using the stock's ticker symbol.
        params = {"interval": "1d", "range": "max"} #Defines the query parameters for the Yahoo Finance API request
        headers = {                                                                     #Sets a User-Agent header to mimic a real browser.
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

        response = requests.get(url, params=params, headers=headers)  #Sends an HTTP GET request to Yahoo Finance with the custom headers and params.
        data = response.json()  #Converts the API response from JSON text into a Python dictionary.
        result = data["chart"]["result"][0] #Enters into the JSON structure to access the chart result section.
        first_ts = result["timestamp"][0] #Extracts the first UNIX timestamp from the API response.
        first_date_str = time.strftime("%Y-%m-%d", time.gmtime(first_ts)) #Converts the UNIX timestamp into a date string with the format YYYY‑MM‑DD.
        first_date = datetime.strptime(first_date_str, "%Y-%m-%d").date() #Turns the date string into a Python datetime object

        return(first_date) #Returns the first available trading date for the stock.

    def update_historical_prices(self):
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{self.ticker_symbol}"  #Constructs the Yahoo Finance API URL using the stock's ticker symbol.
        headers = {                                                                      #Sets a User-Agent header to mimic a real browser.
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
        }

        start = self._get_first_day_of_trading() #Calls the _get_first_day_of_trading() method to get the first available trading date for the stock.
        end = date.today() #Gets the current date

        self.delete_tree() #Calls delete_tree() method from the parent class to detete the current tree stored in the RBT class
        while start < end:  #Loops through the full date range in chunks.
            window_end = start + timedelta(days=92) #Defines the end of the 92‑day window.
            if window_end > end:  #Ensures the final window does not go past the requested end date.
                window_end = end

            period1 = int(datetime(start.year, start.month, start.day, tzinfo=timezone.utc).timestamp()) #Converts the start date of the window into UNIX timestamps
            period2 = int(datetime(window_end.year, window_end.month, window_end.day, tzinfo=timezone.utc).timestamp()) #Converts the end date of the window into UNIX timestamps
            params = {"interval": "1d", "period1": period1, "period2": period2}  #Sets the API parameters: interval="1d" is the daily data and period1/period2 are time window for this chunk
   
            try:
                response = requests.get(url, params=params, headers=headers)  #Sends an HTTP GET request to Yahoo Finance with the custom headers and params.
                data = response.json()  #Converts the API response from JSON text into a Python dictionary.
                result_list = data["chart"]["result"] #Enters into the JSON structure to access the list of results.

                valid_result = (                      
                    result_list
                    and "timestamp" in result_list[0]
                    and "indicators" in result_list[0]
                    and "adjclose" in result_list[0]["indicators"]
                )

                if valid_result: #Checks that the response contains valid price data.
                    #Extracts the UNIX timestamps and adjusted closing prices.
                    result = result_list[0]
                    timestamps = result["timestamp"]
                    closes = result["indicators"]["adjclose"][0]["adjclose"]

                    for ts, close in zip(timestamps, closes): #Loops through each timestamp and its corresponding adjusted close price.
                        if close is not None: #Ensures the price is valid.
                            date_key = datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat() #Converts the UNIX timestamp into a UTC date.
                            self.insert(date_key, close)  #Inserts the date and closing price into the Red-Black Tree
            except:  #Silently ignores errors
                pass
            start = window_end  #Moves to the next 92‑day window
        return("Daily historical prices inserted into RBT") #Returns a string confirming that all data has been processed and stored.

   
    def get_price_at_date(self, date_key): #The user inputs a date and then the price of the stock at the selected date is returned
        if super().validate_key(date_key) == False: #Calls the validate_key() method from the RBT parent class to enusre that the date is the correct format of YYYY-MM-DD
            return('The date is not valid') #If the date the user inputed is not valid then a string is returned telling the user that the date is not valid
       
        range_dict = super().get_min_max_range() #Calls the get_min_max_range() method from the RBT parent class, which gets a dictionary containing the first date and last date in the RBT
        if not(range_dict['min_key'] <= date_key <= range_dict['max_key']): #Checks if the date the user inputed is in between the first and last date in the RBT
            return("The date is outside of the range") #If the date is outside of the date range of the RBT, then a string is returned telling the user that the date they inputed is outside of the date range.
       
        return(super().search(date_key)) #Calls the Search() method from the parent class, to get price at the date that the user specified
   
    def get_highest_price(self):
        highest_price = super().getMax() #Calls the getMax() from the parent class to get the maximum price of the stock that is stored in the RBT
        dates = super().search_value(highest_price) #Calls the search_value() method from the parent class to get the date at which the maximum price of the stock occured on
        return((dates, highest_price)) #Returns a tuple containing the date at which the maximum price ocurred, and the maximum price itself
   
    def get_lowest_price(self):
        lowest_price = super().getMin() #Calls the getMin() from the parent class to get the minimum price of the stock that is stored in the RBT
        dates = super().search_value(lowest_price) #Calls the search_value() method from the parent class to get the date at which the minimum price of the stock occured on
        return((dates, lowest_price)) #Returns a tuple containing the date at which the minimum price ocurred, and the minimum price itself
   
    def get_price_range(self, start_date, end_date):
        if super().validate_key(start_date) == False: #Calls the validate_key() method from the RBT parent class to enusre that the start date is the correct format of YYYY-MM-DD
            return('The start date is not valid') #If the start date the user inputed is not valid then a string is returned telling the user that the date is not valid
        elif super().validate_key(end_date) == False: #Calls the validate_key() method from the RBT parent class to enusre that the end date is the correct format of YYYY-MM-DD
            return('The end date is not valid') #If the end date the user inputed is not valid then a string is returned telling the user that the date is not valid
       
        range_dict = super().get_min_max_range() #Calls the get_min_max_range() method from the RBT parent class, which gets a dictionary containing the first date and last date in the RBT
        if start_date > end_date: #Checks if the start date is greater than the end date
            return("The start date must be less than the end date") #If the start date that the user inputed is greater than the end date, a string is returned telling the user that the start date must be less than the end dat
        elif not(range_dict['min_key'] <= start_date <= range_dict['max_key']): #Checks if the  start date the user inputed is in between the first and last date in the RBT
            return("The start date is out side of the range")  #If the start date is outside of the date range of the RBT, then a string is returned telling the user that the date they inputed is outside of the date range.
        elif not(range_dict['min_key'] <= end_date <= range_dict['max_key']): #Checks if the end date the user inputed is in between the first and last date in the RBT
            return("The end date is outside of the range")  #If the end date is outside of the date range of the RBT, then a string is returned telling the user that the date they inputed is outside of the date range.
       
       
        return(super().search_range(start_date, end_date)) #Calls the serach_range() method from the parent class to get all the prices of the stock during the specified time peroid.
   
    def get_price_range_dict(self, start_date, end_date):
        if super().validate_key(start_date) == False: #Calls the validate_key() method from the RBT parent class to enusre that the start date is the correct format of YYYY-MM-DD
            return('The start date is not valid') #If the start date the user inputed is not valid then a string is returned telling the user that the date is not valid
        elif super().validate_key(end_date) == False: #Calls the validate_key() method from the RBT parent class to enusre that the end date is the correct format of YYYY-MM-DD
            return('The end date is not valid') #If the end date the user inputed is not valid then a string is returned telling the user that the date is not valid
       
        range_dict = super().get_min_max_range() #Calls the get_min_max_range() method from the RBT parent class, which gets a dictionary containing the first date and last date in the RBT
        if start_date > end_date: #Checks if the start date is greater than the end date
            return "The start date must be less than the end date" #If the start date that the user inputed is greater than the end date, a string is returned telling the user that the start date must be less than the end dat
        elif not(range_dict['min_key'] <= start_date <= range_dict['max_key']): #Checks if the start date the user inputed is in between the first and last date in the RBT
            return("The start date is out side of the range") #If the start date is outside of the date range of the RBT, then a string is returned telling the user that the date they inputed is outside of the date range.
        elif not(range_dict['min_key'] <= end_date <= range_dict['max_key']): #Checks if the end date the user inputed is in between the first and last date in the RBT
            return("The end date is outside of the range") #If the end date is outside of the date range of the RBT, then a string is returned telling the user that the date they inputed is outside of the date range.
       
        return(super().search_range_dict(start_date, end_date)) #Calls the search_range_dict() method from the parent class that returns a dictionary where each key is the date and each value is the price on that date for time peroid specified by the user
   
    def get_highest_price_from_range(self, start_date, end_date):
        price_range = self.get_price_range(start_date, end_date) #Calls the get_price_range() method to get all the prices of the stock during the specified time peroid.
   
        if type(price_range) == str: #Checks if price_range's type is a string
            return(price_range) #If price_range is a string than an error message was returned when calling the get_price_range() method, so the error message is then returned to the user
        else:
            return(max(price_range)) #Uses the bulit-in max function to get the maximum price of the stock during the specified time peroid.
       
    def get_lowest_price_from_range(self, start_date, end_date):
        price_range = self.get_price_range(start_date, end_date) #Calls the get_price_range() method to get all the prices of the stock during the specified time peroid.
        if type(price_range) == str: #Checks if price_range's type is a string
            return(price_range) #If price_range is a string than an error message was returned when calling the get_price_range() method, so the error message is then returned to the user
        else:
            return(min(price_range)) #Uses the bulit-in min function to get the minimum price of the stock during the specified time peroid.
       
    def get_average_price_from_range(self, start_date, end_date):
        price_range = self.get_price_range(start_date, end_date)  #Calls the get_price_range() method to get all the prices of the stock during the specified time peroid.
        if type(price_range) == str:  #Checks if the type of price_range is a string
            return(price_range) #If price_range is a string than an error message was returned when calling the get_price_range() method, so the error message is then returned to the user
        else:
            return(sum(price_range) / len(price_range)) #Calculates the average price of the stock during the specified time peroid
           
   
    def make_graph(self, start_date, end_date):
        price_dict = self.get_price_range_dict(start_date, end_date) #Calls the get_price_range() method to get all the prices of the stock during the specified time peroid.
        x_values = [] #initializes x_values as empty list
        y_values = [] #initialize y_values as empty list
        if type(price_dict) == str: #Checks if price_dict's type is a string
            return(price_dict) #If price_dict is a string than an error message was returned when calling the get_price_range_dict() method, so the error message is then returned to the user
        else:
            for date, price in price_dict.items(): #loops through each date price pair in the price dictionary
                x_values += [date] #Adds the date to the X_values list
                y_values += [price] #Adds the price to the y_values list
            plt.figure(figsize=(10, 5))  #Creates a new figure for plotting and sets the size to 10 inches wide by 5 inches tall, this controls how large the graph appears.
            plt.plot(x_values, y_values, marker='o', linestyle='-') #Plots the data points using the x_values and y_values.
            plt.xlabel('Date') #Sets the title of the x-axis of the graph to Date
            plt.ylabel('Price') #Sets the title of the y-axis of the graph to Price
            plt.title('Price Graph') #Sets the title of the graph to Price Graph
            plt.grid(True) #Makes the graph have a grid layout
            plt.tight_layout() #Makes the graph have a tight layout
            plt.show() #Displays the graph
   
    def get_returns(self, start_date, end_date):                                            
        price_range = self.get_price_range(start_date, end_date)  #Calls the get_price_range() method to get all the prices of the stock during the specified time peroid.
        if type(price_range) == str: #Checks if price_range's type is a string
            return(price_range)  #If price_range is a string than an error message was returned when calling the get_price_range() method, so the error message is then returned to the user
        else:
            result = [] #initialize results as empty list
            for i in range(1, len(price_range)): #Loops through each element in price_range
                daily_return = (price_range[i] - price_range[i-1]) / price_range[i-1] #Calculates the daily return by subtracting the price of the stock during the previous day from the current price of the stock and then dividing by the price of the stock during the previous day
                result += [daily_return] #Adds the daily return to the result list
            return(result) #Returns the result list, which contains the daily return of the stock for each day during the specified time period
       
    def get_volatility(self, start_date, end_date):
        returns = self.get_returns(start_date, end_date) #Calls the get_returns() method to get the daily returns of the stock during the specified time peroid.
        if type(returns) == str: #Checks if returns' type is a string
            return(returns)  #If returns is a string than an error message was returned when calling the get_price_range() method, so the error message is then returned to the user
        else:
            daily_vol = statistics.stdev(returns) #Calculates the standard deviation of the daily returns which represents the stock's day‑to‑day volatility.
            range_vol = daily_vol * (252 ** 0.5)  #Converts daily volatility into annualized volatility.
            return(range_vol) #Returns the annualized volatility of the stock.

    def get_max_Drawdown(self, start_date, end_date):
        price_range = self.get_price_range(start_date, end_date) #Calls the get_price_range() method to get all the prices of the stock during the specified time peroid.
        if type(price_range) == str: #Checks if price_range's type is a string
            return(price_range) #If price_range is a string than an error message was returned when calling the get_price_range() method, so the error message is then returned to the user
        else:
            max_price = price_range[0] #Sets the max_price equal to the first price in the price_range list
            max_drawdown = 0  #Sets the max_drawdown equal to zero    
            for price in price_range: #loops through each price in the price_range list
                if price > max_price: #Checks if the price is greater than the current max_price
                    max_price = price #Sets max_price equal to price

                drawdown = (price - max_price) / max_price #Caculates the drawdown by subtracting max_price from price and then dividing by the max_price
                if drawdown < max_drawdown: #Checks if drawdown is less than the max_drawdown
                    max_drawdown = drawdown #Sets the max_drawndown to drawndown
            return(max_drawdown) #Returns the maximum drawdown which represents the largest peak‑to‑trough decline in the stock's price.

    def Rolling_Averages_of_Returns(self, start_date, end_date, window):
        returns = self.get_returns(start_date, end_date)  #Calls the get_returns() method to get the daily returns of the stock during the specified time peroid.
        if type(returns) == str: #Checks if returns' type is a string
            return(returns) #If returns is a string than an error message was returned when calling the get_price_range() method, so the error message is then returned to the user
        else:
            if len(returns) < window: #Checks if the length of the returns list is less the length of the window
                return("Not enough data to compute rolling averages") #Returns a string telling the user that there is not enough data to compute the rolling averages with the current window size
            else:
                result = [] #initialize results as empty list
                for i in range(len(returns) - window + 1): #loops through the returns list and creates each rolling window. The loop stops at len(returns) - window + 1 so the slice never goes out of range.
                    average = sum(returns[i:i + window]) / window #Computes the average return over the current rolling window.
                    result += [average]  #Adds the rolling average to the result list
                return(result) #Returns the full list of rolling averages.

    def Moving_Averages(self, start_date, end_date, window):
        price_range = self.get_price_range(start_date, end_date) #Calls the get_price_range() method to get all the prices of the stock during the specified time peroid.
        if type(price_range) == str: #Checks if price_range's type is a string
            return(price_range) #If price_range is a string than an error message was returned when calling the get_price_range() method, so the error message is then returned to the user
        else:
            if len(price_range) < window:  #Checks if the length of the price_range is less the length of the window
                return("Not enough data to compute moving averages") #Returns a string telling the user that there is not enough data to compute the moving averages with the current window size
            else:
                result = [] #initialize results as empty list
                for i in range(len(price_range) - window + 1): #loops through price_range and creates each rolling window. The loop stops at len(returns) - window + 1 so the slice never goes out of range.
                    average = sum(price_range[i:i + window]) / window #Computes the rolling average over the current window of prices.
                    result += [average] #Adds the moving average to the result list
                return(result) #Returns the full list of moving averages.

    def Compare_Two_Stocks(self, stock2, Stat_method, *args): #Call the Compare_Two_Stocks() method like Stock_ticker.Compare_Two_Stocks(Stock2, stock_ticker.stat_method, start_date, end_date)
        if isinstance(stock2, Stock) != True: #Checks if stock2 is an object of the Stock class
            return('The second stock must be a stock object') #Returns a string telling the user that the stock2 must be an object of the Stock class
       
        statOne = Stat_method(*args) #Calls the method that was inputed by the user with *args as parameters to get the statistic for the first stock object
        statTwo =  getattr(stock2, Stat_method.__name__)(*args) #Calls the method that was inputed by the user with *args as parameters to get the statistic for the second stock object

        if type(statOne) == str: #Checks if statOne's type is a string
            return(statOne) #If StatOne is a string than an error message was returned when calling the method that was inputed by the user, so the error message is then returned to the user
        elif type(statTwo) == str: #Checks if statTwo's type is a string
            return(statTwo) #If StatTwo is a string than an error message was returned when calling the method that was inputed by the user, so the error message is then returned to the user
       
        if type(statOne) == list and type(statTwo) == list: #Checks if statOne's type is a list and that statTwo's type is a list as well.
            n = min(len(statOne), len(statTwo)) #Ensures both datasets are the same length by using the length of the shorter dataset.
            statOne = statOne[:n]  #Trims the stateOne list so that it has exactly n elements.
            statTwo = statTwo[:n]  #Trims the statTwo list so that it has exactly n elements.

            mean1 = statistics.mean(statOne) #Computes the average of the statOne list.
            mean2 = statistics.mean(statTwo) #Computes the average of the statTwo list.
            sdt1 = statistics.stdev(statOne) #Computes the standard deviation of the statOne list.         #standard deviation measures how spread out the values are.
            sdt2 = statistics.stdev(statTwo) #Computes the standard deviation of the StatTwo list.        
            t_stat = (mean1 - mean2) / (((sdt1**2 / n) + (sdt2**2 / n)) ** 0.5) #Calculates the t‑statistic for a two‑sample t‑test assuming unequal variances.
            p_value = 2 * (1 - t_dist.cdf(abs(t_stat), df=n-1)) #Computes the two‑tailed p‑value.
            if p_value < 0.05: #Checks if the p_value is less than the aplha of 0.05 (5%)
                return(f'The two stocks differ significantly at the 5% level\nMean-1: {mean1}\nMean-2: {mean2}\nt-statistic: {t_stat}\np-value: {p_value}') #Returns a formatted message indicating that the statistical test found a significant difference between the two stocks at the 5% level. Also, includes the means, t-statistic, and p-value for clarity.
            else:
                return(f'The two stocks do not differ significantly at the 5% level\nMean-1: {mean1}\nMean-2: {mean2}\nt-statistic: {t_stat}\np-value: {p_value}') #Returns a formatted message indicating that the statistical test did NOT find a significant difference between the two stocks at the 5% level. Also, includes the means, t-statistic, and p-value for clarity.
        return('Statistics are not comparable') #If StatOne and StatTwo are not list containg statistical information, then a string is returned to the user telling them that these two statistics are not comparable.

import tkinter as tk #imports the built in interface software
from tkinter import messagebox, simpledialog #imports two options from the tkinter inface for messageboxes and simple popups
from tkinter import scrolledtext #imports the scrolled text option so that popups with a lot of text can be scrollable
class Screens():
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to Stock Comparisons") #creates the title "Welcome to Stock Comparisons"
        self.root.geometry("500x500") # creates the size of the popup window

        self.active_stock = None #initializes stock

        # Create the Menu Frame
        self.main_menu = tk.Frame(self.root)
        self.main_menu.pack(expand=True, fill="both")

        tk.Label(self.main_menu, text="Please enter the Ticker of the stock here: ", font=("Arial", 10)).pack(pady=20) #creates a text box that says "Please enter the Ticker of the stock here: "
        self.stock_input = tk.Entry(self.main_menu, font=("Arial", 12)) #creates an import box for the user to insert the stock they want
        self.stock_input.pack(pady=10)
        tk.Button(self.main_menu, text="Click Me", command=self.confirmation_window).pack() #creates button that when clicked opens the confirmation window

    def clear_screen(self): #this is a helper function that clears the widgets from the root window
        """Helper to clear all widgets from the root window."""
        for widget in self.root.winfo_children(): #for every widget on the frame it deletes the package
            widget.pack_forget()

    def confirmation_window(self): #creates the second window
        # Hide the main menu
        ticker = self.stock_input.get().upper().strip() #initializes the ticker symbol from what the user inputted, but cleans and makes the string completely upper case
         
        if not ticker: #checks if there was no ticker symbol inputted
            messagebox.showwarning("Warning", "Please enter a ticker symbol.") #returns an error message and stops running the confirmation window
            return
       
        self.selected_ticker = ticker #saves it to the instance
        self.main_menu.pack_forget() #forgets the main menu frame

        # Create the Second Window Frame
        self.second_window = tk.Frame(self.root) #initializes the second frame
        self.second_window.pack(expand=True, fill="both") #fills the second frame

        tk.Label(self.second_window, text="Confirmation Window", font=("Arial", 10)).pack(pady=20) #creates a label at the top called confirmation window
       
        # Display the text from the first window
        tk.Label(self.second_window, text=f"Are you sure you want to select: {ticker}?", wraplength=250).pack(pady=10) #asks the user if they are sure this is the stock they want to check

        # Buttons Frame (to sit side-by-side)
        button_frame = tk.Frame(self.second_window) #creates a button frame below the question
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Yes", width=10, bg="green", fg="white", #creates a yes button that has a green background and a white text
                  command=lambda: self.initialize_and_go(ticker)).pack(side="left", padx=5) #when clicked this button goes to the helper function initialize and go for the inputted ticker symbol
       
        tk.Button(button_frame, text="No", width=10, bg="red", fg="white", #creates a no button that has a red background and a white text  
                  command=self.back_to_menu).pack(side="left", padx=5) #when clicked this button goes to the helper function back to menu and allows the user to input a different stock ticker
       
    def initialize_and_go(self, ticker):
        self.active_stock =  Stock(ticker) #this creates the stock from the RBT logic

        self.active_stock.update_historical_prices() #download the data
       
        tree_range = self.active_stock.get_min_max_range() #checks if the tree is actually filled
        if tree_range is None: #if the tree is empty
            messagebox.showerror("Error", f"Could not find data for {ticker}. Check your internet or ticker symbol.") #displays an  error message saying the stock could not be found
            self.back_to_menu() #calls the back to menu function
            return
   
        self.action_menu(ticker) #now moves to the action menu once the data is loaded

    def back_to_menu(self):
        # Remove second window and show main menu again
        self.second_window.destroy() # Using destroy to clear memory since it's recreated every time
        self.main_menu.pack(expand=True, fill="both") #returns the user to menu
   
    def show_scrollable_results(self, title, header, data_list):
        top = tk.Toplevel(self.root) # Create a new pop-up window
        top.title(title) #makes the title be one provided
        top.geometry("450x500") #sets the size to 450X500

        tk.Label(top, text=header, font=("Arial", 10, "bold")).pack(pady=10) # Add a header label

        text_area = scrolledtext.ScrolledText(top, width=40, height=20) #creates the text area with the built in python method scrolledtext and initializes the width and height
        text_area.pack(padx=10, pady=10, expand=True, fill="both") #uses the tkinterr packs geomtry manager to add 10 pixels to the vert and horz padding on the window and makes the widget be expandable

       
        formatted_data = "\n".join(data_list) #formats the data from the list to insert in a new line for every element in the list
   
        text_area.insert(tk.INSERT, formatted_data) #inserts the string formatted data into the text widget
        text_area.configure(state='disabled')  # Make it read-only

       
        tk.Button(top, text="Close", command=top.destroy).pack(pady=5) #creates a close button

    def action_menu(self, ticker):
        if hasattr(self, 'second_window'): #Checks whether the object already has an attribute named second_window
            self.second_window.destroy() #Closes and removes the existing second_window so a new one can be created cleanly

        self.third_window = tk.Frame(self.root) #creates a third window
        self.third_window.pack(expand=True, fill="both", padx=20, pady=20) #initializes the geometry

        tk.Label(self.third_window, text=f"Actions for: {ticker}", font=("Arial", 14, "bold")).pack(pady=10) #creates a title that has actions for {inserted ticker}

        # Date entries
        date_frame = tk.Frame(self.third_window)  #It creates a new Frame widget inside self.third_window, which acts as a container for organizing other widgets
        date_frame.pack(pady=10) #initializes the geometry of the date entry
        tk.Label(date_frame, text="Start:").grid(row=0, column=0) # creates an input box for the start date the user wants to search for
        self.start_entry = tk.Entry(date_frame) # sets start entry to the date inputted
        self.start_entry.grid(row=0, column=1) #intializes where the input box will be shown
        self.start_entry.insert(0, "2024-01-01") #intializes a given date if the user doesnt input one (just a random date that should be in the range of any stock inputted)

        tk.Label(date_frame, text="End:").grid(row=1, column=0) # creates an input box for the end date the user wants to search for
        self.end_entry = tk.Entry(date_frame) # sets end entry to the date inputted
        self.end_entry.grid(row=1, column=1)  #intializes where the input box will be shown
        self.end_entry.insert(0, (date.today() - timedelta(days=2)).isoformat())  #intializes a given date if the user doesnt input one (is set to be two days before the current date because the webscapping is up to current date completely)


        # Buttons
        grid_frame = tk.Frame(self.third_window) #It creates a new Frame widget inside self.third_window, which acts as a container for organizing the buttons
        grid_frame.pack(fill="both", expand=True) #It makes grid_frame stretch to fill all available space in its container and grow when the window grows.

        tk.Button(grid_frame, text="Get Returns", command=self.execute_returns).grid(row=0, column=0, sticky="nsew") #creates a button that is in the grid frame in the first row first column that calls the execute_returns function
        tk.Button(grid_frame, text="Show Graph", command=self.execute_graph).grid(row=0, column=1, sticky="nsew") #creates a button that is in the grid frame in the first row second column that calls the execute_graph function
        tk.Button(grid_frame, text= "Price Range",command=self.execute_price_range).grid(row=0,column = 2,sticky="nsew") #creates a button that is in the grid frame in the first row third column that calls the execute_price_range function
        tk.Button(grid_frame, text= "Average Price from Range",command=self.execute_get_average_price_from_range).grid(row=1,column = 0,sticky="nsew") #creates a button that is in the grid frame in the second row first column that calls the execute_get_average_price_from_Range function
        tk.Button(grid_frame, text= "Lowest Price from Range",command=self.execute_get_lowest_price_from_range).grid(row=1,column = 1,sticky="nsew") #creates a button that is in the grid frame in the second row second column that calls the execute_get_lowest_price_from_range function
        tk.Button(grid_frame, text= "Highest Price from Range",command=self.execute_get_highest_price_from_range).grid(row=1,column = 2,sticky="nsew") #creates a button that is in the grid frame in the second row third column that calls the execute_get_highest_price_from_range function
        tk.Button(grid_frame, text= "Lowest Price of all time",command=self.execute_lowest_price).grid(row=2,column = 0,sticky="nsew") #creates a button that is in the grid frame in the third row first column that calls the execute_get_lowest_price function
        tk.Button(grid_frame, text= "Highest Price of all time",command=self.execute_highest_price).grid(row=2,column = 1,sticky="nsew") #creates a button that is in the grid frame in the third row second column that calls the execute_get_highest_price function
        tk.Button(grid_frame, text= "Price at date",command=self.execute_price_at_day).grid(row=2,column = 2,sticky="nsew") #creates a button that is in the grid frame in the third row third column that calls the execute_price_at_day function
       
        #statistical analysis
        tk.Button(grid_frame, text= "Moving averages",command=self.execute_moving_averages).grid(row=3,column = 0,sticky="nsew") #creates a button that is in the grid frame in the fourth row first column that calls the execute_moving_averages function
        tk.Button(grid_frame, text= "Rolling averages",command=self.execute_rolling_averages).grid(row=3,column = 1,sticky="nsew")#creates a button that is in the grid frame in the fourth row second column that calls the execute_rolling_averages function
        tk.Button(grid_frame, text= "Get Max Drawdown",command=self.execute_get_max_drawdown).grid(row=3,column = 2,sticky="nsew")#creates a button that is in the grid frame in the fourth row third column that calls the execute_get_max_drawdown function
        tk.Button(grid_frame, text= "Get Volatility",command=self.execute_get_volatity).grid(row=4,column = 1,sticky="nsew")#creates a button that is in the grid frame in the fifth row first column that calls the execute_get_volatity function

        #special methods
        tk.Button(grid_frame, text= "Update Current Price",command=self.execute_update_current_price).grid(row=5,column = 0,sticky="nsew") #creates a button that is in the grid frame in the sixth row first column that calls the execute_update_current_price function
        tk.Button(grid_frame, text= "Update Historical Price",command=self.execute_update_historic_price).grid(row=5,column = 1,sticky="nsew") #creates a button that is in the grid frame in the sixth row second column that calls the execute_update_historic_price function
        tk.Button(grid_frame, text= "Compare two stocks ",command=self.execute_compare_two_stocks).grid(row=5,column = 2,sticky="nsew") #creates a button that is in the grid frame in the sixth row third column that calls the execute_compare_two_stocks function

        #main menu button
        tk.Button(self.third_window, text="Back to Main Menu", bg="gray", fg="white",  #creates a button at the bottom of the window that takes the user back to the main menu
                   command=self.show_main_menu).pack(pady=20)
       
    def execute_returns(self):
        if self.active_stock is None: #checks if there is no stock being searched for
            messagebox.showerror("Error", "No stock data loaded. Please go back and select a ticker.") #returns an error and stops running the program when the button is pressed
            return
        start = self.start_entry.get() #sets start to the start date inserted by the user
        end= self.end_entry.get() #sets end to the end date inserted by the user
        result = self.active_stock.get_returns(start, end) #runs the get_returns function in the stock class and stores the result
       
        if isinstance(result, str): #checks if the result is an instance of a str
            messagebox.showerror("Error", result) #returns a message box error that explains the input error to the user
        else:
            #  Get the sorted dates for the range to label each return
            price_dict = self.active_stock.get_price_range_dict(start, end) #makes the data into a pricerange dict
            sorted_dates = sorted(price_dict.keys()) #sorts the keys in the dict by date
           
            # Format the returns into strings with dates
            display_list = [] # creates a list
            for i in range(len(result)): #for every date in the length of result
                date_label = sorted_dates[i+1] # The date the return was realized
                display_list.append(f"{date_label}: {result[i]*100:.4f}%") #the list gets the date appended as well as the result value at that index

            # Pass the list of strings to the updated viewer
            self.show_scrollable_results("Calculation Success", f"Daily Returns for {self.active_stock.ticker_symbol}:", display_list) #calls tha show_scrollable results that displays success and a list of results that are scrollale when inputed into the get returns fuction

    def execute_graph(self):
        start = self.start_entry.get()#sets start to the start date inserted by the user
        end = self.end_entry.get() #sets end to the end date inserted by the user
        self.active_stock.make_graph(start, end) #runs the make_graph function in the stock class
   
    def execute_price_range(self):
        start = self.start_entry.get()#sets start to the start date inserted by the user
        end = self.end_entry.get() #sets end to the end date inserted by the user
     
        result_dict = self.active_stock.get_price_range_dict(start, end) #runs the get_price_range_dict function in the stock class and stores it in a results_dict
       
        if isinstance(result_dict, str): #checks if the result is an instance of a str
            messagebox.showerror("Error", result_dict) #returns a message box error that explains the input error to the user
        else:
            sorted_dates = sorted(result_dict.keys()) #sorts the keys in the dict by date
            display_list = [] # creates a list for the values to be displayed
           
            for date_key in sorted_dates: #for each date in the stored dates dict
                price = result_dict[date_key] #sets the price to the value of that key
                display_list.append(f"{date_key}: ${price:.2f}") #appedns each value to the display list

            #Pass the list of formatted strings to the updated viewer
            self.show_scrollable_results("Calculation Success", f"Historical Prices for {self.active_stock.ticker_symbol}:", display_list) #calls tha show_scrollable results that displays success and a list of results that are scrollale when inputed into the get returns fuction

   
    def execute_get_average_price_from_range(self):
        start = self.start_entry.get()#sets start to the start date inserted by the user
        end = self.end_entry.get() #sets end to the end date inserted by the user
        result = self.active_stock.get_average_price_from_range(start, end) #runs the get_average_price_from_Range in the stock class with the given start and stop dates and stores it in results
        messagebox.showinfo("Success", f"The average price from the range is {result}") #returns the f string that has the average price from that range in a pop up


    def execute_get_lowest_price_from_range(self):
        start = self.start_entry.get()#sets start to the start date inserted by the user
        end = self.end_entry.get() #sets end to the end date inserted by the user
        result = self.active_stock.get_lowest_price_from_range(start, end) #runs the get_lowest_price_from_Range in the stock class with the given start and stop dates and stores it in results
        messagebox.showinfo("Success", f"The lowest price from the range is {result}")  #returns the f string that has the lowest price from that range in a pop up


    def execute_get_highest_price_from_range(self):
        start = self.start_entry.get()#sets start to the start date inserted by the user
        end = self.end_entry.get() #sets end to the end date inserted by the user
        result = self.active_stock.get_highest_price_from_range(start, end) #runs the get_highest_price_from_Range in the stock class with the given start and stop dates and stores it in results
        messagebox.showinfo("Success", f"The highest price from the range is {result}")  #returns the f string that has the highest price from that range in a pop up


    def execute_lowest_price(self):
        if self.active_stock is None: #checks if there is no stock being searched for
            messagebox.showerror("Error", "No stock data loaded.") #returns an error and stops running the program when the button is pressed
            return
        result = self.active_stock.get_lowest_price() #sets result to the stock with the given ticker and calls get_lowest price
        if result and result[0] != float('-inf'): #checks that result is not empty and also that its first element is not negative infinity.
            price, dates = result # this unpacks the data in results and splits it into two seperate variables price and date
       
            date_str = ", ".join(dates)# Format the dates into a string and if there are many dates, we join them with commas.
       
            message = (f"The all-time lowest adjusted close for " f"{self.active_stock.ticker_symbol} is:\n\n" f"${price:.2f}\n\n" f"Occurred on: {date_str}") #creates the message for the pop up that shows text with the inputted ticker symbol as well as the lowest price and the day it occured on
       
            messagebox.showinfo("Lowest Price Found", message) #sets the title and message of the popup
        else:
            messagebox.showwarning("No Data", "Could not determine highest price. The tree might be empty.") #returns that there was no data in that branch of the tree and to double check the stock is correctly inputted

    def execute_highest_price(self):
        if self.active_stock is None: #checks if there is no stock being searched for
            messagebox.showerror("Error", "No stock data loaded.") #returns an error and stops running the program when the button is pressed
            return
        result = self.active_stock.get_highest_price() #sets result to the stock with the given ticker and calls get_highest_price
        if result and result[0] != float('-inf'): #checks that result is not empty and also that its first element is not negative infinity.
            price, dates = result # this unpacks the data in results and splits it into two seperate variables price and date
       
            date_str = ", ".join(dates) # Format the dates into a string and if there are many dates, we join them with commas.
       
            message = (f"The all-time highest adjusted close for " f"{self.active_stock.ticker_symbol} is:\n\n" f"${price:.2f}\n\n" f"Occurred on: {date_str}")#creates the message for the pop up that shows text with the inputted ticker symbol as well as the lowest price and the day it occured on
       
            messagebox.showinfo("Highest Price Found", message) #sets the title and message of the popup
        else:
            messagebox.showwarning("No Data", "Could not determine highest price. The tree might be empty.") #returns that there was no data in that branch of the tree and to double check the stock is correctly inputted

    def execute_price_at_day(self):
        if self.active_stock is None: #checks if there is no stock being searched for
            messagebox.showerror("Error", "No stock data loaded.") #returns an error and stops running the program when the button is pressed
            return

        target_date = simpledialog.askstring("Input Date", "Enter the date you want to check (YYYY-MM-DD):",parent=self.root) #Ask the user for the date in a popup

        if target_date: #If the user clicks 'Cancel', target_date will be None
            target_date = target_date.strip() # if not then the target date will strip the inserted string

            result = self.active_stock.get_price_at_date(target_date) #sets reslt to the price of date when called in the stock class with the users desired date

            #Responses
            if isinstance(result, str): # if the 'The date is not valid' or 'outside of the range'
                messagebox.showerror("Error", result) #return an error message
            elif result is None: # checks if there are no results for a specific date
                messagebox.showinfo("No Data", f"The market was closed on {target_date}.")  #return a message that tells the user that there is no data from that day because the market was closed
            else:
                messagebox.showinfo("Price Found", f"Ticker: {self.active_stock.ticker_symbol}\n" f"Date: {target_date}\n" f"Adjusted Close: ${result:.2f}") #returns a success and displaces the first from the users given date

    def execute_moving_averages(self):
        if self.active_stock is None:  #checks if there is no stock being searched for
            messagebox.showerror("Error", "No stock data loaded.") #returns an error and stops running the program when the button is pressed
            return
        window_size = simpledialog.askinteger("Input Window", "Enter the window size (number of days):", parent=self.root, minvalue=1) #opens an input window to get the users wanted window size
       
        if window_size:  #checks if the window size is valid for that given stock
            start = self.start_entry.get()#sets start to the start date inserted by the user
            end = self.end_entry.get() #sets end to the end date inserted by the user
            result = self.active_stock.Moving_Averages(start, end, window_size) #calls the moving averages function in the stock class
           
            if isinstance(result, str): #checks if the result is an instance of a str
                messagebox.showerror("Error", result) #returns a message box error that explains the input error to the user
            else:
                price_dict = self.active_stock.get_price_range_dict(start,end) #creates a diction of the price range from the given start and end dates
                sorted_dates = sorted(price_dict.keys()) #sorts the keys (dates) by date

                display_lst = [] #initializes a new list to display
                for i in range(len(result)): #goes through every element in the date list from the given range
                    range_text = f"{sorted_dates[i]} to {sorted_dates[i + window_size - 1]}" #creates a message of the range with the dates sorted from start to end
                    display_lst.append(f"{range_text}: ${result[i]:.2f}") #appends the element to the list with the price
                self.show_scrollable_results(f"{window_size}-Day Moving Average", f"Moving Average Prices for {self.active_stock.ticker_symbol}:", display_lst) #opens a scrollable window and formats the list to show day #: $Price
               

    def execute_rolling_averages(self):
        if self.active_stock is None: #checks if there is no stock being searched for
            messagebox.showerror("Error", "No stock data loaded.") #returns an error and stops running the program when the button is pressed
            return
        window_size = simpledialog.askinteger("Input Window", "Enter the window size (number of days):", parent=self.root, minvalue=1) #opens an input window to get the users wanted window size
       
        if window_size:  #checks if the window size is valid for that given stock
            start = self.start_entry.get()#sets start to the start date inserted by the user
            end = self.end_entry.get() #sets end to the end date inserted by the user
            result = self.active_stock.Rolling_Averages_of_Returns(start, end, window_size) #calls the rolling averages function in the stock class
           
            if isinstance(result, str):  #checks if the result is an instance of a str
                messagebox.showerror("Error", result) #returns a message box error that explains the input error to the user
            else:
                price_dict = self.active_stock.get_price_range_dict(start, end) #creates a diction of the price range from the given start and end dates
                sorted_dates = sorted(price_dict.keys()) #sorts the keys (dates) by date
               
                display_list = [] #initializes a new list to display
                for i in range(len(result)):   #goes through every element in the date list from the given range
                   
                    range_text = f"{sorted_dates[i]} to {sorted_dates[i + window_size]}" #  sets the text for the return window at i starts at date i and ends at date i + window_size
                    display_list.append(f"{range_text}: {result[i]*100:.4f}%") #appends that text to the display list
               
                self.show_scrollable_results(f"Rolling {window_size}-Day Returns", f"Average Returns for {self.active_stock.ticker_symbol}:",  display_list) #opens a scrollable window and formats the list to show day and the returns for that day

    def execute_get_max_drawdown(self):
        if self.active_stock is None: #checks if there is no stock being searched for
            messagebox.showerror("Error", "No stock data loaded.") #returns an error and stops running the program when the button is pressed
            return
        start = self.start_entry.get()#sets start to the start date inserted by the user
        end = self.end_entry.get() #sets end to the end date inserted by the user

        result = self.active_stock.get_max_Drawdown(start, end) #calls the get_max_drawdown function in the stock class
       
        if isinstance(result, str): #checks if the result is an instance of a str
                messagebox.showerror("Error", result) #returns a message box error that explains the input error to the user
        else:
            percentage = result * 100 #make the result into a percentage
            message = (f"Maximum Drawdown for {self.active_stock.ticker_symbol}:\n\n" f"{percentage:.2f}%\n\n" f"This represents the largest drop from a peak to a \n" f"subsequent low during the selected period.") #creates a method to display the result as a percent with teh range inputed by the user
            messagebox.showinfo("Risk Analysis", message) #creates a message popup titled risk analysis

    def execute_get_volatity(self):
        if self.active_stock is None: #checks if there is no stock being searched for
            messagebox.showerror("Error", "No stock data loaded.") #returns an error and stops running the program when the button is pressed
            return

        start = self.start_entry.get()#sets start to the start date inserted by the user
        end = self.end_entry.get() #sets end to the end date inserted by the user
   
        result = self.active_stock.get_volatility(start, end) #calls the get_volatity function in the stock class

        if isinstance(result, str): #checks if the result is an instance of a str
            messagebox.showerror("Error", result) #returns a message box error that explains the input error to the user
        else:
            annual_vol = result * 100 # since volatity is usually displayed as an annualized percentage this turns the result into a percent
       
            message = (f"Annualized Volatility for {self.active_stock.ticker_symbol}:\n\n" f"{annual_vol:.2f}%\n\n" f"This represents the 'intensity' of price movements.\n" f"Higher percentages indicate higher risk/reward.") #creates a popup to display the annual volatility and display this percentage with the inputted ticker symbol and the percentage
            #also include a message that shows what the precentage represents (higher = bad etc)        
            messagebox.showinfo("Volatility Analysis", message)  # creates the popup with the title and the message

    def execute_update_current_price(self):
        if self.active_stock is None: #checks if there is no stock being searched for
            messagebox.showerror("Error", "No stock data loaded.") #returns an error and stops running the program when the button is pressed
            return
       
        result = self.active_stock.update_current_price() #creates a result based on the return alue from update_current_price from the stock class

        if isinstance(result, str): #checks if there was an error in the formmating of the stock
            messagebox.showerror("API Error", result) # This catches "Not a valid ticker symbol" or API errors
        else:
            message = (f"Current Market Price for {self.active_stock.ticker_symbol}:\n\n" f"${result:.2f}\n\n" f"Note: This price is fetched from Yahoo Finance \n" f"and represents the most recent regular market price.") # formats the message and the price to 2 decimal places for currency
       
        messagebox.showinfo("Live Quote", message) # creates the popup with the title and the message

    def execute_update_historic_price(self):
        if self.active_stock is None: #checks if there is no stock being searched for
            messagebox.showerror("Error", "No stock data loaded.")#returns an error and stops running the program when the button is pressed
            return

        confirm = messagebox.askyesno("Confirm Refresh", f"This will delete all current data for {self.active_stock.ticker_symbol} " "and re-download the entire history. This may take a moment. Continue?")# creates a popup that confirms with the user first since this deletes the current tree
   
        if confirm: #if the user presses yes on the confirm box
        # This takes 2-5 seconds depending on the stock's age
            result = self.active_stock.update_historical_prices() #creates a result based on the return alue from update_current_price from the stock class
       
        # Once finished, show the success message
            messagebox.showinfo("Database Updated", f"Successfully refreshed {self.active_stock.ticker_symbol}.\n\n{result}") #creates a popup that says that the try was successfully cleared and checked
 
    def execute_compare_two_stocks(self):
        if self.active_stock is None: #checks if there is no stock being searched for
            messagebox.showerror("Error", "No stock Data loaded.")  #returns an error and stops running the program when the button is pressed
            return
        ticker2 = simpledialog.askstring("Compare Stocks", "Enter second ticker (e.g., MSFT):") #initializes the second ticker for the stock the user wants to compare with the current stock
        if not ticker2: #checks that ticker2 is actually a stock and exits if it isnt
            return
       
        try:
            stock2 = Stock(ticker2.upper().strip()) #creates a cleaned stock object
            stock2.update_historical_prices() #gets the updated historical price for that stock item
        except Exception as e: #catches errors that occur while creating the stock and loading in its historical data
            messagebox.showerror("Error", f"Could not load {ticker2}: {e}") #returns a message box saying that stock could be loaded
            return #stops the function
       
        choice = messagebox.askyesno("Comparison Type", "Compare Daily Returns?\n(Select 'No' for Rolling Averages)") #creates a yes no popup that if yes it will run the function to compare daily returns, if no it will run rolling averages
   
        start = self.start_entry.get()#sets start to the start date inserted by the user
        end = self.end_entry.get() #sets end to the end date inserted by the user
        if choice: #checks to see if choice is yes
            result = self.active_stock.Compare_Two_Stocks(stock2, self.active_stock.get_returns, start, end) #calls compare when the arg is get_returns
        else: # User chose Rolling Averages
            win = simpledialog.askinteger("Window", "Enter window size:", minvalue=1) #creates another popup to ask the user what the want the window of study to be
            if not win:  #if the data set is not in the window return error
                return
            result = self.active_stock.Compare_Two_Stocks(stock2, self.active_stock.Rolling_Averages_of_Returns, start, end, win) #else result calls compare two stocks with the arg* being rolling averages for the two stocks provided
   
        messagebox.showinfo("T-Test Comparison Results", result)# sets up a return box using the info box feature with all the results on their own line
   
    def show_main_menu(self):
        self.clear_screen() #calls the helper function clear screen
        self.main_menu.pack(expand=True, fill="both") #resets the size of the main menu
 
if __name__ == "__main__":
    root = tk.Tk() #runs the root
    app = Screens(root) #imports the roots into the screen function
    root.mainloop() #creates the main loop that mains the ui appear on the users screen
