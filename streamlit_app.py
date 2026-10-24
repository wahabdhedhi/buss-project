import streamlit as st
from copy import deepcopy
from database import routes as original_routes


# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="Smart Bus",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# SESSION STATE
# =========================================================

if "routes_ui" not in st.session_state:
    st.session_state.routes_ui = deepcopy(original_routes)

if "bookings_ui" not in st.session_state:
    st.session_state.bookings_ui = []

if "booking_counter_ui" not in st.session_state:
    st.session_state.booking_counter_ui = 1001

if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Home"

if "selected_route_id_ui" not in st.session_state:
    st.session_state.selected_route_id_ui = None

if "notice" not in st.session_state:
    st.session_state.notice = None


# =========================================================
# MINIMAL SLEEK DESIGN
# =========================================================

st.markdown(
    """
    <style>

    :root {
        --text: #0f172a;
        --muted: #64748b;
        --line: #e8edf3;
        --soft: #f8fafc;
        --blue: #2563eb;
        --blue-dark: #1d4ed8;
    }

    /* Main page */
    .stApp {
        background-color: #ffffff;
        color: var(--text);
    }

    .block-container {
        max-width: 1180px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #fbfcfe;
        border-right: 1px solid var(--line);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    /* Headings */
    h1, h2, h3 {
        color: var(--text);
        letter-spacing: -0.03em;
    }

    h1 {
        font-weight: 750 !important;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 18px 20px;
        box-shadow: 0 6px 24px rgba(15, 23, 42, 0.035);
    }

    /* Containers / cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--line) !important;
        border-radius: 20px !important;
        background: white;
        box-shadow: 0 6px 24px rgba(15, 23, 42, 0.035);
    }

    /* Buttons */
    .stButton > button {
        min-height: 46px;
        border-radius: 12px;
        font-weight: 650;
        border: 1px solid #dbe3ee;
        box-shadow: none;
        transition: all 0.18s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        border-color: #b8c6da;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
    }

    .stButton > button[kind="primary"] {
        background: var(--blue);
        color: white;
        border-color: var(--blue);
    }

    .stButton > button[kind="primary"]:hover {
        background: var(--blue-dark);
        border-color: var(--blue-dark);
    }

    /* Input fields */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border-color: #dbe3ee !important;
        min-height: 46px;
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 1px var(--blue) !important;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 14px;
    }

    /* Progress */
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: var(--blue);
    }

    /* Sidebar navigation */
    div[role="radiogroup"] label {
        padding: 8px 10px;
        border-radius: 10px;
        margin-bottom: 2px;
    }

    div[role="radiogroup"] label:hover {
        background: #f1f5f9;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 16px;
        overflow: hidden;
    }

    /* Hide Streamlit footer/menu */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def find_route(route_id):

    for route in st.session_state.routes_ui:

        if route["route_id"] == route_id:
            return route

    return None


def find_booking(booking_id):

    for booking in st.session_state.bookings_ui:

        if booking["booking_id"] == booking_id:
            return booking

    return None


def route_status(route):

    if route["available_seats"] == 0:
        return "Fully booked"

    elif route["available_seats"] == route["total_seats"]:
        return "Available"

    else:
        return "Limited seats"


def route_status_badge(route):

    status = route_status(route)

    if status == "Available":
        return "🟢 Available"

    elif status == "Limited seats":
        return "🟠 Limited seats"

    else:
        return "🔴 Fully booked"


def go_to(page_name):

    st.session_state.nav_page = page_name


def go_to_booking(route_id):

    st.session_state.selected_route_id_ui = route_id
    st.session_state.nav_page = "Book Ticket"


def reset_demo():

    st.session_state.routes_ui = deepcopy(original_routes)

    st.session_state.bookings_ui = []

    st.session_state.booking_counter_ui = 1001

    st.session_state.selected_route_id_ui = None

    st.session_state.notice = "Demo data reset successfully."


def show_page_header(title, subtitle):

    st.title(title)

    st.caption(subtitle)

    st.write("")


def show_route(route, show_action=False, action_key=""):

    with st.container(border=True):

        title_col, fare_col = st.columns([3.4, 1])

        with title_col:

            st.subheader(
                f"{route['departure_city']} → "
                f"{route['destination_city']}"
            )

            st.caption(
                f"{route['route_id']}  ·  "
                f"Departs {route['departure_time']}"
            )

        with fare_col:

            st.metric(
                "Fare",
                f"Rs. {route['ticket_price']:,}"
            )

        info1, info2, info3 = st.columns(3)

        with info1:

            st.caption("AVAILABILITY")

            st.write(
                f"**{route['available_seats']} seats left**"
            )

        with info2:

            st.caption("CAPACITY")

            st.write(
                f"**{route['total_seats']} seats**"
            )

        with info3:

            st.caption("STATUS")

            st.write(
                f"**{route_status_badge(route)}**"
            )

        reserved = (
            route["total_seats"]
            - route["available_seats"]
        )

        if route["total_seats"] > 0:

            occupancy = (
                reserved
                / route["total_seats"]
            )

        else:

            occupancy = 0

        st.progress(occupancy)

        if (
            show_action
            and route["available_seats"] > 0
        ):

            st.button(
                "Book this route",
                key=(
                    f"book_route_"
                    f"{action_key}_"
                    f"{route['route_id']}"
                ),
                type="primary",
                use_container_width=True,
                on_click=go_to_booking,
                args=(route["route_id"],),
            )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🚌 Smart Bus")

    st.caption(
        "Simple booking. Better journeys."
    )

    st.write("")

    pages = [
        "Home",
        "Routes",
        "Book Ticket",
        "My Bookings",
        "Cancel Booking",
        "Seat Availability",
        "Reports",
    ]

    page = st.radio(
        "Navigation",
        pages,
        key="nav_page",
        label_visibility="collapsed",
    )

    st.write("")

    st.divider()

    st.caption("DEMO TOOLS")

    st.button(
        "Reset demo data",
        on_click=reset_demo,
        use_container_width=True,
    )

    st.caption(
        "Smart Bus · Reservation System"
    )


# =========================================================
# NOTICE
# =========================================================

if st.session_state.notice:

    st.success(
        st.session_state.notice
    )

    st.session_state.notice = None


# =========================================================
# HOME PAGE
# =========================================================

if page == "Home":

    show_page_header(
        "Travel, without the hassle.",
        "Find a route, reserve your seat and manage your booking in a few clicks.",
    )

    action1, action2, spacer = st.columns(
        [1.15, 1.15, 3.7]
    )

    with action1:

        st.button(
            "Book a ticket",
            type="primary",
            use_container_width=True,
            on_click=go_to,
            args=("Book Ticket",),
        )

    with action2:

        st.button(
            "Explore routes",
            use_container_width=True,
            on_click=go_to,
            args=("Routes",),
        )

    st.write("")
    st.write("")

    total_available = 0

    for route in st.session_state.routes_ui:

        total_available += (
            route["available_seats"]
        )

    confirmed = []

    for booking in st.session_state.bookings_ui:

        if booking["status"] == "Confirmed":

            confirmed.append(booking)

    revenue = 0

    for booking in confirmed:

        revenue += booking["total_fare"]

    # Metrics
    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Routes",
            len(st.session_state.routes_ui),
            border=True,
        )

    with m2:

        st.metric(
            "Seats available",
            total_available,
            border=True,
        )

    with m3:

        st.metric(
            "Active bookings",
            len(confirmed),
            border=True,
        )

    with m4:

        st.metric(
            "Revenue",
            f"Rs. {revenue:,}",
            border=True,
        )

    st.write("")

    st.subheader(
        "Recommended routes"
    )

    st.caption(
        "Popular departures available right now."
    )

    for index, route in enumerate(
        st.session_state.routes_ui[:3],
        start=1,
    ):

        show_route(
            route,
            show_action=True,
            action_key=f"home_{index}",
        )


# =========================================================
# ROUTES PAGE
# =========================================================

elif page == "Routes":

    show_page_header(
        "Find your route",
        "Search by route ID, departure city or destination.",
    )

    search = st.text_input(
        "Search routes",
        placeholder=(
            "Try Karachi, Lahore or R101"
        ),
        label_visibility="collapsed",
    )

    search_value = (
        search.strip().lower()
    )

    filtered_routes = []

    for route in st.session_state.routes_ui:

        if not search_value:

            filtered_routes.append(route)

        elif (
            search_value
            in route["route_id"].lower()
            or search_value
            in route[
                "departure_city"
            ].lower()
            or search_value
            in route[
                "destination_city"
            ].lower()
        ):

            filtered_routes.append(route)

    st.caption(
        f"{len(filtered_routes)} route(s) found"
    )

    st.write("")

    if not filtered_routes:

        st.info(
            "No route matches your search."
        )

    else:

        for index, route in enumerate(
            filtered_routes,
            start=1,
        ):

            show_route(
                route,
                show_action=True,
                action_key=f"routes_{index}",
            )


# =========================================================
# BOOK TICKET PAGE
# =========================================================

elif page == "Book Ticket":

    show_page_header(
        "Book your ticket",
        "Passenger details first, then choose your journey.",
    )

    available_routes = []

    for route in st.session_state.routes_ui:

        if route["available_seats"] > 0:

            available_routes.append(route)

    if not available_routes:

        st.warning(
            "All routes are currently fully booked."
        )

    else:

        with st.container(border=True):

            st.subheader(
                "Passenger details"
            )

            name_col, age_col = (
                st.columns([2, 1])
            )

            with name_col:

                passenger_name = (
                    st.text_input(
                        "Full name",
                        placeholder=(
                            "Passenger name"
                        ),
                    )
                )

            with age_col:

                passenger_age = (
                    st.number_input(
                        "Age",
                        min_value=1,
                        max_value=120,
                        value=18,
                        step=1,
                    )
                )

            st.write("")

            st.subheader("Journey")

            route_ids = []

            for route in available_routes:

                route_ids.append(
                    route["route_id"]
                )

            preferred_route = (
                st.session_state
                .selected_route_id_ui
            )

            if preferred_route in route_ids:

                selected_index = (
                    route_ids.index(
                        preferred_route
                    )
                )

            else:

                selected_index = 0

            selected_route_id = (
                st.selectbox(
                    "Choose route",
                    route_ids,
                    index=selected_index,
                    format_func=lambda rid: (
                        f"{rid}  ·  "
                        f"{find_route(rid)['departure_city']} "
                        f"→ "
                        f"{find_route(rid)['destination_city']} "
                        f" · "
                        f"{find_route(rid)['departure_time']}"
                    ),
                )
            )

            selected_route = find_route(
                selected_route_id
            )

            route_col, seats_col = (
                st.columns([2, 1])
            )

            with route_col:

                st.caption(
                    "SELECTED ROUTE"
                )

                st.subheader(
                    f"{selected_route['departure_city']} "
                    f"→ "
                    f"{selected_route['destination_city']}"
                )

                st.caption(
                    f"Departure "
                    f"{selected_route['departure_time']} "
                    f"· "
                    f"Rs. "
                    f"{selected_route['ticket_price']:,} "
                    f"per seat"
                )

            with seats_col:

                seats = st.selectbox(
                    "Seats",
                    list(
                        range(
                            1,
                            selected_route[
                                "available_seats"
                            ] + 1,
                        )
                    ),
                )

            total_fare = (
                selected_route[
                    "ticket_price"
                ]
                * seats
            )

            st.divider()

            fare_col, button_col = (
                st.columns([2, 1.2])
            )

            with fare_col:

                st.caption("TOTAL")

                st.subheader(
                    f"Rs. {total_fare:,}"
                )

                st.caption(
                    f"{seats} seat(s)"
                )

            with button_col:

                st.write("")

                confirm_booking = (
                    st.button(
                        "Confirm booking",
                        type="primary",
                        use_container_width=True,
                    )
                )

        # ---------------------------------------------
        # PROCESS BOOKING
        # ---------------------------------------------

        if confirm_booking:

            clean_name = (
                passenger_name.strip()
            )

            if clean_name == "":

                st.error(
                    "Please enter the passenger name."
                )

            elif (
                seats
                > selected_route[
                    "available_seats"
                ]
            ):

                st.error(
                    "The selected number of seats is no longer available."
                )

            else:

                booking_id = (
                    f"B"
                    f"{st.session_state.booking_counter_ui}"
                )

                booking = {

                    "booking_id":
                        booking_id,

                    "passenger_name":
                        clean_name,

                    "passenger_age":
                        int(passenger_age),

                    "route_id":
                        selected_route_id,

                    "seats":
                        int(seats),

                    "total_fare":
                        total_fare,

                    "status":
                        "Confirmed",
                }

                st.session_state.bookings_ui.append(
                    booking
                )

                selected_route[
                    "available_seats"
                ] -= seats

                st.session_state.booking_counter_ui += 1

                st.success(
                    "Booking confirmed successfully."
                )

                # Booking receipt
                with st.container(
                    border=True
                ):

                    receipt_left, receipt_right = (
                        st.columns([2, 1])
                    )

                    with receipt_left:

                        st.subheader(
                            f"Booking {booking_id}"
                        )

                        st.write(
                            f"**{clean_name}**"
                        )

                        st.caption(
                            f"{selected_route['departure_city']} "
                            f"→ "
                            f"{selected_route['destination_city']} "
                            f"· "
                            f"{selected_route['departure_time']}"
                        )

                    with receipt_right:

                        st.metric(
                            "Total paid",
                            f"Rs. {total_fare:,}",
                        )

                    r1, r2, r3 = (
                        st.columns(3)
                    )

                    with r1:

                        st.metric(
                            "Seats",
                            seats,
                        )

                    with r2:

                        st.metric(
                            "Route",
                            selected_route_id,
                        )

                    with r3:

                        st.metric(
                            "Status",
                            "Confirmed",
                        )


# =========================================================
# MY BOOKINGS PAGE
# =========================================================

elif page == "My Bookings":

    show_page_header(
        "My bookings",
        "Everything you have booked, in one place.",
    )

    if not st.session_state.bookings_ui:

        st.info(
            "No bookings yet. Your confirmed tickets will appear here."
        )

        st.button(
            "Book your first ticket",
            type="primary",
            on_click=go_to,
            args=("Book Ticket",),
        )

    else:

        filter_value = st.selectbox(
            "Show",
            [
                "All bookings",
                "Confirmed",
                "Cancelled",
            ],
        )

        visible_bookings = []

        for booking in (
            st.session_state.bookings_ui
        ):

            if (
                filter_value
                == "All bookings"
                or booking["status"]
                == filter_value
            ):

                visible_bookings.append(
                    booking
                )

        if not visible_bookings:

            st.info(
                "No bookings match this filter."
            )

        for booking in reversed(
            visible_bookings
        ):

            route = find_route(
                booking["route_id"]
            )

            with st.container(
                border=True
            ):

                top_left, top_right = (
                    st.columns([3, 1])
                )

                with top_left:

                    st.subheader(
                        f"{route['departure_city']} "
                        f"→ "
                        f"{route['destination_city']}"
                    )

                    st.caption(
                        f"Booking "
                        f"{booking['booking_id']} "
                        f"· "
                        f"{route['departure_time']}"
                    )

                with top_right:

                    if (
                        booking["status"]
                        == "Confirmed"
                    ):

                        st.success(
                            "Confirmed"
                        )

                    else:

                        st.error(
                            "Cancelled"
                        )

                b1, b2, b3 = (
                    st.columns(3)
                )

                with b1:

                    st.metric(
                        "Passenger",
                        booking[
                            "passenger_name"
                        ],
                    )

                with b2:

                    st.metric(
                        "Seats",
                        booking["seats"],
                    )

                with b3:

                    st.metric(
                        "Fare",
                        f"Rs. "
                        f"{booking['total_fare']:,}",
                    )


# =========================================================
# CANCEL BOOKING PAGE
# =========================================================

elif page == "Cancel Booking":

    show_page_header(
        "Cancel a booking",
        "Choose a confirmed booking. Reserved seats will be restored automatically.",
    )

    confirmed_bookings = []

    for booking in (
        st.session_state.bookings_ui
    ):

        if (
            booking["status"]
            == "Confirmed"
        ):

            confirmed_bookings.append(
                booking
            )

    if not confirmed_bookings:

        st.info(
            "There are no confirmed bookings available to cancel."
        )

    else:

        booking_ids = []

        for booking in confirmed_bookings:

            booking_ids.append(
                booking["booking_id"]
            )

        selected_booking_id = (
            st.selectbox(
                "Booking",
                booking_ids,
                format_func=lambda bid: (
                    f"{bid}  ·  "
                    f"{find_booking(bid)['passenger_name']} "
                    f"· "
                    f"{find_booking(bid)['route_id']}"
                ),
            )
        )

        selected_booking = (
            find_booking(
                selected_booking_id
            )
        )

        selected_route = (
            find_route(
                selected_booking[
                    "route_id"
                ]
            )
        )

        with st.container(
            border=True
        ):

            st.subheader(
                f"{selected_route['departure_city']} "
                f"→ "
                f"{selected_route['destination_city']}"
            )

            st.caption(
                f"{selected_booking_id} "
                f"· "
                f"{selected_route['departure_time']}"
            )

            c1, c2, c3 = (
                st.columns(3)
            )

            with c1:

                st.metric(
                    "Passenger",
                    selected_booking[
                        "passenger_name"
                    ],
                )

            with c2:

                st.metric(
                    "Seats",
                    selected_booking[
                        "seats"
                    ],
                )

            with c3:

                st.metric(
                    "Fare",
                    f"Rs. "
                    f"{selected_booking['total_fare']:,}",
                )

        st.warning(
            "This action will cancel the booking and restore its seats."
        )

        if st.button(
            "Cancel booking",
            type="primary",
            use_container_width=True,
        ):

            if (
                selected_booking[
                    "status"
                ]
                == "Confirmed"
            ):

                selected_booking[
                    "status"
                ] = "Cancelled"

                selected_route[
                    "available_seats"
                ] += selected_booking[
                    "seats"
                ]

                st.session_state.notice = (
                    f"Booking "
                    f"{selected_booking_id} "
                    f"cancelled. "
                    f"{selected_booking['seats']} "
                    f"seat(s) restored."
                )

                st.rerun()


# =========================================================
# SEAT AVAILABILITY PAGE
# =========================================================

elif page == "Seat Availability":

    show_page_header(
        "Seat availability",
        "A clear view of remaining capacity across every route.",
    )

    total_capacity = 0
    total_available = 0

    for route in (
        st.session_state.routes_ui
    ):

        total_capacity += (
            route["total_seats"]
        )

        total_available += (
            route["available_seats"]
        )

    total_reserved = (
        total_capacity
        - total_available
    )

    s1, s2, s3 = (
        st.columns(3)
    )

    with s1:

        st.metric(
            "Total capacity",
            total_capacity,
            border=True,
        )

    with s2:

        st.metric(
            "Available",
            total_available,
            border=True,
        )

    with s3:

        st.metric(
            "Reserved",
            total_reserved,
            border=True,
        )

    st.write("")

    for route in (
        st.session_state.routes_ui
    ):

        show_route(route)


# =========================================================
# REPORTS PAGE
# =========================================================

elif page == "Reports":

    show_page_header(
        "Booking report",
        "Live summary of bookings, seats and confirmed revenue.",
    )

    total_bookings = len(
        st.session_state.bookings_ui
    )

    confirmed_bookings = []
    cancelled_bookings = []

    for booking in (
        st.session_state.bookings_ui
    ):

        if (
            booking["status"]
            == "Confirmed"
        ):

            confirmed_bookings.append(
                booking
            )

        elif (
            booking["status"]
            == "Cancelled"
        ):

            cancelled_bookings.append(
                booking
            )

    reserved_seats = 0
    confirmed_revenue = 0

    for booking in (
        confirmed_bookings
    ):

        reserved_seats += (
            booking["seats"]
        )

        confirmed_revenue += (
            booking["total_fare"]
        )

    fully_booked = 0

    for route in (
        st.session_state.routes_ui
    ):

        if (
            route["available_seats"]
            == 0
        ):

            fully_booked += 1

    # Report metrics
    row1 = st.columns(3)

    with row1[0]:

        st.metric(
            "Total bookings",
            total_bookings,
            border=True,
        )

    with row1[1]:

        st.metric(
            "Confirmed",
            len(
                confirmed_bookings
            ),
            border=True,
        )

    with row1[2]:

        st.metric(
            "Cancelled",
            len(
                cancelled_bookings
            ),
            border=True,
        )

    row2 = st.columns(3)

    with row2[0]:

        st.metric(
            "Reserved seats",
            reserved_seats,
            border=True,
        )

    with row2[1]:

        st.metric(
            "Revenue",
            f"Rs. "
            f"{confirmed_revenue:,}",
            border=True,
        )

    with row2[2]:

        st.metric(
            "Fully booked routes",
            fully_booked,
            border=True,
        )

    st.write("")

    st.subheader(
        "Route performance"
    )

    st.caption(
        "Confirmed bookings only."
    )

    report_rows = []

    # Nested loops required by project
    for route in (
        st.session_state.routes_ui
    ):

        route_bookings = []

        for booking in (
            confirmed_bookings
        ):

            if (
                booking["route_id"]
                == route["route_id"]
            ):

                route_bookings.append(
                    booking
                )

        route_reserved = 0
        route_revenue = 0

        for booking in (
            route_bookings
        ):

            route_reserved += (
                booking["seats"]
            )

            route_revenue += (
                booking["total_fare"]
            )

        report_rows.append(
            {
                "Route":
                    route["route_id"],

                "Journey":
                    (
                        f"{route['departure_city']} "
                        f"→ "
                        f"{route['destination_city']}"
                    ),

                "Bookings":
                    len(
                        route_bookings
                    ),

                "Reserved seats":
                    route_reserved,

                "Available seats":
                    route[
                        "available_seats"
                    ],

                "Revenue":
                    route_revenue,
            }
        )

    st.dataframe(
        report_rows,
        hide_index=True,
        use_container_width=True,
    )