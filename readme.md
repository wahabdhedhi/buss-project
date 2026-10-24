# Smart Bus - Ticket Booking & Reservation System

## Project Overview

Smart Bus is a Python-based console application designed to manage a small bus ticket booking and reservation system.

The system allows users to view bus routes, search for routes, book tickets, view bookings, cancel bookings, check seat availability, and generate booking reports.

## Technologies Used

- Python 3
- Built-in Python features only
- Console-based interface
- In-memory data storage

No external libraries or database are required.

## Features

1. View Available Routes
2. Search for a Route
3. Book a Ticket
4. View My Bookings
5. Cancel a Booking
6. View Seat Availability
7. Generate Booking Report
8. Exit

Additional functionality includes route schedules grouped by departure city.

## Project Files

- `main.py` - Main menu and program flow
- `database.py` - Stores routes, bookings, booking IDs, and supported cities
- `routes_features.py` - Route search, listing, schedules, and seat availability
- `booking_features.py` - Ticket booking, booking history, and cancellation
- `report_features.py` - Booking and revenue reports
- `test_cases.txt` - Test cases and results
- `readme.md` - Project documentation

## How to Run

1. Install Python 3.
2. Keep all project files in the same folder.
3. Open the project folder in a terminal.
4. Run:

   python main.py

5. Select an option from the displayed menu.

## Sample Workflow

1. View available bus routes.
2. Search for a route by Route ID or city.
3. Select Book a Ticket.
4. Enter passenger name and age.
5. Enter the Route ID.
6. Enter the required number of seats.
7. The system generates a unique Booking ID and calculates the total fare.
8. The booking can later be viewed or cancelled.

## Data Storage

The application uses in-memory storage.

All bookings and changes are available only while the program is running. When the program is closed, the data resets to its original state.

## Validation

The system validates:

- Passenger name
- Passenger age
- Route ID
- Number of seats
- Available seat capacity
- Unique booking IDs
- Booking cancellation status
- Invalid menu choices

## Limitations

- No permanent database
- No online payment system
- No user login system
- No GUI in the core application
- Data is not saved after the program closes