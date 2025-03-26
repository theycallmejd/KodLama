import tkinter as tk
from tkinterweb import HtmlFrame
import folium
import googlemaps

def plan_trip():
    current_location = current_location_entry.get()
    destination = destination_entry.get()
    budget = budget_entry.get()
    days = days_entry.get()

    if not current_location or not destination or not budget or not days:
        label.config(text="Please fill in all fields.")
        return

    try:
        budget = float(budget)
        days = int(days)
    except ValueError:
        label.config(text="Please enter a valid budget and number of days.")
        return

    # Here you can add logic to fetch transport options, pricing, and timing
    # You can also integrate AI-based trip planning and food recommendations
    label.config(text=f"Planning trip from {current_location} to {destination} for {days} days with a budget of {budget}")

    # Create a map centered at the destination
    map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    folium.Marker([20.5937, 78.9629], popup="Destination").add_to(map)
    map.save("map.html")
    frame.load_file("map.html")

# Create the main window
root = tk.Tk()
root.title("Tourism, Transportation, and Logistics App")

# Create input fields for current location, destination, budget, and days
tk.Label(root, text="Current Location:").pack(pady=5)
current_location_entry = tk.Entry(root)
current_location_entry.pack(pady=5)

tk.Label(root, text="Destination:").pack(pady=5)
destination_entry = tk.Entry(root)
destination_entry.pack(pady=5)

tk.Label(root, text="Budget:").pack(pady=5)
budget_entry = tk.Entry(root)
budget_entry.pack(pady=5)

tk.Label(root, text="Number of Days:").pack(pady=5)
days_entry = tk.Entry(root)
days_entry.pack(pady=5)

# Create a button to plan the trip
plan_button = tk.Button(root, text="Plan Trip", command=plan_trip)
plan_button.pack(pady=10)

# Create a label to display the trip plan
label = tk.Label(root, text="")
label.pack(pady=10)

# Create an HtmlFrame to display the map
frame = HtmlFrame(root)
frame.pack(fill="both", expand=True)

# Run the application
root.mainloop()
