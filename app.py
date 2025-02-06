from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Land prices per Aana (in NPR) for different locations
land_prices = {
    "Kathmandu Metropolitan City": 4500000,
    "Kageshwori Manohara": 3200000,
    "Gokarneshwor": 2800000,
    "Tokha": 3000000,
    "Budhanilkantha": 4000000,
    "Chandragiri": 2500000,
    "Nagarjun": 2200000,
    "Tarakeshwor": 2700000,
    "Shankharapur": 2000000,
    "Lalitpur Metropolitan City": 4200000,
    "Godawari": 3500000,
    "Mahalaxmi": 3000000,
    "Konjyosom": 1800000,
    "Bagmati": 1700000,
    "Bhaktapur Municipality": 3800000,
    "Madhyapur Thimi": 3600000,
    "Changunarayan": 2800000,
    "Suryabinayak": 2900000
}

# Construction cost per sqft (NPR)
construction_cost_per_sqft = 2800  

def format_currency(value):
    """Format currency in NPR lakh/crore notation"""
    if value >= 10**7:
        return f"NPR {value / 10**7:.2f} crore"
    elif value >= 10**5:
        return f"NPR {value / 10**5:.2f} lakh"
    else:
        return f"NPR {value:,.2f}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate_cost():
    try:
        data = request.json
        land_area = float(data.get("land_area", 0))
        location = data.get("location", "")
        house_area = float(data.get("house_area", 0))
        floors = int(data.get("floors", 1))

        if location not in land_prices:
            return jsonify({"error": "Invalid location selected."}), 400

        land_cost = land_area * land_prices[location]
        construction_cost = house_area * floors * construction_cost_per_sqft
        total_cost = land_cost + construction_cost

        return jsonify({
            "land_cost": format_currency(land_cost),
            "construction_cost": format_currency(construction_cost),
            "total_cost": format_currency(total_cost)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
