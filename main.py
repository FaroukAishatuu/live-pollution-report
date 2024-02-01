# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification

import sys
import monitoring
import reporting
import datetime

def main_menu():
    """
    Displays the main menu and handles user input to navigate between different modules of the application.

    The function provides options for accessing the PR module, RM module, printing the About text, and quitting the
    application. It prompts the user for input and executes the corresponding functionality based on the chosen option.

    Returns:
        None
    """
    while True:
        print("Main Menu:")
        print("R - PR module")
        print("M - RM module")
        print("A - About the ACQUA System")
        print("Q - Quit the application")
        
        choice = input("Choose an option: ").upper()
        
        if choice == "R":
            reporting_menu()
        elif choice == "M":
            monitoring_menu()
        elif choice == "A":
            about()
        elif choice == "Q":
            quit()
        else:
            print("Invalid choice. Please try again.")

def reporting_menu():
    """
    Displays the reporting menu and handles user input for generating pollution reports.

    The function guides the user through different menu levels to select the monitoring station, pollutant, and type
    of report. It then calls the appropriate reporting functions based on the user's selections.

    Returns:
        None
    """
    menu_level = 1
    monitoring_station = ''
    pollutant = ''
    data = reporting.read_csv_files()
    while True:
        if menu_level == 1:
            print("Monitoring Station:")
            print("1 - London Marylebone Road")
            print("2 - London N Kensington")
            print("3 - London Harlington")
            print("Q - Back to Main Menu")
            choice = input("Choose an option: ").upper()
            if choice == '1':
                monitoring_station = 'MY1'
                menu_level = 2
            elif choice == '2':
                monitoring_station = 'KC1'
                menu_level = 2
            elif choice == '3':
                monitoring_station = 'HRL'
                menu_level = 2
            elif choice == 'Q':
                break
            else:
                print("Invalid option. Please try again.")
        
        elif menu_level == 2:
            print("Pollutant:")
            print("1 - Nitrogen Monoxide (NO)")
            print("2 - PM10")
            print("3 - PM2.5")
            print("Q - Back to Monitoring Station Menu")
            choice2 = input("Choose an option: ").upper()
            if choice2 == '1':
                pollutant = 'no'
                menu_level = 3
            elif choice2 == '2':
                pollutant = 'pm10'
                menu_level = 3
            elif choice2 == '3':
                pollutant = 'pm25'
                menu_level = 3
            elif choice2 == 'Q':
                menu_level = 1
            else:
                print("Invalid option. Please try again.")
        
        elif menu_level == 3:
            print("Report:")
            print("1 - Hourly Pollution Levels")
            print("2 - Daily Pollution Levels")
            print("3 - Monthly Average Pollution Levels")
            print("4 - Weekly Average Pollution Levels")
            print("5 - Day of the Week Average Pollution Levels")
            print("Q - Back to Pollutant Menu")
            choice3 = input("Choose an option: ").upper()
            if choice3 == '1':
                menu_level = 4
            elif choice3 == '2':
                menu_level = 5
            elif choice3 == '3':
                monthly_averages = reporting.monthly_average(data, monitoring_station, pollutant)
                for average in monthly_averages:
                    print(average)
                input(">>> Press Enter to return to Report Menu...")
            elif choice3 == '4':
                weekly_averages = reporting.weekly_average(data, monitoring_station, pollutant)
                for average in weekly_averages:
                    print(average)
                input(">>> Press Enter to return to Report Menu...")
            elif choice3 == '5':
                day_of_week_averages = reporting.day_of_week_average(data, monitoring_station, pollutant)
                for average in day_of_week_averages:
                    print(average)
                input(">>> Press Enter to return to Report Menu...")
            elif choice3 == 'Q':
                menu_level = 2
            else:
                print("Invalid option. Please try again.")

        elif menu_level == 4:
            print("Hourly Report:")
            print("1 - Hourly Average Pollution Levels")
            print("2 - Highest Pollution Hour")
            print("Q - Back to Report Menu")
            choice4 = input("Choose an option: ").upper()
            if choice4 == '1':
                hourly_averages = reporting.hourly_average(data, monitoring_station, pollutant)
                for average in hourly_averages:
                    print(average)
                input(">>> Press Enter to return to Hourly Report Menu...")
            elif choice4 == '2':
                while True:
                    choice5 = input("Enter a date (YYYY-MM-DD): ")

                    try:
                        chosen_date = datetime.datetime.strptime(choice5, "%Y-%m-%d").date()
                        start_date = datetime.date(2021, 1, 1)
                        end_date = datetime.date(2021, 12, 31)

                        if start_date <= chosen_date <= end_date:
                            peak = reporting.peak_hour_date(data, choice5, monitoring_station, pollutant)
                            print(peak)
                            input(">>> Press Enter to return to Hourly Report Menu...")
                            break  # Exit the loop after successful processing
                        else:
                            print("Invalid date! Please enter a date between 2021-01-01 and 2021-12-31.")
                    except ValueError:
                        print("Invalid date format! Please enter the date in the format YYYY-MM-DD.")
            elif choice4 == 'Q':
                menu_level = 3
            else:
                print("Invalid option. Please try again.")

        elif menu_level == 5:
            print("Daily Report:")
            print("1 - Daily Average Pollution Levels")
            print("2 - Daily Median Pollution Levels")
            print("Q - Back to Report Menu")
            choice4 = input("Choose an option: ").upper()
            if choice4 == '1':
                daily_averages = reporting.daily_average(data, monitoring_station, pollutant)
                for average in daily_averages:
                    print(average)
                input(">>> Press Enter to return to Daily Report Menu...")
            elif choice4 == '2':
                daily_medians = reporting.daily_median(data, monitoring_station, pollutant)
                for average in daily_medians:
                    print(average)
                input(">>> Press Enter to return to Daily Report Menu...")
            elif choice4 == 'Q':
                menu_level = 3
            else:
                print("Invalid option. Please try again.")


