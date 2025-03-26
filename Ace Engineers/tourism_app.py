import tkinter as tk
from tkinterweb import HtmlFrame
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="travel_planner_app")

def get_coordinates(location):
    location = geolocator.geocode(location)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def find_people_nearby(current_lat, current_lng, radius=50):
    # Dummy data for people nearby (latitude, longitude, name)
    people = [
        (current_lat + 0.1, current_lng + 0.1, "Alice"),
        (current_lat - 0.1, current_lng - 0.1, "Bob"),
        (current_lat + 0.05, current_lng - 0.05, "Charlie"),
    ]
    nearby_people = []
    for person in people:
        person_location = (person[0], person[1])
        distance = geodesic((current_lat, current_lng), person_location).km
        if distance <= radius:
            nearby_people.append(person)
    return nearby_people

def plan_trip():
    current_location = current_location_entry.get()
    destination = destination_entry.get()
    transport_mode = transport_mode_var.get()
    payment_method = payment_method_var.get()

    if not current_location or not destination or not transport_mode or not payment_method:
        label.config(text="Please fill in all fields.")
        return

    # Get coordinates for current location and destination
    current_lat, current_lng = get_coordinates(current_location)
    dest_lat, dest_lng = get_coordinates(destination)

    if current_lat is None or dest_lat is None:
        label.config(text="Could not find the specified locations.")
        return

    # Find people nearby
    nearby_people = find_people_nearby(current_lat, current_lng)
    people_text = "\n".join([f"{person[2]} ({person[0]}, {person[1]})" for person in nearby_people])

    # Display trip plan and nearby people
    label.config(text=f"Planning trip from {current_location} to {destination} by {transport_mode} with {payment_method} payment method.\n\nPeople nearby:\n{people_text}")

    # Create a map centered at the destination
    map = folium.Map(location=[dest_lat, dest_lng], zoom_start=10)
    folium.Marker([dest_lat, dest_lng], popup="Destination").add_to(map)
    for person in nearby_people:
        folium.Marker([person[0], person[1]], popup=person[2]).add_to(map)
    map.save("map.html")
    frame.load_file("map.html")

    # Ask if the user wants to join the nearby people
    join_trip = tk.messagebox.askyesno("Join Trip", "Do you want to join the nearby people?")
    if join_trip:
        joined_people = ", ".join([person[2] for person in nearby_people])
        label.config(text=f"Trip planned successfully! You will be joined by: {joined_people}")

# Create the main window
root = tk.Tk()
root.title("Group Trip Planner App")

# Create input fields for current location, destination, transport mode, and payment method
tk.Label(root, text="Current Location:").pack(pady=5)
current_location_entry = tk.Entry(root)
current_location_entry.pack(pady=5)

tk.Label(root, text="Destination:").pack(pady=5)
destination_entry = tk.Entry(root)
destination_entry.pack(pady=5)

tk.Label(root, text="Mode of Transport:").pack(pady=5)
transport_mode_var = tk.StringVar(value="By Road")
tk.Radiobutton(root, text="By Road", variable=transport_mode_var, value="By Road").pack(pady=2)
tk.Radiobutton(root, text="By Railway", variable=transport_mode_var, value="By Railway").pack(pady=2)
tk.Radiobutton(root, text="By Flight", variable=transport_mode_var, value="By Flight").pack(pady=2)

tk.Label(root, text="Preferred Payment Method:").pack(pady=5)
payment_method_var = tk.StringVar(value="Credit Card")
tk.Radiobutton(root, text="Credit Card", variable=payment_method_var, value="Credit Card").pack(pady=2)
tk.Radiobutton(root, text="Debit Card", variable=payment_method_var, value="Debit Card").pack(pady=2)
tk.Radiobutton(root, text="Cash", variable=payment_method_var, value="Cash").pack(pady=2)

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