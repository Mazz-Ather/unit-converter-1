import streamlit as st
import streamlit.components.v1 as components
import requests

# Initialize session state for history if not already done
if 'history' not in st.session_state:
    st.session_state.history = []

# Cache the currency API response for 10 minutes
@st.cache_data(ttl=600)
def fetch_currency_rates():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        return response.json().get("rates", {})
    except Exception as e:
        st.error("Error fetching currency rates")
        return {}

# Conversion functions
def distance_converter(from_unit, to_unit, value):
    units = {
        "Meters": 1,
        "Kilometers": 1000,
        "Feet": 0.3048,
        "Miles": 1609.34,
        "Yards": 0.9144,
        "Inches": 0.0254
    }
    return value * units[from_unit] / units[to_unit]

def temperature_converter(from_unit, to_unit, value):
    if from_unit == "Celsius" and to_unit == "Fahrenheit":
        return (value * 9/5) + 32
    elif from_unit == "Fahrenheit" and to_unit == "Celsius":
        return (value - 32) * 5/9
    return value

def weight_converter(from_unit, to_unit, value):
    units = {
        "Kilograms": 1,
        "Grams": 0.001,
        "Pounds": 0.453592,
        "Ounces": 0.0283495,
        "Stones": 6.35029
    }
    return value * units[from_unit] / units[to_unit]

def pressure_converter(from_unit, to_unit, value):
    units = {
        "Pascals": 1,
        "Hectopascals": 100,
        "Kilopascals": 1000,
        "Bar": 100000,
        "Atmospheres": 101325
    }
    return value * units[from_unit] / units[to_unit]

def currency_converter(from_unit, to_unit, value, rates):
    return value * rates[to_unit] / rates[from_unit]

def time_converter(from_unit, to_unit, value):
    units = {
        "Seconds": 1,
        "Minutes": 60,
        "Hours": 3600,
        "Days": 86400,
        "Weeks": 604800,
        "Months": 2628000
    }
    return value * units[from_unit] / units[to_unit]

def volume_converter(from_unit, to_unit, value):
    units = {
        "Liters": 1,
        "Milliliters": 0.001,
        "Gallons": 3.78541,
        "Cups": 0.236588,
        "Cubic Meters": 1000
    }
    return value * units[from_unit] / units[to_unit]

def area_converter(from_unit, to_unit, value):
    units = {
        "Square Meters": 1,
        "Square Kilometers": 1e6,
        "Acres": 4046.86,
        "Hectares": 10000
    }
    return value * units[from_unit] / units[to_unit]

def speed_converter(from_unit, to_unit, value):
    units = {
        "Meters per second": 1,
        "Kilometers per hour": 0.277778,
        "Miles per hour": 0.44704,
        "Knots": 0.514444
    }
    return value * units[from_unit] / units[to_unit]

def data_converter(from_unit, to_unit, value):
    units = {
        "Bytes": 1,
        "Kilobytes": 1024,
        "Megabytes": 1024**2,
        "Gigabytes": 1024**3,
        "Terabytes": 1024**4
    }
    return value * units[from_unit] / units[to_unit]

# Fetch real-time currency rates
currency_rates = fetch_currency_rates()

