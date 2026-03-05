#Student ID  : 012398812
#Student Name: Travon Bazil
#Class   Name: DATA STRUCTURES AND ALGORITHMS II
#Title       : WGUPS ROUTING PROGRAM IMPLEMENTATION

import csv
import datetime
from HashTable import HashMap
from Trucks_Packages import Truck, Package


# Creation of hashtable
hash_table = HashMap()

# Read file with addresses and distances
with open("Data_Files/Distances and Addresses.csv") as file1:
    distance_rows = list(csv.reader(file1))

# Read file with package information
with open("Data_Files/Package Information.csv") as file2:
    package_rows = list(csv.reader(file2))

# Making sure that extra spaces are taken into account
address_to_index = {}
for col in range(1, len(distance_rows[0])):
    address_name = distance_rows[0][col].strip()
    if address_name != "":
        address_to_index[address_name] = col

# Method to convert an address string into its index in the distance table
def extract_address(address):
    return address_to_index.get(address.strip())

# Method to return the distance between two address indexes
def distance_in_between(x_value, y_value):
    distance = distance_rows[x_value][y_value]
    if distance == "":
        distance = distance_rows[y_value][x_value]
    return float(distance)

# Creation of function to load packages into hash table
def load_packages(filename, table):
    with open(filename) as package_info:
        rows = csv.reader(package_info)

        # Skipping header rows
        next(rows)
        next(rows)

        # Inserting package objects into the hash table (key = package id)
        for row in rows:
            package_id = int(row[0])
            delivery_address = row[1].strip()
            delivery_city = row[2].strip()
            delivery_state = row[3].strip()
            delivery_zipcode = row[4].strip()
            delivery_deadline = row[5].strip()
            package_weight = row[6].strip()

            # All packages start at the hub
            delivery_status = "At Hub"

            # Defining package object
            package_object = Package(
                delivery_status,
                package_id,
                delivery_deadline,
                delivery_address,
                delivery_city,
                delivery_state,
                delivery_zipcode,
                package_weight
            )
            # Insertion of data into hash table
            table.insert(package_id, package_object)

# Load packages into hash table
load_packages("Data_Files/Package Information.csv", hash_table)


# Constraint for package 9 (address correction after 10:20 am)
address_correction_time = datetime.timedelta(hours=10, minutes=20)
# Change these values if your dataset uses a different corrected address for package 9
p9_correct_address = ("410 S State St", "Salt Lake City", "UT", "84111")

# Creation of package 9 correction function
def set_package9_state(check_time):
    p9 = hash_table.lookup(9)
    if p9 is None:
        return

    if check_time >= address_correction_time:
        p9.delivery_address, p9.delivery_city, p9.delivery_state, p9.delivery_zipcode = p9_correct_address
        p9.notes = "address corrected at 10:20 am"
    else:
        # Revert to original (wrong) address before 10:20
        p9.delivery_address = p9.orig_address
        p9.delivery_city = p9.orig_city
        p9.delivery_state = p9.orig_state
        p9.delivery_zipcode = p9.orig_zip
        p9.notes = "wrong address until 10:20 am"

# Delayed packages (must show non-default status before 9:05)
delayed_until_time = datetime.timedelta(hours=9, minutes=5)
delayed_packages = {6, 25, 28, 32}

# Apply delayed notes/times to those packages
for package_id in delayed_packages:
    package_object = hash_table.lookup(package_id)
    if package_object is not None:
        package_object.available_time = delayed_until_time
        package_object.notes = "delayed until 9:05 am"

# Update delivery status of package
def update_status(package_object, check_time):
    if package_object.available_time and check_time < package_object.available_time:
        package_object.delivery_status = "Delayed (arrives 9:05 AM)"
        return
    if package_object.delivery_time and package_object.delivery_time <= check_time:
        package_object.delivery_status = "Delivered"
    elif package_object.departure_time and package_object.departure_time <= check_time:
        package_object.delivery_status = "En route"
    else:
        package_object.delivery_status = "At Hub"


# Print output that includes delivery time
def package_display(package_object):
    truck_text = package_object.truck_number if package_object.truck_number else "N/A"

    # Only show delivery time if actually delivered by the check time
    delivery_time_text = package_object.delivery_time if package_object.delivery_status == "Delivered" else "N/A"

    return (
        f"package id: {package_object.package_id} | "
        f"delivery address: {package_object.delivery_address} | "
        f"delivery status: {package_object.delivery_status} | "
        f"delivery deadline: {package_object.delivery_deadline} | "
        f"truck number: {truck_text} | "
        f"delivery time: {delivery_time_text}"
    )

