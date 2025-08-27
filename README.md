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

# 📂 Project Layout

data/ → contains metro_stations.json, which stores all metro station details like names, lines, coordinates, and fares.

notebooks/ → includes metro_planner.ipynb for running and testing the project inside Jupyter Notebook.

src/ → holds the main Python logic:

route_planner.py for shortest route and fare calculation,

nearest_station.py for finding the nearest metro station,

utils.py for helper functions like loading data and formatting results.


main.py → entry point of the project, which integrates all functions and gives outputs.

requirements.txt → lists all Python dependencies required to run the project.

README.md → documentation of the project.
