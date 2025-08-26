# main.py (project root)
import os, json
from src.metro_planner import (
    load_stations, build_graph, find_nearest_station,
    dijkstra, deduce_segments, fare_from_distance_km, haversine_km
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "stations.json")
OUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

# --- Edit LINES if you expand stations.json ---
LINES = {
    "Line 1 (Blue)": ["Versova","Azad Nagar","D N Nagar","Andheri","Chakala (Airport Road)","Marol Naka","Saki Naka","Asalpha","Jagruti Nagar","Ghatkopar"],
    "Line 2A (Yellow)": ["Dahisar East","Borivali","Malad","Andheri West","D N Nagar"]
}

def interactive():
    stations = load_stations(DATA_PATH)
    graph = build_graph(LINES, stations)

    # get user location (manual)
    print("Enter your current location as 'lat,lon' (example: 19.1509,72.8236)")
    loc = input("Your location (lat,lon): ").strip()
    if "," in loc:
        try:
            user_loc = tuple(map(float, loc.split(",")))
        except:
            print("Invalid coords. Exiting."); return
    else:
        print("Please enter lat,lon format. Exiting."); return

    origin, orig_d = find_nearest_station(user_loc, stations)
    print(f"Nearest origin station: {origin} ({orig_d*1000:.0f} m)")

    dest_input = input("Enter destination station name (exact name): ").strip()
    if dest_input in stations:
        dest = dest_input
    else:
        print("Destination not found in stations.json. Exiting."); return

    if origin not in graph or dest not in graph:
        print("Origin or destination not connected in graph (check LINES order & stations.json). Exiting.")
        return

    path, total_km = dijkstra(graph, origin, dest)
    if not path:
        print("No path found (graph incomplete).")
        return

    time_min = total_km / 30.0 * 60.0
    fare = fare_from_distance_km(total_km)

    print("\n=== ROUTE ===")
    print(" -> ".join(path))
    print(f"Distance: {total_km:.2f} km   Time approx: {time_min:.0f} min   Fare: ₹{fare}\n")
    segments = deduce_segments(path, stations)
    print("Step-by-step:")
    for ln, seq in segments:
        segdist = sum(haversine_km(stations[seq[i]]["coords"], stations[seq[i+1]]["coords"]) for i in range(len(seq)-1))
        print(f" - Take {ln} from {seq[0]} to {seq[-1]} ({len(seq)-1} stops, ~{segdist:.2f} km)")

    # save result
    out = {"origin": origin, "destination": dest, "path": path, "distance_km": total_km, "time_min": time_min, "fare_inr": fare}
    out_file = os.path.join(OUT_DIR, "last_route.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print("Saved last route to", out_file)

if __name__ == "__main__":
    interactive()
