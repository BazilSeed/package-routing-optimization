# Package Routing Optimization System

A Python simulation of a real-world package delivery routing problem for the Western Governors University Parcel Service (WGUPS). The program determines an efficient delivery route for 40 packages across Salt Lake City using a custom **Nearest Neighbor/Greedy algorithm** and a **self-built hash table**, ensuring all packages are delivered on time with a combined truck mileage under 140 miles.


## Tech Stack

- **Language**: Python
- **Data Structures**: Custom hash table with chaining (built from scratch, no external libraries)
- **Interface**: Command-line (CLI)


## The Problem

Three trucks, two drivers, and 40 packages with unique delivery constraints including:
- Deadlines ranging from 9:00 AM to end of day
- Package grouping requirements (certain packages must ride together)
- A delayed address correction at 10:20 AM for Package #9
- Truck capacity limit of 16 packages per truck
- Truck 3 does not deploy until Trucks 1 and 2 complete their routes

The goal was to deliver all packages on time while keeping total combined mileage under 140 miles.


## Algorithm — Nearest Neighbor / Greedy

For each truck, the program repeatedly selects the closest undelivered address from the truck's current location until the package list is empty. This approach was chosen because:

- It is simple to implement and easy to verify for correctness
- It quickly produces low-mileage routes without long computation time
- It supports time-sensitive delivery scheduling better than exhaustive search algorithms

### Alternatives Considered
- **Dijkstra's Algorithm** — finds globally shortest paths using accumulated cost, but is more complex and slower for this use case
- **A* Search** — similar to Dijkstra but uses a heuristic to guide the search more efficiently; better for larger-scale problems but unnecessary given the 40-package constraint


## Data Structure — Hash Table with Chaining

A custom hash table was built from scratch to store and retrieve package data. Each package ID is the key, and the value is a package object containing address, deadline, city, zip code, weight, status, and delivery timestamp.

- **Average lookup/insert**: O(1)
- **Worst case**: O(n) due to chaining
- Supports direct access without scanning the full list

### Alternatives Considered
- **Python List** — O(1) with direct addressing, suitable for small fixed datasets like 40 packages, but less scalable
- **Binary Search Tree** — maintains sorted order with O(log n) lookup, but adds unnecessary complexity for this problem size


## Features

- **Greedy routing** — loads and routes trucks based on distance, deadlines, and package constraints
- **Real-time status tracking** — query any package at any point in the delivery day (At Hub / En Route / Delivered)
- **Truck monitoring** — view truck locations and mileage at any time during the day
- **Special case handling** — automatically updates Package #9's corrected address at 10:20 AM
- **Delivery timestamps** — logs exact delivery time for every package
- **Total mileage display** — calculates and displays combined mileage at end of execution


## Results

- ✅ All 40 packages delivered on time
- ✅ Total combined mileage under 140 miles
- ✅ All special delivery constraints met (deadlines, grouping, address correction)
- ✅ Truck scheduling constraints satisfied


## Future Improvements

- Standardized address formatting to handle variations like "S" vs "South"
- GUI with visual delivery tracking showing package statuses and truck availability in real time
