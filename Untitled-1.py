import tkinter as tk
class Screens:
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

        tk.Button(self.third_window, text="Back to Main Menu", bg="blue", fg="orange", 
                  command=self.show_main_menu).pack(pady=20)

    def show_main_menu(self):
        self.clear_screen()
        self.main_menu.pack(expand=True, fill="both")
if __name__ == "__main__":
    root = tk.Tk()
    app = Screens(root)
    root.mainloop()

# update historical prices 
# update current price 
#moving averages 
#rolling averages 
#compare two stocks
#maxdrawdown
#get volatility
#get returns 
#make graph 
