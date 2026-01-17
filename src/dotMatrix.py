import pandas as pd
import tkinter as tk

def import_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error importing CSV: {e}")
        return None



# set up
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Railboard")
    window.geometry("800x600")

    window.mainloop()