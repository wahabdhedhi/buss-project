from database import routes, cities


def view_routes():
    print("\n===== AVAILABLE BUS ROUTES =====")

    for number, route in enumerate(routes, start=1):

        if route["available_seats"] == 0:
            continue

        print(
            f"{number}. {route['route_id']} | "
            f"{route['departure_city']} -> {route['destination_city']} | "
            f"{route['departure_time']} | "
            f"Rs. {route['ticket_price']} | "
            f"Seats: {route['available_seats']}/{route['total_seats']}"
        )


def search_route():
    search = input("Enter Route ID or City: ").strip().lower()

    # Search by Route ID
    for route in routes:
        if search == route["route_id"].lower():
            print(
                f"{route['route_id']} | "
                f"{route['departure_city']} -> {route['destination_city']} | "
                f"{route['departure_time']} | "
                f"Rs. {route['ticket_price']} | "
                f"{route['available_seats']} seats available"
            )
            break

    else:
        # Search by City
        found = False

        for route in routes:
            if (
                search == route["departure_city"].lower()
                or search == route["destination_city"].lower()
            ):
                print(
                    f"{route['route_id']} | "
                    f"{route['departure_city']} -> {route['destination_city']} | "
                    f"{route['departure_time']} | "
                    f"Rs. {route['ticket_price']} | "
                    f"{route['available_seats']} seats available"
                )
                found = True

        if not found:
            print("No matching route found.")


def view_seat_availability():
    print("\n===== SEAT AVAILABILITY =====")

    for route in routes:

        if route["available_seats"] == 0:
            status = "Fully Booked"

        elif route["available_seats"] == route["total_seats"]:
            status = "Available"

        else:
            status = "Partially Booked"

        print(
            f"{route['route_id']} | "
            f"{route['departure_city']} -> {route['destination_city']} | "
            f"Seats: {route['available_seats']}/{route['total_seats']} | "
            f"Status: {status}"
        )


def view_route_schedule():
    print("\n===== ROUTE SCHEDULE =====")

    for city in cities:
        print(f"\nDepartures from {city}:")

        found = False

        for route in routes:
            if route["departure_city"] == city:
                print(
                    f"{route['route_id']} | "
                    f"{route['destination_city']} | "
                    f"{route['departure_time']}"
                )
                found = True

        if not found:
            print("No scheduled departures.")