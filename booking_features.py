from database import routes, bookings, booking_ids


def book_ticket():
    print("\n===== BOOK A TICKET =====")

    # Passenger Name
    name = input("Enter passenger name: ").strip()

    if name == "":
        print("Passenger name cannot be empty!")
        return

    # Passenger Age
    age_input = input("Enter passenger age: ")

    if not age_input.isdigit():
        print("Age must be a valid number!")
        return

    age = int(age_input)

    if age <= 0:
        print("Age must be greater than 0!")
        return

    # Route ID
    route_id = input("Enter Route ID: ").strip().upper()

    selected_route = None

    for route in routes:
        if route["route_id"] == route_id:
            selected_route = route
            break

    if selected_route is None:
        print("Route not found!")
        return

    # Number of Seats
    seats_input = input("Enter number of seats: ")

    if not seats_input.isdigit():
        print("Seats must be a valid number!")
        return

    seats = int(seats_input)

    if seats <= 0:
        print("Number of seats must be greater than 0!")
        return

    if seats > selected_route["available_seats"]:
        print("Not enough seats available!")
        return

    # Generate Unique Booking ID
    booking_number = 1001

    while f"B{booking_number}" in booking_ids:
        booking_number += 1

    booking_id = f"B{booking_number}"

    # Calculate Fare
    total_fare = selected_route["ticket_price"] * seats

    # Create Booking
    booking = {
        "booking_id": booking_id,
        "passenger_name": name,
        "passenger_age": age,
        "route_id": route_id,
        "seats": seats,
        "total_fare": total_fare,
        "status": "Confirmed"
    }

    bookings.append(booking)
    booking_ids.add(booking_id)

    # Reduce Available Seats
    selected_route["available_seats"] -= seats

    print("\n===== BOOKING SUCCESSFUL =====")
    print(f"Booking ID : {booking_id}")
    print(f"Passenger  : {name}")
    print(
        f"Route      : {selected_route['departure_city']} -> "
        f"{selected_route['destination_city']}"
    )
    print(f"Seats      : {seats}")
    print(f"Total Fare : Rs. {total_fare}")
    print("Status     : Confirmed")

def view_bookings():
    print("\n===== MY BOOKINGS =====")

    if len(bookings) == 0:
        print("No bookings found.")
        return

    for number, booking in enumerate(bookings, start=1):
        print(f"\nBooking #{number}")
        print(f"Booking ID : {booking['booking_id']}")
        print(f"Passenger  : {booking['passenger_name']}")
        print(f"Route ID   : {booking['route_id']}")
        print(f"Seats      : {booking['seats']}")
        print(f"Total Fare : Rs. {booking['total_fare']}")
        print(f"Status     : {booking['status']}")


def cancel_booking():
    print("\n===== CANCEL BOOKING =====")

    booking_id = input("Enter Booking ID: ").strip().upper()

    for booking in bookings:

        if booking["booking_id"] == booking_id:

            if booking["status"] == "Cancelled":
                print("This booking is already cancelled!")
                break

            booking["status"] = "Cancelled"

            for route in routes:
                if route["route_id"] == booking["route_id"]:
                    route["available_seats"] += booking["seats"]
                    break

            print("Booking cancelled successfully!")
            print(f"{booking['seats']} seat(s) restored.")
            break

    else:
        print("Booking ID not found!")