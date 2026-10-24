from database import routes, bookings


def generate_booking_report():
    print("\n===== BOOKING REPORT =====")

    total_bookings = len(bookings)
    confirmed_bookings = 0
    cancelled_bookings = 0
    reserved_seats = 0
    confirmed_revenue = 0
    fully_booked_routes = 0

    for booking in bookings:

        if booking["status"] == "Confirmed":
            confirmed_bookings += 1
            reserved_seats += booking["seats"]
            confirmed_revenue += booking["total_fare"]

        elif booking["status"] == "Cancelled":
            cancelled_bookings += 1

    for route in routes:
        if route["available_seats"] == 0:
            fully_booked_routes += 1

    print(f"Total Bookings      : {total_bookings}")
    print(f"Confirmed Bookings  : {confirmed_bookings}")
    print(f"Cancelled Bookings  : {cancelled_bookings}")
    print(f"Seats Reserved      : {reserved_seats}")
    print(f"Confirmed Revenue   : Rs. {confirmed_revenue}")
    print(f"Fully Booked Routes : {fully_booked_routes}")

    print("\n===== ROUTE-WISE SUMMARY =====")

    for route in routes:

        route_bookings = 0
        route_seats = 0
        route_revenue = 0

        for booking in bookings:

            if (
                booking["route_id"] == route["route_id"]
                and booking["status"] == "Confirmed"
            ):
                route_bookings += 1
                route_seats += booking["seats"]
                route_revenue += booking["total_fare"]

        print(
            f"{route['route_id']} | "
            f"Bookings: {route_bookings} | "
            f"Seats: {route_seats} | "
            f"Revenue: Rs. {route_revenue}"
        )