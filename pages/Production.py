import streamlit as st
import gurobipy as gp
from gurobipy import GRB
import pandas as pd

# Function to solve the factory planning optimization problem
def solve_factory_planning(user_input):
    # Unpacking user input
    products = user_input['products']
    months = user_input['months']

    profit = user_input['profit']
    max_sales = user_input['max_sales']

    holding_cost = user_input['holding_cost']
    max_inventory = user_input['max_inventory']
    store_target = user_input['store_target']
    hours_per_month = user_input['hours_per_month']

    resources = user_input['resources']
    resource_cost = user_input['resource_cost']
    time_req = user_input['time_req']
    down = user_input['down']
    installed = user_input['installed']

    raw_materials = user_input['raw_materials']
    raw_material_availability = user_input['raw_material_availability']
    raw_material_cost = user_input['raw_material_cost']
    material_usage = user_input['material_usage']

    # Model Initialization
    factory = gp.Model('Factory Planning')

    # Decision Variables
    make = factory.addVars([(month, product) for month in months for product in products], name="Make")
    store = factory.addVars([(month, product) for month in months for product in products], ub=max_inventory, name="Store")
    sell = factory.addVars([(month, product) for month in months for product in products], ub=max_sales, name="Sell")

    # Constraints
    # Initial balance
    factory.addConstrs(
        (make[months[0], product] == sell[months[0], product] + store[months[0], product] for product in products),
        name="Initial_Balance"
    )
    # Balance for subsequent months
    factory.addConstrs(
        (store[months[months.index(month) - 1], product] + make[month, product] == sell[month, product] + store[month, product]
         for product in products for month in months if month != months[0]),
        name="Balance"
    )
    # Final inventory targets
    factory.addConstrs(
        (store[months[-1], product] == store_target for product in products),
        name="End_Balance"
    )
    # Resource capacity constraints
    factory.addConstrs(
        (gp.quicksum(time_req[resource][product] * make[month, product] for product in time_req[resource]) <= 
         hours_per_month * (installed[resource] - down.get((month, resource), 0))
         for resource in resources for month in months),
        name="Capacity"
    )
    # Raw material constraints
    factory.addConstrs(
        (gp.quicksum(material_usage[material][product] * make[month, product] for product in products for month in months) <= 
         raw_material_availability[material] for material in raw_materials),
        name="Raw_Material_Limit"
    )

    # Objective Function
    obj = (
        gp.quicksum(profit[product] * sell[month, product] - holding_cost * store[month, product] for month in months for product in products)
        - gp.quicksum(resource_cost[resource] * gp.quicksum(time_req[resource][product] * make[month, product] for product in products)
                      for resource in resources for month in months)
        - gp.quicksum(raw_material_cost[material] * gp.quicksum(material_usage[material][product] * make[month, product] for product in products for month in months)
                      for material in raw_materials)
    )
    factory.setObjective(obj, GRB.MAXIMIZE)

    # Optimization
    factory.optimize()

    # Results
    if factory.status == GRB.OPTIMAL:
        result = {
            'profit': factory.objVal,
            'make_plan': pd.DataFrame(0.0, index=months, columns=products),
            'sell_plan': pd.DataFrame(0.0, index=months, columns=products),
            'store_plan': pd.DataFrame(0.0, index=months, columns=products),
            'raw_material_plan': pd.DataFrame(0.0, index=months, columns=raw_materials)
        }

        for (month, product), var in make.items():
            result['make_plan'].loc[month, product] = var.x

        for (month, product), var in sell.items():
            result['sell_plan'].loc[month, product] = var.x

        for (month, product), var in store.items():
            result['store_plan'].loc[month, product] = var.x

        for month in months:
            for material in raw_materials:
                result['raw_material_plan'].loc[month, material] = sum(
                    material_usage[material][product] * make[month, product].x for product in products
                )

        return result
    else:
        return None

# Streamlit App
st.title("Factory Planning Optimization")
st.sidebar.header("Configuration")

