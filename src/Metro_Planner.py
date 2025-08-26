# src/metro_planner.py
import os, json, math, heapq
from collections import defaultdict

# -----------------------
# Utilities
# -----------------------
def haversine_km(a, b):
    lat1, lon1 = a; lat2, lon2 = b
    R = 6371.0
    phi1 = math.radians(lat1); phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1); dlambda = math.radians(lon2 - lon1)
    x = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.asin(math.sqrt(x))

def dijkstra(graph, source, target):
    pq = [(0, source)]
    dist = {source: 0}
    prev = {}
    while pq:
        d,u = heapq.heappop(pq)
        if u == target:
            break
        if d > dist.get(u, 1e18): continue
        for v,w in graph.get(u,[]):
            nd = d + w
            if nd < dist.get(v, 1e18):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    if target not in dist:
        return None, None
    path = []
    cur = target
    while cur != source:
        path.append(cur)
        cur = prev[cur]
    path.append(source); path.reverse()
    return path, dist[target]

def fare_from_distance_km(km):
    slabs = [(3,10),(12,20),(18,30),(24,40),(30,50),(36,60),(42,70)]
    for limit,fare in slabs:
        if km <= limit: return fare
    return 80

# -----------------------
# Load stations file
# Accepts two JSON shapes:
# 1) mapping: { "Versova": {"lat":..,"lon":..,"lines":[...]}, ... }
# 2) simple list under "stations": [{"name":..., "lat":..., "lon":..., "lines":[...]}, ...]
# -----------------------
def load_stations(json_path):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"stations.json not found at {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    stations = {}
    # case 1: top-level mapping
    if isinstance(raw, dict) and all(isinstance(v, dict) for v in raw.values()):
        for name, info in raw.items():
            if "lat" in info and "lon" in info:
                stations[name] = {"coords": (float(info["lat"]), float(info["lon"])),
                                  "lines": set(info.get("lines", []))}
    # case 2: {"stations": [ {name, lat, lon, lines} ]}
    elif isinstance(raw, dict) and "stations" in raw and isinstance(raw["stations"], list):
        for entry in raw["stations"]:
            name = entry.get("name") or entry.get("station")
            if name and "lat" in entry and "lon" in entry:
                stations[name] = {"coords": (float(entry["lat"]), float(entry["lon"])),
                                  "lines": set(entry.get("lines", []))}
    else:
        raise ValueError("stations.json format not recognized. Use mapping or {'stations': [...] }")
    return stations

# -----------------------
# Build graph from an ordered LINES dict (you must edit LINES to include correct station order)
# -----------------------
def build_graph(lines_ordered, stations):
    graph = defaultdict(list)
    for line_name, seq in lines_ordered.items():
        filtered = [s for s in seq if s in stations]
        for i in range(len(filtered)-1):
            a,b = filtered[i], filtered[i+1]
            d = haversine_km(stations[a]["coords"], stations[b]["coords"])
            graph[a].append((b,d))
            graph[b].append((a,d))
    return graph

def find_nearest_station(point, stations):
    best=None; bestd=1e18
    for name, info in stations.items():
        d = haversine_km(point, info["coords"])
        if d < bestd:
            best, bestd = name, d
    return best, bestd

def deduce_segments(path, stations):
    if not path: return []
    segments=[]
    current_line=None
    seg_stations=[path[0]]
    for i in range(len(path)-1):
        s,t = path[i], path[i+1]
        common = stations[s]["lines"].intersection(stations[t]["lines"])
        chosen = next(iter(common)) if common else "Unknown"
        if chosen != current_line:
            if current_line is not None:
                segments.append((current_line, seg_stations))
            current_line = chosen
            seg_stations = [s,t]
        else:
            seg_stations.append(t)
    segments.append((current_line, seg_stations))
    return segments
