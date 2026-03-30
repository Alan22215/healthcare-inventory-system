data = {
    "Drug A": [3000, 2800, 3200],
    "Drug B": [500, 600, 550]
}

stock = {
    "Drug A": 600,
    "Drug B": 700
}

def forecast(values):
    return 0.5*values[-1] + 0.3*values[-2] + 0.2*values[-3]

def reorder_level(f):
    return (f / 30) * 7

def generate_po(f, stock):
    safety = 0.2 * f
    required = f + safety
    return max(0, required - stock)

for item in data:
    f = forecast(data[item])
    r = reorder_level(f)
    po = generate_po(f, stock[item])

    print(f"Item: {item}")
    print(f"Forecast: {f}")
    print(f"Reorder Level: {r}")
    print(f"PO Quantity: {po}")
    print("-----")
