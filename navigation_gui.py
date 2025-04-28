import tkinter as tk
from tkinter import messagebox, ttk
import googlemaps
import folium
import heapq
import uuid
import webbrowser
from collections import defaultdict
import math
import os
import polyline

API_KEY = "AIzaSyDldf_k8iPX5zzpe68luqnpRPRog78RWXE"
gmaps = googlemaps.Client(key=API_KEY)

def geocode_address(address):
    result = gmaps.geocode(address)
    if result:
        loc = result[0]['geometry']['location']
        return (loc['lat'], loc['lng'])
    else:
        raise ValueError("Invalid address")

def haversine(coord1, coord2):
    R = 6371000
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def find_closest_node(coord, graph):
    all_nodes = list(graph.keys()) + [n for neighbors in graph.values() for n, _ in neighbors]
    return min(all_nodes, key=lambda node: haversine(coord, node))

def get_route_data(start, end):
    directions = gmaps.directions(start, end, mode='driving')
    steps = directions[0]['legs'][0]['steps']
    overview_polyline = directions[0]['overview_polyline']['points']
    decoded_path = polyline.decode(overview_polyline)
    total_distance = directions[0]['legs'][0]['distance']['value']
    duration = directions[0]['legs'][0]['duration']['text']
    return decoded_path, total_distance, duration

def show_map(path_coords):
    m = folium.Map(location=path_coords[0], zoom_start=13)
    folium.Marker(path_coords[0], tooltip="Pickup", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(path_coords[-1], tooltip="Delivery", icon=folium.Icon(color='red')).add_to(m)
    folium.PolyLine(path_coords, color="blue", weight=5).add_to(m)
    m.save("route_map.html")
    webbrowser.open("route_map.html")

def load_delivery_log():
    if not os.path.exists("delivery_log.txt"):
        return "No deliveries recorded yet."

    output = ""
    with open("delivery_log.txt", "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) < 6:
                continue
            delivery_id, client, driver, route, distance, duration = parts
            output += (
                f"📦 ID: {delivery_id}\n"
                f"👤 Client: {client.strip()} | 🚚 Driver: {driver.strip()}\n"
                f"🗺️ From: {route.strip()}\n"
                f"📏 Distance: {distance.strip()} | ⏱️ Time: {duration.strip()}\n"
                "──────────────────────────────────────────────\n"
            )
    return output

def clear_history():
    if os.path.exists("delivery_log.txt"):
        os.remove("delivery_log.txt")
    log_text.config(state='normal')
    log_text.delete(1.0, tk.END)
    log_text.insert(tk.END, "No deliveries recorded yet.")
    log_text.config(state='disabled')

def calculate_route():
    pickup = pickup_entry.get()
    delivery = delivery_entry.get()
    client = client_entry.get()
    driver = driver_entry.get()

    try:
        pickup_coords = geocode_address(pickup)
        delivery_coords = geocode_address(delivery)
        path, total_distance, duration = get_route_data(pickup, delivery)

        if path:
            delivery_id = str(uuid.uuid4())[:8]
            total_miles = total_distance * 0.000621371
            result = (
                f"\n✅ Route Found!\n"
                f"📦 ID: {delivery_id}\n"
                f"👤 Client: {client}\n"
                f"🚚 Driver: {driver}\n"
                f"📍 From: {pickup} → {delivery}\n"
                f"📏 Distance: {total_miles:.2f} mi\n"
                f"⏱️ Time: {duration}\n"
            )
            result_text.config(state='normal', fg='lightgreen')
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, result)
            result_text.config(state='disabled')

            with open("delivery_log.txt", "a") as f:
                f.write(f"{delivery_id},{client},{driver},{pickup} -> {delivery},{total_miles:.2f} mi,{duration}\n")

            show_map(path)
            log_text.config(state='normal')
            log_text.delete(1.0, tk.END)
            log_text.insert(tk.END, load_delivery_log())
            log_text.config(state='disabled')
        else:
            result_text.config(state='normal', fg='red')
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "❌ No valid route found.")
            result_text.config(state='disabled')
    except Exception as e:
        result_text.config(state='normal', fg='red')
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"❌ Error: {str(e)}")
        result_text.config(state='disabled')

# GUI setup
root = tk.Tk()
root.title("PathFinderAI - Delivery Route Planner")
root.geometry("640x850")
root.configure(bg='#1e1e1e')

style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", foreground="white", background="#4CAF50", font=("Segoe UI", 10, "bold"))
style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 10))

icon_label = tk.Label(root, text="🚀 PathFinderAI", font=("Helvetica", 16, "bold"), bg="#1e1e1e", fg="white")
icon_label.pack(pady=10)

form_frame = tk.Frame(root, bg="#1e1e1e")
form_frame.pack(pady=10)

labels = ["Pickup Location:", "Delivery Destination:", "Client Name:", "Deliveryman Name:"]
entries = []

for label_text in labels:
    lbl = tk.Label(form_frame, text=label_text, font=("Segoe UI", 10), anchor="w", bg="#1e1e1e", fg="white")
    lbl.pack(fill='x', padx=20, pady=2)
    entry = tk.Entry(form_frame, width=50)
    entry.pack(padx=20, pady=5)
    entries.append(entry)

pickup_entry, delivery_entry, client_entry, driver_entry = entries

ttk.Button(root, text="Calculate Route", command=calculate_route).pack(pady=15)

result_text = tk.Text(root, height=10, width=70, state='disabled', bg='#2e2e2e', fg='lightgreen', relief='solid', borderwidth=1)
result_text.pack(pady=10)

log_title = tk.Label(root, text="📦 Delivery History", font=("Segoe UI", 12, "bold"), bg="#1e1e1e", fg="white")
log_title.pack(pady=(20, 5))

log_frame = tk.Frame(root, bg="#1e1e1e")
log_frame.pack(pady=5)

log_text = tk.Text(log_frame, height=10, width=70, state='disabled', bg='#2e2e2e', fg='white', relief='solid', borderwidth=1)
log_text.pack(side='left')

clear_button = ttk.Button(log_frame, text="🧹 Clear History", command=clear_history)
clear_button.pack(side='left', padx=10)

log_text.config(state='normal')
log_text.insert(tk.END, load_delivery_log())
log_text.config(state='disabled')

root.mainloop()
