import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import requests
import numpy as np
from autocomplete_entry import AutocompleteEntry  # Import the custom autocomplete entry class
import csv
from ml_model_1 import xgb_model





total_burned_calories = -2000
total_eaten_calories = 0

# Read the CSV file and create a dictionary mapping food items to their calorie values
csv_file_path = 'calories.csv'  # Update this path if necessary
food_calories = {}

with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        food_calories[row['FoodItem'].strip().lower()] = float(str(row['Cals_per100grams'].split(' cal')[0]))


def select_image_and_detect_food():
    # Open a file dialog to select the image
    img_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

    if img_path:  # Proceed only if a file is selected
        api_user_token = '2710ac37c1819349968b4936d26201cc149ecfa1'
        headers = {'Authorization': 'Bearer ' + api_user_token}

        # Food Type Detection
        api_url = 'https://api.logmeal.es/v2'
        endpoint = '/image/recognition/dish'

        try:
            response = requests.post(api_url + endpoint,
                                     files={'image': open(img_path, 'rb')},
                                     headers=headers)

            response.raise_for_status()  # Raise an exception for HTTP errors
            resp = response.json()

            # Loop through food_types and print the name with highest probability
            max_prob = 0
            max_name = ''
            for food in resp['recognition_results']:
                if food['prob'] > max_prob:
                    max_prob = food['prob']
                    max_name = food['name'].lower()
            print(max_name)

            # Set the name of the food in the Entry widget
            food_name_entry.delete(0, tk.END)
            food_name_entry.insert(0, max_name)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {e}")



def summarize_and_reset_day():
    global total_burned_calories, total_eaten_calories

    # Calculate net calories
    net_calories = total_eaten_calories + total_burned_calories

    # Update the output field with the result
    summary_result_label.config(text=f"Net Calories for the Day: {net_calories:.2f}")

    # Reset the total counters and update summary labels
    total_burned_calories = -2000
    total_eaten_calories = 0
    update_summary_labels()


def update_summary_labels():
    burned_calories_summary_label.config(text=f"Total Burned Calories: {total_burned_calories:.2f}")
    eaten_calories_summary_label.config(text=f"Total Eaten Calories: {total_eaten_calories:.2f}")

# Function to calculate burned calories using the xgb_model
# Function for calculating calories in food
def calculate_food_calories(food_name, quantity):
    try:
        calories_per_100g = food_calories[food_name]
        total_calories = (float(quantity)/100) * calories_per_100g
        return total_calories
    except KeyError:
        messagebox.showerror("Error", f"{food_name} not found in the database.")
    except ValueError:
        messagebox.showerror("Error", "Invalid quantity. Please enter a numeric value.")
        return None

# Function called when the Calculate button in the Food tab is clicked
def on_calculate_food_click():
    global total_eaten_calories
    food_name = food_name_entry.get().strip().lower()
    quantity = quantity_entry.get().strip()

    if not food_name or not quantity:
        messagebox.showerror("Error", "Please fill in both fields")
        return

    calories = calculate_food_calories(food_name, quantity)
    if calories is not None:
        total_eaten_calories += calories
        update_summary_labels()
        calories_label.config(text=f"Calories in Food: {calories:.2f}")

def calculate_burned_calories():
    try:
        # Initialize the data array with the gender value
        data = [float(gender_combobox.get() == 'Female')]  # 0 for Male, 1 for Female

        # Append the numeric values from the entry widgets to the data array
        for entry in entries:
            data.append(float(entry.get()))

        # Convert the data to a numpy array and reshape for prediction
        data = np.array(data).reshape(1, -1)

        # Predict the burned calories using the xgb_model
        predicted_calories = xgb_model.predict(data)
        return float('{:.3f}'.format(predicted_calories[0]))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

# Function to collect and validate data, then update the label
def collect_data():
    global total_burned_calories
    # Check if the gender is selected
    if gender_combobox.get() not in ["Male", "Female"]:
        messagebox.showerror("Error", "Please select a gender")
        return

    # Check if any field is empty
    if any(not entry.get().strip() for entry in entries):
        messagebox.showerror("Error", "You need to fill all fields")
        return

    # Calculate burned calories
    burned_calories = calculate_burned_calories()

    # Update the label with the calculated value
    if burned_calories is not None:
        total_burned_calories -= burned_calories
        update_summary_labels()
        burned_calories_label.config(text=f"Burned Calories: {burned_calories}")

