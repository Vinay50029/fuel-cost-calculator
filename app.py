from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Function to fetch live fuel prices using RapidAPI
def get_live_prices():
    url = "https://daily-petrol-diesel-lpg-cng-fuel-prices-in-india.p.rapidapi.com/v1/fuel-prices/today/india/telangana"  
    headers = {
       "x-rapidapi-key": "9e7ffde3femsh7b97028a7f75e86p1af75djsn1261d0f865bc",
	"x-rapidapi-host": "daily-petrol-diesel-lpg-cng-fuel-prices-in-india.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)

        data = response.json()  # Parse the response JSON
        
                                                                          
        prices = {
            "petrol": data["fuel"]["petrol"]["retailPrice"],              # Petrol price in INR
            "diesel": data["fuel"]["diesel"]["retailPrice"],              # Diesel price in INR
            "lpg": data["fuel"]["lpg"]["retailPrice"],                    # LPG price in INR
            "cng": data["fuel"].get("cng", {}).get("retailPrice", 70.0),  # Default price for CNG if not provided
            "electricity": 10.0                                           # Assuming electricity might be static, or from a different API
        }
        return prices
    except requests.exceptions.RequestException as e:
        print(f"Error fetching live fuel prices: {e}")
        return {
            "petrol": 108.0,  # Default values in case of an error
            "diesel": 96.0,
            "lpg":99.0,
            "cng": 800.0,
            "electricity": 10.0
        }


def fuel_vehicle_cost(distance, fuel_efficiency, fuel_price):
    """Calculate the fuel consumption and cost for a fuel vehicle."""
    fuel_needed = distance / fuel_efficiency  # liters or kg
    fuel_cost = fuel_needed * fuel_price  
    return fuel_needed, fuel_cost

def electric_vehicle_cost(distance, ev_efficiency, electricity_cost):
    """Calculate the energy consumption and cost for an electric vehicle."""
    energy_needed = distance / ev_efficiency  # kWh
    ev_cost = energy_needed * electricity_cost  
    return energy_needed, ev_cost

def hybrid_vehicle_cost(distance, fuel_efficiency, fuel_price, ev_efficiency, electricity_cost, hybrid_split):
    """Calculate the fuel and energy consumption and cost for a hybrid vehicle."""
    fuel_distance = distance * (hybrid_split / 100)
    energy_distance = distance * ((100 - hybrid_split) / 100)

    fuel_needed = fuel_distance / fuel_efficiency  # liters or kg
    energy_needed = energy_distance / ev_efficiency  # kWh
    hybrid_cost = (fuel_needed * fuel_price) + (energy_needed * electricity_cost) 
    return fuel_needed, energy_needed, hybrid_cost

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input
        distance = float(request.form.get("distance"))
        hybrid_split = float(request.form.get("hybrid_split"))

        # Get live prices from RapidAPI
        prices = get_live_prices()

        # Fuel vehicle assumptions
        petrol_efficiency = 21.0  # km per liter
        diesel_efficiency = 2.0  # km per liter
        cng_efficiency = 25.0  # km per kg
        lpg_efficiency = 21.0  # km per kg (adjust this as necessary)
        ev_efficiency = 10.0  # km per kWh

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

        return render_template("index.html", prices=prices,
                       distance=distance,
                       hybrid_split=hybrid_split,
                       petrol_fuel_needed=round(petrol_fuel_needed, 2),
                       petrol_cost=round(petrol_cost, 2),
                       diesel_fuel_needed=round(diesel_fuel_needed, 2),
                       diesel_cost=round(diesel_cost, 2),
                       cng_fuel_needed=round(cng_fuel_needed, 2),
                       cng_cost=round(cng_cost, 2),
                       lpg_fuel_needed=round(lpg_fuel_needed, 2),
                       lpg_cost=round(lpg_cost, 2),
                       ev_energy_needed=round(ev_energy_needed, 2),
                       ev_cost=round(ev_cost, 2),
                       hybrid_petrol_fuel_needed=round(hybrid_petrol_fuel_needed, 2),
                       hybrid_petrol_energy_needed=round(hybrid_petrol_energy_needed, 2),
                       hybrid_petrol_cost=round(hybrid_petrol_cost, 2),
                       hybrid_diesel_fuel_needed=round(hybrid_diesel_fuel_needed, 2),
                       hybrid_diesel_energy_needed=round(hybrid_diesel_energy_needed, 2),
                       hybrid_diesel_cost=round(hybrid_diesel_cost, 2),
                       hybrid_cng_fuel_needed=round(hybrid_cng_fuel_needed, 2),
                       hybrid_cng_energy_needed=round(hybrid_cng_energy_needed, 2),
                       hybrid_cng_cost=round(hybrid_cng_cost, 2),
                       hybrid_lpg_fuel_needed=round(hybrid_lpg_fuel_needed, 2),
                       hybrid_lpg_energy_needed=round(hybrid_lpg_energy_needed, 2),
                       hybrid_lpg_cost=round(hybrid_lpg_cost, 2),
                       lowest_cost_fuel=lowest_cost_fuel,
                       lowest_cost_value=round(lowest_cost_value, 2))
    return render_template("index.html")

if __name__ == "__main__":
    # Check if running in Docker container
    import os
    if os.getenv('FLASK_ENV') == 'production':
        # Docker/Production mode
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        # Development mode
        app.run(host='127.0.0.1', port=5000, debug=True)
