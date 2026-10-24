from report_features import generate_booking_report
from routes_features import view_routes, search_route, view_seat_availability,view_route_schedule
from booking_features import book_ticket,view_bookings,cancel_booking


while True:
    print("\n===== SMART BUS RESERVATION SYSTEM =====")
    print("1. View Available Routes")
    print("2. Search for a Route")
    print("3. Book a Ticket")
    print("4. View My Bookings")
    print("5. Cancel a Booking")
    print("6. View Seat Availability")
    print("7. Generate Booking Report")
    print("8. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        view_routes()
        view_route_schedule()

    elif choice == "2":
        search_route()

    elif choice == "3":
        book_ticket()

    elif choice == "4":
        view_bookings()

    elif choice == "5":
        cancel_booking()

    elif choice == "6":
        view_seat_availability()

    elif choice == "7":
        generate_booking_report()

    elif choice == "8":
        print("Thank you for using Smart Bus Reservation System!")
        break

    else:
        print("Invalid choice! Please select from 1 to 8.")