# 🚇 Mumbai Metro Navigator

This project is a simple yet practical **route planner for Mumbai Metro**.  
It helps commuters quickly find the **nearest station**, get the **shortest route** to their destination, and know the **estimated fare** before starting their journey.  

# 🤖 What it does
- Finds the nearest metro station from your current location  
- Suggests the shortest route between two stations  
- Gives step-by-step travel instructions (which line to take, where to switch, etc.)  
- Estimates the total fare in INR  
- Can be run as a **Python script** or explored in a **Jupyter Notebook**  


# 📒 Tech Stack
- **Python 3**  
- **Jupyter Notebook**  
- **Geopy** → to work with user location  
- **NetworkX** → to calculate shortest path between stations  
- **JSON** → to store metro station data  

---

# 🧩 Project Layout

mumbai-metro-planner/
│── data/
│   └── metro_stations.json     # Station names, lines, coordinates, fares
│
│── notebooks/
│   └── metro_planner.ipynb     # Jupyter Notebook for exploration & demo
│
│── src/
│   ├── route_planner.py        # Core logic: shortest path, fare calculation
│   ├── nearest_station.py      # Finds nearest station from user location
│   └── utils.py                # Helper functions
│
│── main.py                     # Script to run the project
│── requirements.txt            # Python dependencies
│── README.md                   # Project documentation
