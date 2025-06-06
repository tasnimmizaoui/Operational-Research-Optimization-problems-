import streamlit as st
import matplotlib.pyplot as plt
from itertools import product
from math import sqrt
import gurobipy as gp
from gurobipy import GRB

# Function to compute the Euclidean distance between two points
def compute_distance(loc1, loc2):
    dx = loc1[0] - loc2[0]
    dy = loc1[1] - loc2[1]
    return sqrt(dx * dx + dy * dy)

# Streamlit app layout
st.title("Facility Location Problem Optimizer")
st.markdown("""
This app helps you solve the Facility Location Problem, which involves determining the optimal locations to build facilities while minimizing the total costs of construction and transportation.
Follow the steps below to provide inputs and run the optimization.
""")

# Collapsible sections for input
with st.sidebar:
    st.header("Configuration")
    st.markdown("""
    Use the sidebar to adjust the key settings for customers and facilities.
    """)
    # Number of customers and facilities
    num_customers = st.slider("Number of customers", min_value=1, max_value=20, value=2)
    num_facilities = st.slider("Number of facilities", min_value=1, max_value=20, value=5)
    cost_per_mile = st.number_input("Cost per mile (in millions GBP)", value=1.0, format="%.2f")

st.header("Customer and Facility Information")
st.markdown("""
Enter the details for each customer and facility below, including names, locations, and setup costs.
""")

# Input for customer details
with st.expander("Customer Locations and Names"):
    st.markdown("Enter the coordinates and names for each customer.")
    customer_names = []
    customers = []
    for i in range(num_customers):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input(f"Name for Customer {i+1}", f"Customer {i+1}")
        with col2:
            x = st.number_input(f"X-coordinate for Customer {i+1}", value=0.0, key=f"cust_x_{i}")
        with col3:
            y = st.number_input(f"Y-coordinate for Customer {i+1}", value=0.0, key=f"cust_y_{i}")
        customer_names.append(name)
        customers.append((x, y))

# Input for facility details
with st.expander("Facility Locations, Names, and Costs"):
    st.markdown("Enter the coordinates, names, and setup costs for each facility.")
    facility_names = []
    facilities = []
    setup_cost = []
    for i in range(num_facilities):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            name = st.text_input(f"Name for Facility {i+1}", f"Facility {i+1}", key=f"fac_name_{i}")
        with col2:
            x = st.number_input(f"X-coordinate for Facility {i+1}", value=0.0, key=f"fac_x_{i}")
        with col3:
            y = st.number_input(f"Y-coordinate for Facility {i+1}", value=0.0, key=f"fac_y_{i}")
        with col4:
            cost = st.number_input(f"Setup cost for Facility {i+1}", value=1.0, key=f"setup_{i}", format="%.2f")
        facility_names.append(name)
        facilities.append((x, y))
        setup_cost.append(cost)

# Run optimization button
if st.button("Run Optimization"):
    # Solve the optimization problem
    cartesian_prod = list(product(range(num_customers), range(num_facilities)))

    # Compute shipping costs
    shipping_cost = {(c, f): cost_per_mile * compute_distance(customers[c], facilities[f]) for c, f in cartesian_prod}

    # Create the optimization model
    m = gp.Model('facility_location')

    # Decision variables
    select = m.addVars(num_facilities, vtype=GRB.BINARY, name='Select')
    assign = m.addVars(cartesian_prod, ub=1, vtype=GRB.CONTINUOUS, name='Assign')

    # Constraints
    m.addConstrs((assign[(c, f)] <= select[f] for c, f in cartesian_prod), name='Setup2ship')
    m.addConstrs((gp.quicksum(assign[(c, f)] for f in range(num_facilities)) == 1 for c in range(num_customers)), name='Demand')

    # Objective function
    m.setObjective(select.prod(setup_cost) + assign.prod(shipping_cost), GRB.MINIMIZE)

    # Optimize the model
    m.optimize()

    # Display results
    if m.status == GRB.OPTIMAL:
        st.success(f"Optimal solution found with total cost of {m.objVal:.2f} million GBP")

        # Display the facility build plan
        st.subheader("Facility Build Plan")
        facility_locations = []
        for facility in select.keys():
            if abs(select[facility].x) > 1e-6:
                facility_locations.append(facilities[facility])
                st.write(f"Build {facility_names[facility]}.")

        # Display the shipment plan
        st.subheader("Shipment Plan")
        shipment_plan = []
        for customer, facility in assign.keys():
            if abs(assign[customer, facility].x) > 1e-6:
                shipment_plan.append((customers[customer], facilities[facility], round(100 * assign[customer, facility].x, 2)))
                st.write(f"{customer_names[customer]} receives {round(100 * assign[customer, facility].x, 2)}% of its demand from {facility_names[facility]}.")

        # Create a plot to visualize the solution
        fig, ax = plt.subplots(figsize=(8, 8))

        # Plot customer locations
        customer_x, customer_y = zip(*customers)
        ax.scatter(customer_x, customer_y, color='blue', label="Customers", zorder=5)

        # Plot facility locations
        facility_x, facility_y = zip(*facilities)
        ax.scatter(facility_x, facility_y, color='red', label="Facilities", zorder=5)

        # Plot selected facility locations
        if facility_locations:
            selected_x, selected_y = zip(*facility_locations)
            ax.scatter(selected_x, selected_y, color='green', label="Built facility", zorder=6, s=100, marker='X')

        # Plot shipment routes
        for (cust, fac, perc) in shipment_plan:
            ax.plot([cust[0], fac[0]], [cust[1], fac[1]], color='gray', alpha=0.5)  # Gray lines for shipment paths
            ax.text((cust[0] + fac[0]) / 2, (cust[1] + fac[1]) / 2, f"{perc}%", fontsize=10, color="black", ha="center")

        # Add labels and legend
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.set_title("Facility Location Problem - Optimization Solution")
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("No optimal solution found!")
