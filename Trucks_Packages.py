# creating class to hold trucks and packages

# creation of truck class
class Truck:
    def __init__(self, package_id, current_address, current_time, departure_time, total_miles, speed_mph, max_capacity):
        self.package_id = package_id
        self.current_address = current_address
        self.current_time = current_time
        self.departure_time = departure_time
        self.total_miles = total_miles
        self.speed_mph = speed_mph
        self.max_capacity = max_capacity

        # added for rubric validation (truck number required in output)
        self.truck_number = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (
            self.package_id,
            self.current_address,
            self.current_time,
            self.departure_time,
            self.total_miles,
            self.speed_mph,
            self.max_capacity
        )


# creation of package class
class Package:
    def __init__(self, delivery_status, package_id, delivery_deadline, delivery_address, delivery_city, delivery_state, delivery_zip_code, package_weight):
        self.delivery_status = delivery_status
        self.package_id = package_id
        self.delivery_deadline = delivery_deadline
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_state = delivery_state

        # keep naming consistent: use delivery_zipcode everywhere
        self.delivery_zipcode = delivery_zip_code

        self.package_weight = package_weight

        # creation of delivery time fields
        self.delivery_time = None
        self.departure_time = None

        # added fields for rubric validation + package constraints
        self.truck_number = None
        self.notes = ""
        self.available_time = None

        # saving original address info for package 9 (so it can be wrong before 10:20)
        self.orig_address = delivery_address
        self.orig_city = delivery_city
        self.orig_state = delivery_state
        self.orig_zip = delivery_zip_code

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (
            self.delivery_status,
            self.package_id,
            self.delivery_deadline,
            self.delivery_address,
            self.delivery_city,
            self.delivery_state,
            self.delivery_zipcode,
            self.package_weight
        )