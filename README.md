# CMPSC-132-Final
Project Description:

For our project, we decided to create an interface where a user can insert a ticker symbol for a stock. Then our program will scrape all the adjusted daily closing prices for the stock associated with the ticker symbol from Yahoo Finance. After the program gathers the desired information from the stock, the interface prompts the users with multiple actions they can perform on the data. First, the interface asks the user to input a start date and end date for the range on which the user wants to perform an action. If the user doesn’t input a range, the program sets the start date to the first day of trading for that stock and sets the end date to the most recent day where an adjusted daily closing price is available. This is usually three days prior to the current day because it takes a while for Yahoo to update its historical data. Secondly, the interface has multiple buttons that allow the user to perform an analysis on the stock. These include getting the returns for a specified range, showing the price graph over the range, displaying the prices of the stock over the given range, showing the average, lowest, or highest price of the stock in the range, and price on a specific date. Additionally, there are four statistical analysis functions provided: calculate the moving averages for a specific window, calculate the rolling averages for a specific window, get the max drawdown from the provided range, and get the volatility of the stock. Lastly, there are three special methods that have buttons on the interface, and these are update current price, update historical price, and compare two stocks. 


Program Instructions 
First, open the python file in VS Code and enter the following pip command in a terminal to install the correct libraires/packages needed for our program to operate

Pip Commands:
1.	python -m pip install requests
2.	pip install pandas
3.	python -m pip install -U matplotlib
4.	pip install scipy

Next, run the python file and a user interface will appear promoting you to input a ticker symbol. A ticker symbol is a unique series of letters or numbers used to identify a publicly traded stock; please look up a stock and its associated ticker symbol to input into the interface (we recommend using ticker symbol TSLA for tesla). Once you input a ticker symbol into the interface, hit the click me button, to move onto the confirmation window. Once at the confirmation window, text will appear asking you if the displayed ticker symbol is correct, click YES to move to the next window or NO to go back to the previous window. After you click yes, it will take a couple of minutes to scrape the stock information from Yahoo Finance, so please be patient. Once the information is gathered, you will be moved to the final stock analysis window. Here you will be prompted for a start and end date, this is the range for which each analysis will be performed. On the stock analysis window, you see the following buttons please click on the button to perform the desired action. 

Buttons:

•	Get returns: calculates and display a list containing the daily return of the stock for each day during the specified period 
•	Show graph: creates a graph that displays the price of the stock for each day in the specified time range. Please be patient, this function takes a significant amount of time to create the graph. If the range inputted by the user is invalid, then nothing is returned by clicking the button.
•	Price Range: displays the adjusted closing price of the stock for each day in the specified range. If the range is invalid, then an error message is displayed. 
•	Average Price from Range:  calculates and displays the average price of the stock during the specified time. If the range is invalid, then an error message is displayed. 
•	Lowest Price from Range: Finds and displays the lowest price of the stock during the specified period. If the range is invalid, then an error message is displayed. 
•	Highest Price from Range: Finds and displays the highest price of the stock during the specified period. If the range is invalid, then an error message is displayed. 
•	Lowest price of all time: Finds and displays the lowest all-time price of the stock.
•	Highest price of all time: Finds and displays the highest all-time price of the stock. 
•	Price at date: Finds the price of the stock at the selected date, If the date is invalid then an error message is returned. This button is also used to get the last closing price of the stock. 
•	Moving Averages: Once the button is clicked, a window will appear prompting the user to enter a number representing the range over which the average price of the stock will be calculated. If either range is invalid, then an error message will be displayed. 
•	Rolling Averages of Returns: Once the button is clicked, a window will appear prompting the user to enter a number representing the range over which the average return of the stock will be calculated. If either range is invalid, then an error message will be displayed. 
•	Get Max Drawdown: Calculates and displays the maximum drawdown which represents the largest peak to trough decline in the stock's price over the specified period of time. If the range is invalid, then an error messaged is displayed. 
•	Update current price: A method that updates the current price of the stock. Please be patient, this function takes a significant amount to update the current price of the stock. Nothing is returned by this function. 
•	Update historical prices: A method that updates the historical prices of the stock. Please be patient, this function takes a significant amount to update the historical prices of the stock. Nothing is returned by this function. 
•	Compare stocks: Once this button is clicked a window appears prompting the user for another ticker symbol. After the second ticker symbol is inputted, a second window will appear asking the user to select if they want to compare the moving average or the rolling averages of returns for the two stocks over the specified time range. A statical analysis will be displayed if the range and ticker symbol are valid, else an error message will be displayed. 