# Sidebar inputs
st.sidebar.subheader("General Settings")
month_count = st.sidebar.number_input("Number of Months", min_value=1, max_value=12, step=1, value=1)
months = [st.sidebar.text_input(f"Name of Month {i + 1}", value=f"Month {i + 1}") for i in range(month_count)]

product_count = st.sidebar.number_input("Number of Products", min_value=1, step=1, value=2)
products = [st.sidebar.text_input(f"Product {i + 1} Name", value=f"Product {i + 1}") for i in range(product_count)]

resource_count = st.sidebar.number_input("Number of Resources", min_value=1, step=1, value=2)
resources = [st.sidebar.text_input(f"Resource {i + 1} Name", value=f"Resource {i + 1}") for i in range(resource_count)]

# Raw material inputs
st.sidebar.subheader("Raw Material Settings")
raw_material_count = st.sidebar.number_input("Number of Raw Materials", min_value=1, step=1, value=3)
raw_materials = [st.sidebar.text_input(f"Raw Material {i + 1} Name", value=f"Material {i + 1}") for i in range(raw_material_count)]

raw_material_availability = {
    material: st.sidebar.number_input(f"Available Quantity of {material}", min_value=0, step=1) for material in raw_materials
}

raw_material_cost = {
    material: st.sidebar.number_input(f"Cost of {material}", min_value=0.0, step=0.01) for material in raw_materials
}

# Main inputs
st.subheader("Input Product Details")
profit = {product: st.number_input(f"Profit for {product}", min_value=0, step=1) for product in products}
max_sales = {(month, product): st.number_input(f"Max Sales of {product} in {month}", min_value=0, step=10) for month in months for product in products}

st.subheader("Input Resource Details")
resource_cost = {resource: st.number_input(f"Cost of {resource} per hour", min_value=0.0, step=0.1) for resource in resources}
time_req = {resource: {product: st.number_input(f"Time Required for {product} on {resource}", min_value=0.0, step=0.1) for product in products} for resource in resources}
down = {(month, resource): st.number_input(f"Number of {resource} Down in {month}", min_value=0, step=1) for month in months for resource in resources}
installed = {resource: st.number_input(f"Number of Installed {resource}", min_value=1, step=1) for resource in resources}

# Material usage per product
st.subheader("Input Material Details")
material_usage = {material: {product: st.number_input(f"{material} Required for {product}", min_value=0.0, step=0.1) for product in products} for material in raw_materials}

st.subheader("Cost and Inventory Parameters")
holding_cost = st.number_input("Holding Cost", min_value=0.0, step=0.01, value=0.5)
max_inventory = st.number_input("Maximum Inventory", min_value=1, step=1, value=100)
store_target = st.number_input("Store Target", min_value=1, step=1, value=50)
hours_per_month = st.number_input("Hours per Month", min_value=1, step=1, value=160)

# Optimization
if st.button("Optimize"):
    user_input = {
        'products': products,
        'profit': profit,
        'max_sales': max_sales,
        'resources': resources,
        'resource_cost': resource_cost,
        'time_req': time_req,
        'down': down,
        'installed': installed,
        'months': months,
        'holding_cost': holding_cost,
        'max_inventory': max_inventory,
        'store_target': store_target,
        'hours_per_month': hours_per_month,
        'raw_materials': raw_materials,
        'raw_material_availability': raw_material_availability,
        'raw_material_cost': raw_material_cost,
        'material_usage': material_usage
    }

    result = solve_factory_planning(user_input)

    if result:
        st.success(f"Optimization Complete! Maximum Profit: {result['profit']:.2f}")
        st.subheader("Production Plan")
        st.dataframe(result['make_plan'])
        st.subheader("Sales Plan")
        st.dataframe(result['sell_plan'])
        st.subheader("Inventory Plan")
        st.dataframe(result['store_plan'])
        st.subheader("Raw Material Usage Plan")
        st.dataframe(result['raw_material_plan'])
    else:
        st.error("Optimization failed. Please check your inputs.")