def monitoring_menu():
    """
    Displays the monitoring menu and handles user input to navigate between different monitoring-related functionalities.

    The function presents a list of available options related to monitoring, such as real-time statistics, highest
    pollutant value in the last 7 days, pollutant statistics retrieval and calculation, pollutant comparison, and air
    quality index. It prompts the user for input and executes the corresponding functionality based on the chosen option.

    Returns:
        None
    """
    while True:
        print("Monitoring Menu:")
        print("1 - Real-time Statistics for a Monitoring Station and Pollutant")
        print("2 - Highest Pollutant Value in Last 7 Days")
        print("3 - Retrieve and Calculate Pollutant Statistics for a Monitoring Station")
        print("4 - Pollutant Comparison")
        print("5 - Air Quality Index")
        print("Q - Back to Main Menu")
        
        choice = input("Choose an option: ").upper()
        
        if choice == "1":
            monitoring.display_real_time_statistics()
            input(">>> Press Enter to return to the Monitoring Menu...")
        elif choice == "2":
            monitoring.get_highest_pollutant_value()
            input(">>> Press Enter to return to the Monitoring Menu...")
        elif choice == "3":
            monitoring.get_pollutant_statistics()
            input(">>> Press Enter to return to the Monitoring Menu...")
        elif choice == "4":
            monitoring.compare_pollutant_levels()
            input(">>> Press Enter to return to the Monitoring Menu...")
        elif choice == "5":
            monitoring.get_air_quality_data()
            input(">>> Press Enter to return to the Monitoring Menu...")
        elif choice == "Q":
            break  # Return to main menu

def about():
    """
    Displays information about the ACQUA System, including the module code and exam number.

    The function prints the module code (ECM1400) and my exam number (068351) to the console. It then waits for
    the user to press Enter before returning to the main menu.

    Returns:
        None
    """
    print("ACQUA System")
    print("Module code: ECM1400")
    print("Exam number: 068351")
    input(">>> Press Enter to return to the main menu.")

def quit():
    """
    Exits the program.

    The function prints a message indicating that the program is exiting and then terminates the program.

    Returns:
        None
    """
    print("Exiting the program.")
    sys.exit()




if __name__ == '__main__':
    main_menu()