# Enhanced CSS styling
st.markdown(
    """
    <style>
    /* Global background & font */
    body {
        background: linear-gradient(135deg, #f0f2f6, #ffffff);
        font-family: 'Arial', sans-serif;
    }
    /* Title styling */
    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: #4CAF50;
        margin-bottom: 20px;
    }
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        font-size: 28px;
        color: #2196F3;
        margin-bottom: 15px;
    }
    /* Converter card container */
    .converter-container {
        background: #fff;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin: 20px auto;
        max-width: 800px;
    }
    /* History container styling */
    .history {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 5px;
        margin-top: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    /* Button styling */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main Title
st.markdown("<div class='title'>🔄 Enhanced Unit Converter</div>", unsafe_allow_html=True)
st.write("Convert between different units easily!")

# Wrap the conversion UI in a container card
st.markdown("<div class='converter-container'>", unsafe_allow_html=True)

# Updated list of categories
categories = ["Distance", "Temperature", "Weight", "Pressure", "Currency", "Time", "Volume", "Area", "Speed", "Data"]
category = st.selectbox("Select Category", categories)
st.markdown(f"<div class='subtitle'>{category} Conversion</div>", unsafe_allow_html=True)

# Unit options for each category
unit_options = {
    "Distance": ["Meters", "Kilometers", "Feet", "Miles", "Yards", "Inches"],
    "Temperature": ["Celsius", "Fahrenheit"],
    "Weight": ["Kilograms", "Grams", "Pounds", "Ounces", "Stones"],
    "Pressure": ["Pascals", "Hectopascals", "Kilopascals", "Bar", "Atmospheres"],
    "Currency": ["USD", "EUR", "INR", "JPY", "GBP", "AUD", "PKR"],
    "Time": ["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months"],
    "Volume": ["Liters", "Milliliters", "Gallons", "Cups", "Cubic Meters"],
    "Area": ["Square Meters", "Square Kilometers", "Acres", "Hectares"],
    "Speed": ["Meters per second", "Kilometers per hour", "Miles per hour", "Knots"],
    "Data": ["Bytes", "Kilobytes", "Megabytes", "Gigabytes", "Terabytes"]
}

from_unit = st.selectbox("From", unit_options[category])
to_unit = st.selectbox("To", unit_options[category])
value = st.number_input("Enter Value", min_value=0.0, format="%.2f")

if st.button("Convert"):
    if category == "Distance":
        result = distance_converter(from_unit, to_unit, value)
        factor = distance_converter(from_unit, to_unit, 1)
        st.write(f"📏 Formula: {value} {from_unit} × {factor:.4f} = {result:.2f} {to_unit}")
    elif category == "Temperature":
        result = temperature_converter(from_unit, to_unit, value)
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            formula = f"({value}°C × 9/5) + 32 = {result:.2f}°F"
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            formula = f"({value}°F - 32) × 5/9 = {result:.2f}°C"
        else:
            formula = f"{value}°{from_unit} = {result:.2f}°{to_unit}"
        st.write(f"🌡️ Formula: {formula}")
    elif category == "Weight":
        result = weight_converter(from_unit, to_unit, value)
        factor = weight_converter(from_unit, to_unit, 1)
        st.write(f"⚖️ Formula: {value} {from_unit} × {factor:.4f} = {result:.2f} {to_unit}")
    elif category == "Pressure":
        result = pressure_converter(from_unit, to_unit, value)
        factor = pressure_converter(from_unit, to_unit, 1)
        st.write(f"🛠️ Formula: {value} {from_unit} × {factor:.4f} = {result:.2f} {to_unit}")
    elif category == "Currency":
        result = currency_converter(from_unit, to_unit, value, currency_rates)
        factor = currency_converter(from_unit, to_unit, 1, currency_rates)
        st.write(f"💱 Formula: {value} {from_unit} × {factor:.4f} = {result:.2f} {to_unit}")
        st.write("Note: Currency rates are fetched in real-time")
    elif category == "Time":
        result = time_converter(from_unit, to_unit, value)
        factor = time_converter(from_unit, to_unit, 1)
        st.write(f"⏳ Formula: {value} {from_unit} × {factor:.4f} = {result:.2f} {to_unit}")
    elif category == "Volume":
        result = volume_converter(from_unit, to_unit, value)
        factor = volume_converter(from_unit, to_unit, 1)
        st.write(f"🧪 Formula: {value} {from_unit} × {factor:.4f} = {result:.2f} {to_unit}")
    elif category == "Area":
        result = area_converter(from_unit, to_unit, value)
        factor = area_converter(from_unit, to_unit, 1)
        st.write(f"📐 Formula: {value} {from_unit} × {factor:.4f} = {result:.2f} {to_unit}")
    elif category == "Speed":
        result = speed_converter(from_unit, to_unit, value)
        factor = speed_converter(from_unit, to_unit, 1)
        st.write(f"🚀 Formula: {value} {from_unit} × {factor:.4f} = {result:.2f} {to_unit}")
    elif category == "Data":
        result = data_converter(from_unit, to_unit, value)
        factor = data_converter(from_unit, to_unit, 1)
        st.write(f"💾 Formula: {value} {from_unit} × {factor:.4f} = {result:.2f} {to_unit}")
    
    st.success(f"{value} {from_unit} is equal to {result:.2f} {to_unit}")
    st.session_state.history.append(f"{value} {from_unit} → {result:.2f} {to_unit}")

st.markdown("</div>", unsafe_allow_html=True)  # End of converter container

# Display Conversion History with Clear History and Refresh Currency Rates options
st.subheader("🕒 Conversion History")
if st.session_state.history:
    st.markdown("<div class='history'>", unsafe_allow_html=True)
    for item in st.session_state.history[::-1][:10]:
        st.write(f" - {item}")
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("Clear History"):
        st.session_state.history = []
        st.success("Conversion history cleared!")
else:
    st.write("No conversions yet.") 

if category == "Currency":
    if st.button("Refresh Currency Rates"):
        currency_rates = fetch_currency_rates()
        st.success("Currency rates updated!")
