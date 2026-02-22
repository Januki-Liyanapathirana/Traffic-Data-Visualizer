#Author: Januki udana Liyanapathirana
#Date: 12/9/2024
#Student ID: 20241272


import csv
import tkinter as tk
from collections import defaultdict

# Task A
def validate_date_input():
    while True:
        try:
            # Getting input for the day
            day = input("Please enter the day of the survey in the format dd: ")
            if not day.isdigit():
                print("Integer required")
                continue
            day = int(day)
            if day < 1 or day > 31:
                print("Out of range - values must be in the range 1 and 31.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for the day.")

    while True:
        try:
            # Getting input for the month
            month = input("Please enter the month of the survey in the format mm: ")
            if not month.isdigit():
                print("Integer required")
                continue
            month = int(month)
            if month < 1 or month > 12:
                print("Out of range - values must be in the range 1 to 12.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for the month.")

    while True:
        try:
            # Getting input for the year
            year = input("Please enter the year of the survey in the format yyyy: ")
            if not year.isdigit():
                print("Integer required")
                continue
            year = int(year)
            if year < 2000 or year > 2024:
                print("Out of range - values must range from 2000 and 2024.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for the year.")

    return f"{day:02}/{month:02}/{year}"

# Task B
file_paths = [
    r"C:\Users\Januki\Desktop\SD1\coursework\traffic_data15062024.csv",
    r"C:\Users\Januki\Desktop\SD1\coursework\traffic_data16062024.csv",
    r"C:\Users\Januki\Desktop\SD1\coursework\traffic_data21062024.csv"
]

def process_csv_data(file_paths):
    outcomes_by_date = {}
    available_dates = []

    try:
        for file_path in file_paths:
            with open(file_path, mode='r') as csvfile:
                reader = csv.DictReader(csvfile)
                date_str = file_path.split("\\")[-1].replace("traffic_data", "").replace(".csv", "")
                formatted_date = f"{date_str[:2]}/{date_str[2:4]}/{date_str[4:]}"

                if formatted_date not in available_dates:
                    available_dates.append(formatted_date)

                if formatted_date not in outcomes_by_date:
                    outcomes_by_date[formatted_date] = {
                        "total_vehicles": 0,
                        "total_trucks": 0,
                        "total_electric_vehicles": 0,
                        "two_wheeled_vehicles": 0,
                        "buses_north_elm": 0,
                        "straight_vehicles": 0,
                        "trucks_percentage": 0,
                        "avg_bicycles_per_hour": 0,
                        "over_speed_limit": 0,
                        "vehicles_elm_only": 0,
                        "vehicles_hanley_only": 0,
                        "scooters_percentage_elm": 0,
                        "scooters_elm": 0,
                        "peak_vehicles_hanley": 0,
                        "peak_hours_hanley": defaultdict(int),  
                        "rainy_hours": set(),  
                        "bicycle_count": 0,
                        "bicycle_hours": set(),  
                        "vehicle_frequency_per_hour": {
                            "Elm Avenue/Rabbit Road": [0] * 24,
                            "Hanley Highway/Westway": [0] * 24
                        }
                    }

                for row in reader:
                    outcomes = outcomes_by_date[formatted_date]
                    hour = int(row["timeOfDay"].split(":")[0])
                    junction = row["JunctionName"]
                    outcomes["vehicle_frequency_per_hour"][junction][hour] += 1
                    vehicle_type = row["VehicleType"]
                    direction_in = row["travel_Direction_in"]
                    direction_out = row["travel_Direction_out"]
                    speed = int(row["VehicleSpeed"])
                    speed_limit = int(row["JunctionSpeedLimit"])
                    time_of_day = row["timeOfDay"]
                    weather = row["Weather_Conditions"]
                    
                    if vehicle_type == "Truck":
                        outcomes["total_trucks"] += 1

                    if row["elctricHybrid"].lower() == "true":
                        outcomes["total_electric_vehicles"] += 1
                        
                    if vehicle_type in ["Bicycle", "Motorcycle", "Scooter"]:
                        outcomes["two_wheeled_vehicles"] += 1
                        
                    if vehicle_type == "Bicycle":
                        outcomes["bicycle_count"] += 1
                        hour = time_of_day.split(":")[0]  
                        outcomes["bicycle_hours"].add(hour)

                    if vehicle_type == "Buss" and junction == "Elm Avenue/Rabbit Road" and direction_out == "N":
                        outcomes["buses_north_elm"] += 1
                        
                    if direction_in == direction_out:
                        outcomes["straight_vehicles"] += 1
                        
                    if speed > speed_limit:
                        outcomes["over_speed_limit"] += 1

                    if junction == "Elm Avenue/Rabbit Road":
                        outcomes["vehicles_elm_only"] += 1
                          
                    if vehicle_type == "Scooter":
                        outcomes["scooters_elm"] += 1
                            
                    if junction == "Hanley Highway/Westway":
                        outcomes["vehicles_hanley_only"] += 1
                        hour = time_of_day.split(":")[0]  
                        outcomes["peak_hours_hanley"][hour] += 1

                    if weather in ["Light Rain", "Heavy Rain"]:
                        hour = time_of_day.split(":")[0]  
                        outcomes["rainy_hours"].add(hour)
                        
        for formatted_date, outcomes in outcomes_by_date.items():
            if outcomes["total_vehicles"] > 0:  
                outcomes["trucks_percentage"] = (outcomes["total_trucks"] / outcomes["total_vehicles"]) * 100

            if outcomes["bicycle_hours"]:
                outcomes["avg_bicycles_per_hour"] = outcomes["bicycle_count"] / len(outcomes["bicycle_hours"])

            if outcomes["vehicles_elm_only"] > 0:  
                outcomes["scooters_percentage_elm"] = (outcomes["scooters_elm"] / outcomes["vehicles_elm_only"]) * 100
                
            if junction == "Elm Avenue/Rabbit Road":
                outcomes["vehicle_frequency_per_hour"]["Elm Avenue/Rabbit Road"][hour] += 1
            elif junction == "Hanley Highway/Westway":
                outcomes["vehicle_frequency_per_hour"]["Hanley Highway/Westway"][hour] += 1
    
  

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return outcomes_by_date, available_dates

