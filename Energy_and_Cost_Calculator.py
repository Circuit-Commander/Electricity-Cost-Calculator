import tkinter as tk
from tkinter import messagebox

MAX_DEVICE_VOLTAGE = 12.0
DEFAULT_EFFICIENCY = 0.85


def toggle_voltage_current(event=None):
    if power_entry.get().strip():
        voltage_entry.config(state="disabled")
        current_entry.config(state="disabled")
    else:
        voltage_entry.config(state="normal")
        current_entry.config(state="normal")


def calculate():
    voltage_entry.config(bg="white")

    # --- Read voltage early for warning ---
    voltage_value = None
    if voltage_entry.get():
        try:
            voltage_value = float(voltage_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Voltage must be a number.")
            return

        if voltage_value > MAX_DEVICE_VOLTAGE:
            voltage_entry.config(bg="#ffcccc")
            proceed = messagebox.askyesno(
                "Possible Adapter Voltage",
                f"You entered {voltage_value} V.\n\n"
                "For small devices, the device voltage is usually 1–12 V.\n"
                "This may be the adapter voltage.\n\n"
                "Do you want to continue using this value?"
            )
            if not proceed:
                return

    # --- Required fields ---
    try:
        # Check if the entry is empty; if so, default to 24
        hours_input = hours_entry.get().strip()
        hours = float(hours_input) if hours_input else 24.0
        price_per_kwh = float(price_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for hours and price.")
        return

    period = period_var.get()

    # --- Power calculation ---
    power_w = None

    if power_entry.get().strip():
        try:
            power_w = float(power_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Total power must be a number.")
            return
    else:
        if not (voltage_entry.get() and current_entry.get()):
            messagebox.showerror(
                "Input Error",
                "Enter either Total Power (W)\n"
                "or Device Voltage and Current."
            )
            return
        try:
            current = float(current_entry.get())
            current_a = current / 1000 if current_unit.get() == "mA" else current
            power_w = voltage_value * current_a
        except ValueError:
            messagebox.showerror("Input Error", "Current must be a number.")
            return

    # --- Adapter efficiency ---
    try:
        efficiency = (
            float(efficiency_entry.get()) / 100
            if efficiency_entry.get().strip()
            else DEFAULT_EFFICIENCY
        )
    except ValueError:
        messagebox.showerror("Input Error", "Efficiency must be a number.")
        return

    if not (0 < efficiency <= 1):
        messagebox.showerror("Input Error", "Efficiency must be between 0 and 100%.")
        return

    include_adapter = adapter_var.get()

    if include_adapter:
        total_power = power_w / efficiency
        loss_power = total_power - power_w
    else:
        total_power = power_w
        loss_power = 0

    # --- Cost calculation ---
    energy_day = total_power * hours / 1000
    cost_day = energy_day * price_per_kwh
    cost_month = cost_day * 30
    cost_year = cost_day * 365

    loss_cost_day = loss_power * hours / 1000 * price_per_kwh
    loss_cost_month = loss_cost_day * 30
    loss_cost_year = loss_cost_day * 365

    # --- Output ---
    if period == "day":
        result = f"Electricity cost per day: {cost_day:.2f} NOK"
        if include_adapter:
            result += f"\nAdapter loss per day: {loss_cost_day:.2f} NOK"
    elif period == "month":
        result = f"Electricity cost per month: {cost_month:.2f} NOK"
        if include_adapter:
            result += f"\nAdapter loss per month: {loss_cost_month:.2f} NOK"
    else:
        result = f"Electricity cost per year: {cost_year:.2f} NOK"
        if include_adapter:
            result += f"\nAdapter loss per year: {loss_cost_year:.2f} NOK"

    result_text.set(result)


# ---------------- GUI ----------------
root = tk.Tk()
root.title("Electricity Cost Calculator")

tk.Label(root, text="Total Power (W): (Optional)").grid(row=0, column=0, sticky="e")
power_entry = tk.Entry(root)
power_entry.grid(row=0, column=1)
power_entry.bind("<KeyRelease>", toggle_voltage_current)

tk.Label(root, text="Device Voltage (V):").grid(row=1, column=0, sticky="e")
voltage_entry = tk.Entry(root)
voltage_entry.grid(row=1, column=1)

tk.Label(root, text="Device Current:").grid(row=2, column=0, sticky="e")
current_entry = tk.Entry(root)
current_entry.grid(row=2, column=1)

current_unit = tk.StringVar(value="mA")
tk.Radiobutton(root, text="mA", variable=current_unit, value="mA").grid(row=2, column=2)
tk.Radiobutton(root, text="A", variable=current_unit, value="A").grid(row=2, column=3)

tk.Label(root, text="Hours per day: (24 as default)").grid(row=3, column=0, sticky="e")
hours_entry = tk.Entry(root)
hours_entry.grid(row=3, column=1)

tk.Label(root, text="Price per kWh (NOK):").grid(row=4, column=0, sticky="e")
price_entry = tk.Entry(root)
price_entry.grid(row=4, column=1)

tk.Label(root, text="Include adapter loss:").grid(row=5, column=0, sticky="e")
adapter_var = tk.BooleanVar()
tk.Checkbutton(root, variable=adapter_var).grid(row=5, column=1, sticky="w")

tk.Label(root, text="Adapter efficiency (% – default 85%):").grid(row=6, column=0, sticky="e")
efficiency_entry = tk.Entry(root)
efficiency_entry.grid(row=6, column=1)

tk.Label(root, text="Show cost per:").grid(row=7, column=0, sticky="e")
period_var = tk.StringVar(value="day")
tk.Radiobutton(root, text="Day", variable=period_var, value="day").grid(row=7, column=1, sticky="w")
tk.Radiobutton(root, text="Month", variable=period_var, value="month").grid(row=7, column=2, sticky="w")
tk.Radiobutton(root, text="Year", variable=period_var, value="year").grid(row=7, column=3, sticky="w")

tk.Button(root, text="Calculate", command=calculate).grid(
    row=8, column=0, columnspan=4, pady=10
)

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, font=("Arial", 12, "bold"), justify="left").grid(
    row=9, column=0, columnspan=4
)

toggle_voltage_current()
root.mainloop()