# Create the main window

root = tk.Tk()
root.title("Health & Nutrition Calculator")
root.geometry("400x500")# Set the window size


# Configure the style
style = ttk.Style()
style.configure("TButton", font=("Roboto", 14), borderwidth=2)
style.configure("TLabel", font=("Roboto", 14))
style.configure("TEntry", font=("Roboto", 14), borderwidth=2)





# Create the tab control
tabControl = ttk.Notebook(root)

# Create the Training tab
tabTraining = ttk.Frame(tabControl)
tabControl.add(tabTraining, text='Training')

# Labels and input fields for the Training tab
labels = ["Age", "Height", "Weight", "Duration", "Heart Rate", "Body Temperature"]
entries = []  # List to keep track of the entry widgets

# Gender Combobox for Training tab
gender_label = ttk.Label(tabTraining, text="Gender")
gender_label.grid(column=0, row=0, sticky=tk.W, padx=10, pady=5)
gender_combobox = ttk.Combobox(tabTraining, values=["Male", "Female"], state="readonly")
gender_combobox.grid(column=1, row=0, sticky=tk.EW, padx=10, pady=5)

# Create the input fields for the other labels in Training tab
for i, text in enumerate(labels, start=1):
    label = ttk.Label(tabTraining, text=text)
    label.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)
    entry = ttk.Entry(tabTraining)
    entry.grid(column=1, row=i, sticky=tk.EW, padx=10, pady=5)
    entries.append(entry)

# Calculate button for Training tab
calculate_training_button = ttk.Button(tabTraining, text="Calculate", style='TButton', command=collect_data)
calculate_training_button.grid(column=0, row=len(labels)+1, columnspan=2, pady=10)

# Burned Calories label for Training tab
burned_calories_label = ttk.Label(tabTraining, text="Burned Calories: ")
burned_calories_label.grid(column=0, row=len(labels)+2, columnspan=2, sticky=tk.W, padx=10, pady=5)

# Create the Food tab
tabFood = ttk.Frame(tabControl)
tabControl.add(tabFood, text='Food')

# Food Name input field for Food tab
food_name_label = ttk.Label(tabFood, text="Name of Food:")
food_name_label.grid(column=0, row=0, sticky=tk.W, padx=10, pady=5)
food_name_entry = AutocompleteEntry(list(food_calories.keys()), tabFood)
food_name_entry.grid(column=1, row=0, sticky=tk.EW, padx=10, pady=5)


# Button to select an image and detect food
take_image_button = ttk.Button(tabFood, text="Take Image", command=select_image_and_detect_food)
take_image_button.grid(column=0, row=4, columnspan=2, pady=10)

# Quantity input field for Food tab
quantity_label = ttk.Label(tabFood, text="Quantity of grams/ml:")
quantity_label.grid(column=0, row=1, sticky=tk.W, padx=10, pady=5)
quantity_entry = ttk.Entry(tabFood)
quantity_entry.grid(column=1, row=1, sticky=tk.EW, padx=10, pady=5)

# Calculate button for Food tab
calculate_food_button = ttk.Button(tabFood, text="Calculate", style='TButton', command=on_calculate_food_click)
calculate_food_button.grid(column=0, row=2, columnspan=2, pady=10)

# Label to display calculated calories for Food tab
calories_label = ttk.Label(tabFood, text="Calories in Food: ")
calories_label.grid(column=0, row=3, columnspan=2, sticky=tk.W, padx=10, pady=5)

# Create the Summarize tab
tabSummarize = ttk.Frame(tabControl)
tabControl.add(tabSummarize, text='Summarize')

# Labels for the Summarize tab
burned_calories_summary_label = ttk.Label(tabSummarize, text="Total Burned Calories: 0")
burned_calories_summary_label.pack(pady=10)

eaten_calories_summary_label = ttk.Label(tabSummarize, text="Total Eaten Calories: 0")
eaten_calories_summary_label.pack(pady=10)

# Button to summarize and reset the day
summarize_day_button = ttk.Button(tabSummarize, text="Summarize Your Day", style='TButton', command=summarize_and_reset_day)
summarize_day_button.pack(pady=10)

# Label to display the net calories after summarizing
summary_result_label = ttk.Label(tabSummarize, text="")
summary_result_label.pack(pady=10)

# Pack to make visible
tabControl.pack(expand=1, fill="both")

# Start the GUI
root.mainloop()