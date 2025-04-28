import googlemaps
import folium
from collections import defaultdict
import heapq
import math
import uuid
import webbrowser


API_KEY = "AIzaSyDldf_k8iPX5zzpe68luqnpRPRog78RWXE"
gmaps = googlemaps.Client(key=API_KEY)

def geocode_address(address):
    try:
        result = gmaps.geocode(address)
        if result:
            loc = result[0]['geometry']['location']
            return (loc['lat'], loc['lng'])
        else:
            raise ValueError("Invalid address")
    except Exception as e:
        raise Exception(f"Geocoding failed: {e}")

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
    try:
        directions = gmaps.directions(start, end, mode='driving')
        if not directions:
            raise Exception("No directions found")
        steps = directions[0]['legs'][0]['steps']
        graph = defaultdict(list)
        coords = []
        for step in steps:
            start_loc = (step['start_location']['lat'], step['start_location']['lng'])
            end_loc = (step['end_location']['lat'], step['end_location']['lng'])
            distance = step['distance']['value']
            graph[start_loc].append((end_loc, distance))
            coords.append((start_loc, end_loc))
        total_distance = directions[0]['legs'][0]['distance']['value']
        duration = directions[0]['legs'][0]['duration']['text']
        return graph, coords, total_distance, duration
    except Exception as e:
        raise Exception(f"Failed to get route data: {e}")

def dijkstra(graph, start, end):
    heap = [(0, start)]
    dist = {start: 0}
    prev = {}
    while heap:
        current_dist, current_node = heapq.heappop(heap)
        if current_node == end:
            break
        for neighbor, weight in graph[current_node]:
            alt = current_dist + weight
            if neighbor not in dist or alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = current_node
                heapq.heappush(heap, (alt, neighbor))
    path, node = [], end
    while node in prev:
        path.insert(0, node)
        node = prev[node]
    if path:
        path.insert(0, start)
    return path, dist.get(end, float('inf'))

def show_map(path_coords):
    m = folium.Map(location=path_coords[0], zoom_start=13)
    folium.Marker(path_coords[0], tooltip="Pickup", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(path_coords[-1], tooltip="Delivery", icon=folium.Icon(color='red')).add_to(m)
    folium.PolyLine(path_coords, color="blue", weight=5).add_to(m)
    m.save("route_map.html")
    webbrowser.open("route_map.html")

def company_info():
    print("\n-- Company Info --")
    print("PathFinderAI: Deliver smarter, not harder.")
    print("Founded: 2025")
    print("Team: Daylen Hall")

def delivery_input():
    pickup = input("Pickup location: ")
    delivery = input("Delivery destination: ")
    client = input("Client name: ")
    driver = input("Deliveryman name: ")
    try:
        pickup_coords = geocode_address(pickup)
        delivery_coords = geocode_address(delivery)
        graph, segments, total_distance, duration = get_route_data(pickup, delivery)

        start_node = find_closest_node(pickup_coords, graph)
        end_node = find_closest_node(delivery_coords, graph)

        path, _ = dijkstra(graph, start_node, end_node)
        if path:
            delivery_id = str(uuid.uuid4())[:8]
            total_miles = total_distance * 0.000621371
            print("\n--- Delivery Record ---")
            print(f"Delivery ID: #{delivery_id}")
            print(f"Client: {client}")
            print(f"Driver: {driver}")
            print(f"Total Distance: {total_miles:.2f} mi")
            print(f"Estimated Travel Time: {duration}")
            show_map(path)
            with open("delivery_log.txt", "a") as f:
                f.write(f"{delivery_id}, {client}, {driver}, {pickup} -> {delivery}, {total_miles:.2f} mi, {duration}\n")
            print("Route map saved as route_map.html ✅")
        else:
            print("No valid route found.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        print("\n--- Main Menu ---")
        print("1. Company Info")
        print("2. Enter Delivery Details")
        print("3. Exit")
        choice = input("Select an option (1-3): ")
        if choice == '1':
            company_info()
        elif choice == '2':
            delivery_input()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