def display_outcomes(outcomes, file_name):
    result_lines = []
    result_lines.append(f"Selected CSV file: {file_name}")
    result_lines.append(f"The total number of vehicles recorded for this date is {outcomes['total_vehicles']}")
    result_lines.append(f"The total number of trucks recorded for this date is {outcomes['total_trucks']}")
    result_lines.append(f"The total number of electric vehicles recorded for this date is {outcomes['total_electric_vehicles']}")
    result_lines.append(f"The total number of two-wheeled vehicles recorded for this date is {outcomes['two_wheeled_vehicles']}")
    result_lines.append(f"The total number of buses leaving Elm Avenue/Rabbit Road heading North is {outcomes['buses_north_elm']}")
    result_lines.append(f"The total number of vehicles passing through both junctions without turning left or right is {outcomes['straight_vehicles']}")
    result_lines.append(f"The percentage of all vehicles recorded that are trucks for the selected date is {outcomes['trucks_percentage']}%")
    result_lines.append(f"The average number of bicycles per hour for this date is {outcomes['avg_bicycles_per_hour']}")
    result_lines.append(f"The total number of vehicles recorded as over the speed limit for this date is {outcomes['over_speed_limit']}")
    result_lines.append(f"The total number of vehicles recorded through only Elm Avenue/Rabbit Road junction is {outcomes['vehicles_elm_only']}")
    result_lines.append(f"The total number of vehicles recorded through only Hanley Highway/Westway junction is {outcomes['vehicles_hanley_only']}")
    result_lines.append(f"The percentage of vehicles through Elm Avenue/Rabbit Road that are scooters is {outcomes['scooters_percentage_elm']}%")
    
    peak_hour = max(outcomes['peak_hours_hanley'], key=outcomes['peak_hours_hanley'].get) 
    result_lines.append(f"The number of vehicles recorded in the peak (busiest) hour on Hanley Highway/Westway is {outcomes['peak_hours_hanley'][peak_hour]}")
    result_lines.append(f"The peak traffic hour(s) on Hanley Highway/Westway: {peak_hour}:00")
    result_lines.append(f"The total number of hours of rain for this date is {len(outcomes['rainy_hours'])}")
    result_lines.append("\n********************************************************")

    print("\n".join(result_lines))
    return result_lines

#Task C 
def save_results_to_file(results_list):
    with open("results.txt", "w") as file:
        for result in results_list:
            file.write(result + "\n")
    print("Results saved to results.txt")


