import requests

# Function to fetch live fuel prices using RapidAPI
def get_live_prices():
    url = "https://daily-petrol-diesel-lpg-cng-fuel-prices-in-india.p.rapidapi.com/v1/fuel-prices/today/india/telangana"  # Replace with your actual API endpoint
    headers = {
       "x-rapidapi-key": "9e7ffde3femsh7b97028a7f75e86p1af75djsn1261d0f865bc",
	"x-rapidapi-host": "daily-petrol-diesel-lpg-cng-fuel-prices-in-india.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)

        data = response.json()  # Parse the response JSON
        
        # Assuming the API returns prices in a dictionary-like structure
        prices = {
             "petrol": data["fuel"]["petrol"]["retailPrice"],  # Petrol price in INR
        "diesel": data["fuel"]["diesel"]["retailPrice"],  # Diesel price in INR
        "lpg": data["fuel"]["lpg"]["retailPrice"],        # LPG price in INR
        # Provide a default value for CNG if it's not available in the API response
        "cng": data["fuel"].get("cng", {}).get("retailPrice", 70.0),  # Default price for CNG if not provided
        "electricity": 10.0  # Assuming electricity might be static, or from a different API
        }
        return prices
    except requests.exceptions.RequestException as e:
        print(f"Error fetching live fuel prices: {e}")
        return {
            "petrol": 108.0,  # Default values in case of an error
            "diesel": 96.0,
            "lpg":99.0,
            "cng": 70.0,
            "electricity": 10.0
        }

def fuel_vehicle_cost(distance, fuel_efficiency, fuel_price):
    """Calculate the fuel consumption and cost for a fuel vehicle."""
    fuel_needed = distance / fuel_efficiency  # liters or kg
    fuel_cost = fuel_needed * fuel_price  # Total cost
    return fuel_needed, fuel_cost

def electric_vehicle_cost(distance, ev_efficiency, electricity_cost):
    """Calculate the energy consumption and cost for an electric vehicle."""
    energy_needed = distance / ev_efficiency  # kWh
    ev_cost = energy_needed * electricity_cost  # Total cost
    return energy_needed, ev_cost

def hybrid_vehicle_cost(distance, fuel_efficiency, fuel_price, ev_efficiency, electricity_cost, hybrid_split):
    """Calculate the fuel and energy consumption and cost for a hybrid vehicle."""
    fuel_distance = distance * (hybrid_split / 100)
    energy_distance = distance * ((100 - hybrid_split) / 100)

    fuel_needed = fuel_distance / fuel_efficiency  # liters or kg
    energy_needed = energy_distance / ev_efficiency  # kWh
    hybrid_cost = (fuel_needed * fuel_price) + (energy_needed * electricity_cost)  # Total cost

    return fuel_needed, energy_needed, hybrid_cost

def compare_costs():
    print("Welcome to the Fuel Cost Comparison Tool!\n")

    while True:
        try:
            distance = float(input("Enter the distance to be traveled (in kilometers): "))
            if distance <= 0:
                print("Distance must be a positive number. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numerical value for distance.")

    while True:
        try:
            hybrid_split = float(input("Enter the percentage of distance covered by fuel (0 to 100): "))
            if hybrid_split < 0 or hybrid_split > 100:
                print("The percentage must be between 0 and 100. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numerical value for the percentage split.")

    # Get live prices from RapidAPI
    prices = get_live_prices()

    # Display current prices
    print("\nLive Prices (in INR):")
    print(f"Petrol: ₹{prices['petrol']} per liter")
    print(f"Diesel: ₹{prices['diesel']} per liter")
    print(f"CNG: ₹{prices['cng']} per kg")
    print(f"LPG: ₹{prices['lpg']} per kg")  # Display LPG price
    print(f"Electricity: ₹{prices['electricity']} per kWh\n")

    # Fuel vehicle assumptions
    petrol_efficiency = 15.0  # km per liter
    diesel_efficiency = 20.0  # km per liter
    cng_efficiency = 25.0  # km per kg
    lpg_efficiency = 10.0  # km per kg (adjust this as necessary)

    # Electric vehicle assumptions
    ev_efficiency = 5.0  # km per kWh

    # Calculate costs for each type of vehicle
    petrol_fuel_needed, petrol_cost = fuel_vehicle_cost(distance, petrol_efficiency, prices["petrol"])
    diesel_fuel_needed, diesel_cost = fuel_vehicle_cost(distance, diesel_efficiency, prices["diesel"])
    cng_fuel_needed, cng_cost = fuel_vehicle_cost(distance, cng_efficiency, prices["cng"])
    lpg_fuel_needed, lpg_cost = fuel_vehicle_cost(distance, lpg_efficiency, prices["lpg"])  # LPG cost
    ev_energy_needed, ev_cost = electric_vehicle_cost(distance, ev_efficiency, prices["electricity"])

    # Hybrid calculations for each type of fuel based on user input hybrid split
    hybrid_petrol_fuel_needed, hybrid_petrol_energy_needed, hybrid_petrol_cost = hybrid_vehicle_cost(
        distance, petrol_efficiency, prices["petrol"], ev_efficiency, prices["electricity"], hybrid_split
    )
    hybrid_diesel_fuel_needed, hybrid_diesel_energy_needed, hybrid_diesel_cost = hybrid_vehicle_cost(
        distance, diesel_efficiency, prices["diesel"], ev_efficiency, prices["electricity"], hybrid_split
    )
    hybrid_cng_fuel_needed, hybrid_cng_energy_needed, hybrid_cng_cost = hybrid_vehicle_cost(
        distance, cng_efficiency, prices["cng"], ev_efficiency, prices["electricity"], hybrid_split
    )
    hybrid_lpg_fuel_needed, hybrid_lpg_energy_needed, hybrid_lpg_cost = hybrid_vehicle_cost(
        distance, lpg_efficiency, prices["lpg"], ev_efficiency, prices["electricity"], hybrid_split
    )

    # Display fuel consumption and costs
    print("==========================================")
    print(f"For a distance of {distance} km:")
    print("==========================================")
    print("Fuel Vehicle (Petrol):")
    print(f"  Fuel consumed: {petrol_fuel_needed:.2f} liters")
    print(f"  Total cost: ₹{petrol_cost:.2f}")
    print("------------------------------------------")
    print("Fuel Vehicle (Diesel):")
    print(f"  Fuel consumed: {diesel_fuel_needed:.2f} liters")
    print(f"  Total cost: ₹{diesel_cost:.2f}")
    print("------------------------------------------")
    print("Fuel Vehicle (CNG):")
    print(f"  Fuel consumed: {cng_fuel_needed:.2f} kg")
    print(f"  Total cost: ₹{cng_cost:.2f}")
    print("------------------------------------------")
    print("Fuel Vehicle (LPG):")
    print(f"  Fuel consumed: {lpg_fuel_needed:.2f} kg")
    print(f"  Total cost: ₹{lpg_cost:.2f}")  # Display LPG cost
    print("------------------------------------------")
    print("Electric Vehicle (EV):")
    print(f"  Energy consumed: {ev_energy_needed:.2f} kWh")
    print(f"  Total cost: ₹{ev_cost:.2f}")
    print("------------------------------------------")
    print(f"Hybrid Vehicle ({hybrid_split}% Petrol, {100 - hybrid_split}% Electric):")
    print(f"  Fuel consumed: {hybrid_petrol_fuel_needed:.2f} liters")
    print(f"  Energy consumed: {hybrid_petrol_energy_needed:.2f} kWh")
    print(f"  Total cost: ₹{hybrid_petrol_cost:.2f}")
    print("------------------------------------------")
    print(f"Hybrid Vehicle ({hybrid_split}% Diesel, {100 - hybrid_split}% Electric):")
    print(f"  Fuel consumed: {hybrid_diesel_fuel_needed:.2f} liters")
    print(f"  Energy consumed: {hybrid_diesel_energy_needed:.2f} kWh")
    print(f"  Total cost: ₹{hybrid_diesel_cost:.2f}")
    print("------------------------------------------")
    print(f"Hybrid Vehicle ({hybrid_split}% CNG, {100 - hybrid_split}% Electric):")
    print(f"  Fuel consumed: {hybrid_cng_fuel_needed:.2f} kg")
    print(f"  Energy consumed: {hybrid_cng_energy_needed:.2f} kWh")
    print(f"  Total cost: ₹{hybrid_cng_cost:.2f}")
    print("------------------------------------------")
    print(f"Hybrid Vehicle ({hybrid_split}% LPG, {100 - hybrid_split}% Electric):")
    print(f"  Fuel consumed: {hybrid_lpg_fuel_needed:.2f} kg")
    print(f"  Energy consumed: {hybrid_lpg_energy_needed:.2f} kWh")
    print(f"  Total cost: ₹{hybrid_lpg_cost:.2f}")
    print("==========================================")

    # Determine the lowest cost option
    costs = {
        "Petrol": petrol_cost,
        "Diesel": diesel_cost,
        "CNG": cng_cost,
        "LPG": lpg_cost,
        "Electric": ev_cost,
        "Hybrid Petrol": hybrid_petrol_cost,
        "Hybrid Diesel": hybrid_diesel_cost,
        "Hybrid CNG": hybrid_cng_cost,
        "Hybrid LPG": hybrid_lpg_cost
    }
    
    lowest_cost_fuel = min(costs, key=costs.get)
    lowest_cost_value = costs[lowest_cost_fuel]

    # Display the lowest cost option
    print(f"The lowest cost option for traveling {distance} km is {lowest_cost_fuel} with a cost of ₹{lowest_cost_value:.2f}.")

# Run the calculator
compare_costs()