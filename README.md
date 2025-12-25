**Electricity Cost Calculator** is a simple desktop app built with Python and Tkinter that helps you calculate the electricity cost of any device.

**Features**

--Enter either total power (W) or device voltage and current

--Include adapter efficiency to account for energy losses

--Calculate electricity cost per day, month, or year

--Customizable electricity price (NOK or any other currency)

--Friendly GUI for quick calculations

**Installation**
1. Clone or download the repository from GitHub: click Code → Download ZIP on GitHub.
2. Install Python (if not already installed): Make sure to check “Add Python to PATH” during installation.
3. Install required packages (if any): pip install tk (Tkinter is usually included with Python, so often no extra packages are needed.)
4. Create a standalone executable (.exe) on Windows:
   
   --Install PyInstaller: pip install pyinstaller.
   
   --Navigate to your project folder in the terminal/command prompt: cd path\to\Electricity-Cost-Calculator
   
   --Create a single executable: pyinstaller --onefile main.py

**Usage**

1. Enter the device information (ususally found on the charger or adapter) and the electricity price.  
2. If "total power consumption" is listed on the device, it is recommended to use it. Voltage/current field will be deactivated. 
3. If a field has a default value and you wish to keep it, you can leave it empty.  
4. Click **Calculate** to see the electricity cost.  
5. Choose between daily, monthly, or yearly cost for the results.

![App Screenshot](assets/appscreen.png)

**About**

This app is perfect for homeowners, hobbyists, or anyone who wants to track and reduce energy costs.