# Task D
class HistogramApp:
    def __init__(self, traffic_data, date):
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.canvas = None

    def setup_window(self):
        formatted_date = f"{self.date[0:2]}/{self.date[2:4]}/{self.date[4:]}"
        self.root.title(f"Histogram of Vehicle Frequency per Hour ({formatted_date})")
        self.canvas = tk.Canvas(self.root, width=1200, height=600, bg="white")
        self.canvas.pack(padx=20, pady=20)

    def draw_histogram(self):
        max_frequency = max(max(freqs) for freqs in self.traffic_data.values())
        bar_width = 18
        group_spacing = 8
        x_offset = 80
        y_offset = 500
        y_scale = 400 / max_frequency

        # Draw axes
        self.canvas.create_line(x_offset, y_offset, x_offset + 24 * (2 * bar_width + group_spacing), y_offset)
        self.canvas.create_line(x_offset, y_offset, x_offset, y_offset - 450)

        for i in range(24):
            x = x_offset + i * (2 * bar_width + group_spacing)
            self.canvas.create_text(x + bar_width, y_offset + 15, text=f"{i:02d}", font=("Arial", 10))
            self.canvas.create_line(x, y_offset, x, 50, fill="#EEEEEE")

        colors = {
            "Elm Avenue/Rabbit Road": "#FF0000",  
            "Hanley Highway/Westway": "#02590F"   
        }

        # Draw bars
        for hour in range(24):
            x_group_start = x_offset + hour * (2 * bar_width + group_spacing)
            for i, (junction, hourly_data) in enumerate(self.traffic_data.items()):
                count = hourly_data[hour]
                x_bar_start = x_group_start + i * bar_width
                y_bar_top = y_offset - (count * y_scale)
                self.canvas.create_rectangle(
                    x_bar_start, y_bar_top,
                    x_bar_start + bar_width, y_offset,
                    fill=colors[junction],
                    outline="#333333"
                )
                if count > 0:
                    self.canvas.create_text(
                        x_bar_start + bar_width/2,
                        y_bar_top - 8,
                        text=str(count),
                        font=("Arial", 9)
                    )

        # Add x-axis label
        self.canvas.create_text(
            x_offset + 24 * (2 * bar_width + group_spacing) / 2,
            y_offset + 40,
            text="Hours 00:00 to 24:00",
            font=("Arial", 12)
        )

        # Adding legend
        legend_y = 30
        for i, (junction, color) in enumerate(colors.items()):
            x_rect = x_offset + i * 300
            self.canvas.create_rectangle(x_rect, legend_y, x_rect + 20, legend_y + 20,
                                      fill=color, outline="#333333")
            self.canvas.create_text(x_rect + 30, legend_y + 10,
                                  text=junction, anchor="w", font=("Arial", 11))

    def run(self):
        self.setup_window()
        self.draw_histogram()
        self.root.mainloop()
#Task E
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.outcomes_by_date = {}
        self.available_dates = []
        self.current_data = None
        self.file_paths = [
            r"C:\Users\Januki\Desktop\SD1\coursework\traffic_data15062024.csv",
            r"C:\Users\Januki\Desktop\SD1\coursework\traffic_data16062024.csv",
            r"C:\Users\Januki\Desktop\SD1\coursework\traffic_data21062024.csv"
        ]

    def load_csv_file(self, file_paths):
        """
        Loads CSV files and processes their data.
        """
        self.outcomes_by_date, self.available_dates = process_csv_data(file_paths)
        
    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None
        
    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        while True:
            user_date = validate_date_input()
            
            if user_date not in self.available_dates:
                print(f"No data available for the selected date: {user_date}")
                continue
                
            self.current_data = self.outcomes_by_date[user_date]
            result_lines = display_outcomes(self.current_data, user_date)
            save_results_to_file(result_lines)

            # Display Histogram
            hourly_data = self.current_data["vehicle_frequency_per_hour"]
            app = HistogramApp(hourly_data, user_date)
            app.run()

            # Ask if the user wants to process another dataset
            while True:
                choice = input("Do you want to select another data file for a different date? Y/N > ").strip().lower()
                if choice in ['y', 'n']:
                    break
                print('Please enter "Y" or "N".')
            
            if choice == 'n':
                print("End of run")
                return False
            elif choice == 'y':
                self.clear_previous_data()
                return True

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        self.load_csv_file(self.file_paths)
        
        while True:
            continue_processing = self.handle_user_interaction()
            if not continue_processing:
                break

if __name__ == "__main__":
    processor = MultiCSVProcessor()
    processor.process_files()