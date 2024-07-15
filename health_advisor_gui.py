import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk # type: ignore
import requests # type: ignore

# Function to process the data and provide health advice
def process_data():
    try:
        age = int(age_entry.get()) # type: ignore
        weight = float(weight_entry.get()) # type: ignore
        height = float(height_entry.get()) # type: ignore
        steps_per_day = int(steps_entry.get()) # type: ignore
        heart_rate = int(heart_rate_entry.get()) # type: ignore
        sleep_hours = float(sleep_entry.get()) # type: ignore
        calories_intake = int(calories_entry.get()) # type: ignore
        cholesterol_level = int(cholesterol_entry.get()) # type: ignore

        bmi = weight / (height / 100) ** 2
        health_score = (age * 0.1 + bmi * 0.2 + steps_per_day * 0.2 + heart_rate * 0.1 +
                        sleep_hours * 0.2 + calories_intake * 0.1 + cholesterol_level * 0.1)

        if health_score > 2000:
            advice = "Your health score is high. Keep up the good work!"
            test_advice = "No additional tests needed."
            nearest_hospital = ""
        elif health_score > 1500:
            advice = "Your health score is moderate. Consider regular exercise and a balanced diet."
            test_advice = "Consider routine blood tests."
            nearest_hospital = ""
        else:
            advice = "Your health score is low. Please consult a doctor."
            test_advice = "Consider a comprehensive health check-up."
            # Find nearest hospital using Google Maps API
            api_key = 'AIzaSyDY5qLH0Uvz1HCSPWbSqzGJs0XRSUtOyDc'  # Replace with your actual API key
            location = '8.5241,76.9366'  # Trivandrum coordinates
            hospital_response = requests.get(
                f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius=5000&type=hospital&key={api_key}')
            hospitals = hospital_response.json().get('results', [])
            if hospitals:
                nearest_hospital = f"\nNearest Hospital: {hospitals[0].get('name', 'Unknown')}"
            else:
                nearest_hospital = "\nNearest Hospital: Not found"

        output_text.set(
            f"Health Score: {health_score:.2f}\nAdvice: {advice}\nTests Recommended: {test_advice}{nearest_hospital}")

    except ValueError:
        messagebox.showerror("Input error", "Please enter valid numeric values.")

# Function to reset the application
def reset_application():
    age_entry.delete(0, tk.END) # type: ignore
    weight_entry.delete(0, tk.END) # type: ignore
    height_entry.delete(0, tk.END) # type: ignore
    steps_entry.delete(0, tk.END) # type: ignore
    heart_rate_entry.delete(0, tk.END) # type: ignore
    sleep_entry.delete(0, tk.END) # type: ignore
    calories_entry.delete(0, tk.END) # type: ignore
    cholesterol_entry.delete(0, tk.END) # type: ignore
    output_text.set("")

# Create the main application window
root = tk.Tk()
root.title("AI Health Advisor")
root.geometry("800x600")

# Set the theme colors
root.configure(bg='white')

# Load and set the background image
try:
    background_image = Image.open("health_advisor.png")
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root, image=background_photo)
    background_label.image = background_photo  # Keep a reference to prevent garbage collection
    background_label.place(relwidth=1, relheight=1)
except FileNotFoundError:
    messagebox.showerror("File Not Found", "The image 'health_advisor.png' was not found. Please ensure it is in the directory.")

# Create a frame to hold the widgets and place it on top of the background
frame = tk.Frame(root, bg='white', bd=6)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.8, anchor='n')

# Create the heading
heading_label = tk.Label(root, text="AI HEALTH ADVISOR", font=("Times New Roman", 20, "bold"), bg='white', fg='navy')
heading_label.place(relx=0.5, rely=0.02, anchor='n')

# Create input fields
fields = {
    "Age": "age_entry",
    "Weight (kg)": "weight_entry",
    "Height (cm)": "height_entry",
    "Steps per Day": "steps_entry",
    "Heart Rate": "heart_rate_entry",
    "Sleep Hours": "sleep_entry",
    "Calories Intake": "calories_entry",
    "Cholesterol Level": "cholesterol_entry"
}

for field, var_name in fields.items():
    label = tk.Label(frame, text=field, font=("Times New Roman", 12), bg='white', fg='navy')
    label.pack(anchor='w')
    entry = tk.Entry(frame, font=("Times New Roman", 12), bg='teal', fg='white')
    entry.pack(fill='x', padx=10, pady=5)
    globals()[var_name] = entry

# Create the process button
process_button = tk.Button(frame, text="Predict", command=process_data, font=("Times New Roman", 12), bg='navy', fg='white')
process_button.pack(pady=10)

# Create the reset button
reset_button = tk.Button(frame, text="Reset", command=reset_application, font=("Times New Roman", 12), bg='navy', fg='white')
reset_button.pack(pady=10)

# Create the output label and place it below the buttons
output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, font=("Times New Roman", 12), bg='white', fg='navy')
output_label.place(relx=0.5, rely=0.85, anchor='n')

# Start the Tkinter event loop
root.mainloop()