hub_location = "HUB"

# Creation of truck 1 and manual loading
truck1 = Truck(
    [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40],
    hub_location,
    datetime.timedelta(hours=8),
    datetime.timedelta(hours=8),
    0.0,
    18,
    16
)

# Creation of truck 2 and manual loading
truck2 = Truck(
    [3, 9, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39],
    hub_location,
    datetime.timedelta(hours=10, minutes=20),
    datetime.timedelta(hours=10, minutes=20),
    0.0,
    18,
    16
)

# Creation of truck 3 and manual loading
truck3 = Truck(
    [2, 4, 5, 6, 7, 8, 10, 11, 25, 28, 32, 33],
    hub_location,
    datetime.timedelta(hours=9, minutes=5),
    datetime.timedelta(hours=9, minutes=5),
    0.0,
    18,
    16
)

# Assigning truck numbers
truck1.truck_number = 1
truck2.truck_number = 2
truck3.truck_number = 3


# Method used for packages and implementation of nearest neighbor algorithm
def delivery_route(truck):
    # Apply package 9 state for the truck's current time (package 9 is on truck 2)
    set_package9_state(truck.current_time)

    # Copy original package ids so we do not mutate the list while iterating
    original_ids = list(truck.package_id)

    # Creating a list of package objects to deliver
    pending_packages = []
    for package_id in original_ids:
        package_object = hash_table.lookup(package_id)
        if package_object is not None:
            package_object.truck_number = truck.truck_number
            package_object.departure_time = truck.departure_time
            pending_packages.append(package_object)


    truck.package_id = []

    # Nearest neighbor loop
    while len(pending_packages) > 0:
        closest_distance = 2000
        closest_package = None

        start_index = extract_address(truck.current_address)
        if start_index is None:
            raise ValueError(f"current address not found in distance table header: {truck.current_address}")

        for package_object in pending_packages:
            end_index = extract_address(package_object.delivery_address)
            if end_index is None:
                raise ValueError(f"package address not found in distance table header: {package_object.delivery_address}")

            distance = distance_in_between(start_index, end_index)

            if distance <= closest_distance:
                closest_distance = distance
                closest_package = package_object

        # Record the delivery order
        truck.package_id.append(closest_package.package_id)
        pending_packages.remove(closest_package)

        # Update truck stats
        truck.total_miles += closest_distance
        truck.current_address = closest_package.delivery_address

        # Update truck stats
        truck.current_time += datetime.timedelta(hours=closest_distance / truck.speed_mph)

        # Stamp package times
        closest_package.delivery_time = truck.current_time


# Routes for trucks
delivery_route(truck1)
delivery_route(truck2)

# Setting conditions for truck 3 to run its route
truck3.departure_time = max(min(truck1.current_time, truck2.current_time), delayed_until_time)
truck3.current_time = truck3.departure_time
delivery_route(truck3)


print("                                 **********************")
print("                                 *      WGUPS         *")
print("                                 **********************")

# Showing packages in trucks
print("***************************************************************************************************")
print("truck 1 packages (delivery order):", truck1.package_id)
print("truck 2 packages (delivery order):", truck2.package_id)
print("truck 3 packages (delivery order):", truck3.package_id)
print("****************************************************************************************************")


starter = input(
    "Hello User, You are currently logged into the routing system \n"
    "Please enter START to begin: "
).strip()

if starter != "START":
    print("Entry invalid. Closing program.")
    exit()

# user input for time
try:
    inputted_time = input("Enter a time (hh:mm:ss) to check package status: ").strip()
    h, m, s = inputted_time.split(":")
    check_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
except ValueError:
    print("Entry invalid. Closing program.")
    exit()

set_package9_state(check_time)

view_choice = input("Type 'ONE' for a single package or 'ALL' for all packages: ").strip()

# single package output
if view_choice == "ONE":
    try:
        ONE_input = int(input("Enter the package id: ").strip())
    except ValueError:
        print("Entry invalid. Closing program.")
        exit()

    package_object = hash_table.lookup(ONE_input)
    update_status(package_object, check_time)
    print(package_display(package_object))

# Choice for viewing all packages
elif view_choice == "ALL":
    for package_id in range(1, 41):
        package_object = hash_table.lookup(package_id)
        update_status(package_object, check_time)
        print(package_display(package_object))

else:
    print("Entry invalid. Closing program.")
    exit()

# Prints out the total mileage for all trucks
total_mileage = truck1.total_miles + truck2.total_miles + truck3.total_miles
print("total mileage traveled by all trucks:", round(total_mileage, 2))