from datetime import datetime

class Node:
    def __init__(self, key, value):
        self.key = key 
        self.value = value
        self.right = None
        self.left = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if key < node.key:
            if node.left == None:
                node.left = Node(key, value)
            else:
                self._insert(node.left, key, value)
        elif key > node.key:   
            if node.right == None:
                node.right = Node(key, value)
            else:
                self._insert(node.right, key, value)
        else:
            node.value = value
    
    def validate_key(self, key):
        if type(key) != int:
            return(False)
        
        key = str(key)
        if len(key) != 8:
            return(False)
        
        try:
            datetime.strptime(key, "%Y%m%d")
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
        return(self._delete_tree_helper(self.root))
    
    def _delete_tree_helper(self, node):
        if node == None:
            return(None)
        
        self._delete_tree_helper(node.left)
        self._delete_tree_helper(node.right)

        node.right = None
        node.left = None

class Stock(BST):
    def __init__(self, current_price):
        super().__init__()
        self.__current_price = current_price

    def get_current_price(self):
        return(self.__current_price)
    
    def get_price_at_date(self, date_key):
        if super().validate_key(date_key) == False:
            return('The date is not valid')
        
        range_dict = super().get_min_max_range()
        if not(range_dict['min_key'] <= date_key <= range_dict['max_key']): 
            return("The date is out side of the range")
        
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
        if not(range_dict['min_key'] <= start_date <= range_dict['max_key']):
            return("The start date is out side of the range")
        elif not(range_dict['min_key'] <= end_date <= range_dict['max_key']):
            return("The end date is out side of the range")
        
        return(super().search_range(start_date, end_date))
    
    def get_price_range_dict(self, start_date, end_date):                           #Implemenet 
        pass
    
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
    
    def get_returns(self, start_date, end_date):                                     #Add Implementation to include shares          
        price_range = self.get_price_range(start_date, end_date)
        if type(price_range) == str:
            return(price_range)
        else:
            return(price_range[len(price_range) - 1] - price_range[0])

    def get_volatility(self, start_date, end_date):                                   #Implemenet 
        pass



ticker_symbol = input("Please input a ticker symbol: ")
