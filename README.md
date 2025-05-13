# 🚀 PathFinderAI

**PathFinderAI** is a Python-based delivery route planner that calculates the shortest driving route between two locations using Google Maps and Dijkstra’s algorithm. It features a modern Tkinter GUI, interactive map visualizations, and delivery tracking.

---

## 📌 Features

- 📍 Address geocoding via Google Maps API  
- 🧭 Shortest path calculation using **Dijkstra’s Algorithm**  
- 🗺️ Route visualization using Folium  
- 🧑‍💻 Intuitive GUI built with Tkinter  
- 📝 Delivery history logging  
- 🧹 Clear history functionality  
- 🏢 Company Info popup (founders, mission, year)

---

## 🏗️ Tech Stack

- **Python 3.10+**
- [Google Maps API](https://developers.google.com/maps/documentation)
- `folium`
- `polyline`
- `tkinter`
- `heapq`, `uuid`, `math`, `os`

---

## 📂 File Structure

> **Note**: The primary script used for the complete project is `navigation_gui.py`. The rest of the files are either legacy code, output files, or documentation.

- NavigationSystem/

- navigation_gui.py # ✅ Main and only required script. Includes GUI, route logic, Dijkstra’s, and logging.
- navigation_system.py # ❌ Legacy/experimental code, not used in final build.
- delivery_log.txt # 📝 Output file that stores delivery history once the app is run.
- route_map.html # 🌐 Auto-generated HTML file that displays the route on a map.
- README.md # 📘 This documentation file.


---

## 💡 How It Works

1. User enters:
   - Pickup location
   - Delivery destination
   - Client name
   - Deliveryman name
2. App geocodes addresses using Google Maps API
3. Google Directions API generates a route graph
4. Dijkstra’s algorithm finds the shortest path
5. Folium displays the route on an interactive map
6. Delivery history is logged for reference

---

## 🧠 Founders & Mission

**PathFinderAI** was founded in **2025** by:

- Daylen Hall  
- Eric Cheeley  
- Ashari Joiner  

**Mission Statement:**  
> *Deliver optimized, fast, and reliable route planning for delivery operations, enhancing both efficiency and user experience.*

---

## 🚀 Getting Started

1. Clone this repo:
   ```bash
   git clone https://github.com/daylenx/PathFinderAI.git
   cd PathFinderAI

Install required packages:

2. Install required package
  pip install googlemaps folium polyline

3. Add your Google Maps API key inside navigation_gui.py

4. Run application
   python navigation_gui.py


