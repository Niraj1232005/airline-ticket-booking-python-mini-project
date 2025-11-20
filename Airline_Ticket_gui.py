import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

# Distance map
distances = {
    ("Mumbai", "Delhi"): 1400,
    ("Mumbai", "New York"): 12500,
    ("London", "Paris"): 340,
    ("Mumbai", "London"): 7200,
    ("Delhi", "Paris"): 6700,
    ("New York", "Paris"): 5830,
}

# Flights with layovers
planes = {
    ("Mumbai", "Delhi"): [
        {"name": "Air India AI101", "time": "08:00 AM", "duration": "2.5", "layover": "Non-stop"},
        {"name": "Vistara UK981", "time": "10:30 AM", "duration": "2.5", "layover": "Non-stop"}
    ],
    ("Mumbai", "New York"): [
        {"name": "Emirates EK202", "time": "03:00 AM", "duration": "20", "layover": "via Dubai"}
    ],
    ("London", "Paris"): [
        {"name": "British Airways BA304", "time": "11:00 AM", "duration": "1", "layover": "Non-stop"}
    ],
    ("Mumbai", "London"): [
        {"name": "Air India AI161", "time": "02:00 AM", "duration": "9.5", "layover": "Non-stop"},
        {"name": "British Airways BA142", "time": "07:15 AM", "duration": "9.2", "layover": "Non-stop"},
        {"name": "Air India AI131", "time": "09:30 PM", "duration": "9.5", "layover": "Non-stop"},
    ],
    ("Delhi", "Paris"): [
        {"name": "Air France AF225", "time": "01:30 AM", "duration": "10", "layover": "Non-stop"}
    ],
    ("New York", "Paris"): [
        {"name": "Delta DL118", "time": "05:00 PM", "duration": "7", "layover": "Non-stop"}
    ],
}

fare_per_km = {"Economy": 5, "Business": 8, "First": 12}
GST_RATE = 0.18

root = tk.Tk()
root.title("Airline Ticket Booking System")
root.geometry("700x800")

tk.Label(root, text="✈️ Airline Ticket Booking", font=("Arial", 18, "bold")).pack(pady=10)

cities = ["Mumbai", "Delhi", "New York", "London", "Paris"]
classes = ["Economy", "Business", "First"]
trip_types = ["One-way", "Round-trip"]
seats = [f"A{i}" for i in range(1, 6)] + [f"B{i}" for i in range(1, 6)]

# Variables
from_var = tk.StringVar(value="Select City")
to_var = tk.StringVar(value="Select City")
class_var = tk.StringVar(value="Economy")
trip_var = tk.StringVar(value="One-way")
flight_select = tk.StringVar(value="Select Flight")
seat_var = tk.StringVar(value="A1")

# Passenger Info
tk.Label(root, text="Passenger Name:").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Age:").pack()
age_entry = tk.Entry(root)
age_entry.pack()

# Dropdowns
tk.Label(root, text="From City:").pack()
tk.OptionMenu(root, from_var, *cities).pack()

tk.Label(root, text="To City:").pack()
tk.OptionMenu(root, to_var, *cities).pack()

tk.Label(root, text="Trip Type:").pack()
tk.OptionMenu(root, trip_var, *trip_types).pack()

tk.Label(root, text="Travel Date:").pack()
travel_date = DateEntry(root)
travel_date.pack()

tk.Label(root, text="Return Date (if Round-trip):").pack()
return_date = DateEntry(root)
return_date.pack()

tk.Label(root, text="Class:").pack()
tk.OptionMenu(root, class_var, *classes).pack()

# Dynamic flight selection
def update_flight_list(*args):
    from_city = from_var.get()
    to_city = to_var.get()

    flights = planes.get((from_city, to_city)) or planes.get((to_city, from_city)) or []

    menu = flight_menu["menu"]
    menu.delete(0, "end")
    if not flights:
        menu.add_command(label="No Flights", command=lambda: flight_select.set("No Flights"))
        return

    flight_select.set("Select Flight")
    for flight in flights:
        label = f"{flight['name']} | {flight['time']} | {flight['duration']} hrs | {flight['layover']}"
        menu.add_command(label=label, command=lambda l=label: flight_select.set(l))

from_var.trace("w", update_flight_list)
to_var.trace("w", update_flight_list)

tk.Label(root, text="Select Flight:").pack()
flight_menu = tk.OptionMenu(root, flight_select, "")
flight_menu.pack()

tk.Label(root, text="Select Seat:").pack()
tk.OptionMenu(root, seat_var, *seats).pack()

# Generate ticket
def generate_ticket():
    name = name_entry.get()
    age = age_entry.get()
    from_city = from_var.get()
    to_city = to_var.get()
    travel = travel_date.get()
    ret = return_date.get() if trip_var.get() == "Round-trip" else "N/A"
    trip = trip_var.get()
    cls = class_var.get()
    flight = flight_select.get()
    seat = seat_var.get()

    if not name or not age or not flight or "No Flights" in flight:
        messagebox.showerror("Error", "Missing or invalid flight/passenger info.")
        return

    try:
        age_int = int(age)
    except:
        messagebox.showerror("Error", "Invalid Age")
        return

    dist = distances.get((from_city, to_city)) or distances.get((to_city, from_city))
    if not dist:
        messagebox.showerror("Error", "Distance not available.")
        return

    base_fare = fare_per_km[cls] * dist * (2 if trip == "Round-trip" else 1)
    gst = base_fare * GST_RATE
    total = base_fare + gst

    # Ticket in new window
    win = tk.Toplevel(root)
    win.title("Flight Ticket")
    win.geometry("500x550")
    tk.Label(win, text="✈️ Flight Ticket", font=("Arial", 16, "bold")).pack(pady=10)

    summary = f"""
Passenger Name: {name}
Age: {age}
From: {from_city}
To: {to_city}
Trip: {trip}
Departure: {travel}
Return: {ret}
Class: {cls}
Seat: {seat}
Flight: {flight}
Distance: {dist} km
Fare: ₹{base_fare:.2f}
GST (18%): ₹{gst:.2f}
Total Fare: ₹{total:.2f}
-------------------------
Have a safe flight! 🛫
"""

    text = tk.Text(win, height=25, width=60)
    text.pack()
    text.insert(tk.END, summary)
    text.config(state='disabled')

# Button
tk.Button(root, text="Generate Ticket", bg="blue", fg="white", command=generate_ticket).pack(pady=20)

root.mainloop()
