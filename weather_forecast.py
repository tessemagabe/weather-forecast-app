# 11.1 Final Class Project

"""
Purpose:
        This project: create a weather application that interacts
        with the OpenWeatherMap web service to retrieve weather data.

        The program will use all the information learned in the class  to create
        a Python application to perform a geolocation lookup, connect
        to a weather app, retrieve info, process JSON data, and display it in
        a readable format.

Program: MY Weather Lookup Application
Author:  Gabe
Course:  DSC510 - Introduction to Programming
Assignment: 11.1 Final Class Project
Presented: Professor Michael Eller
DSC510-T301
Date: 11/21/2026
"""
import requests


API_KEY = "YOUR_API_KEY"

class WeatherForecast:
    def __init__(self, api_key):
        self.api_key = api_key

    #def get_weather_data(self):
    def weather_lookup(self):
        """ OpenWeatherMap requires information, as indicated in the input in build function,
            but a state code alone (eg. VA or CA) does not return reliable weather results."""

        while True:
            location = input(
                "\nPlease enter a city, city and state (e.g. Falls Church, VA), or a ZIP code: "
            ).strip()

            #Input validation for empty input
            if location:
                break
            print("-" * 50)
            print("Error: Location cannot be empty. Please try again.")
            print("-" * 50)


        # First API call: GEO Lookup
        if location.isdigit():
            geo_url = (
                f"https://api.openweathermap.org/geo/1.0/zip"
                f"?zip={location},US&appid={self.api_key}"
            )
            try:
                geo_response = requests.get(geo_url, timeout=10)
                geo_response.raise_for_status()
                geo_data = geo_response.json()
                #print(geo_data)  # debug
            except requests.exceptions.HTTPError as err:
                print(
                    f"HTTP error occurred during ZIP lookup: {err}. Please check your ZIP code."
                )
                return {"cod": 404}, ""
            except requests.exceptions.ConnectionError:
                print(
                    "Network connection error. Please check your internet connection."
                )
                return {"cod": 503}, ""
            except requests.exceptions.Timeout:
                print("The request timed out. Please try again later.")
                return {"cod": 504}, ""
            except requests.exceptions.RequestException as err:
                print(f"An unexpected error occurred: {err}")
                return {"cod": 404}, ""

            if not geo_data or "lat" not in geo_data:
                return {"cod": 404}, ""

            location_name = geo_data.get("name", "")
            lat = geo_data["lat"]
            lon = geo_data["lon"]
        else:
            # Validate that the user included a state for city lookups
            if "," not in location:
                print("Error: Please include a state code (e.g., Falls Church, VA) to get the precise result.")
                return {"cod": 404}, ""

            geo_url = (
                f"https://api.openweathermap.org/geo/1.0/direct"
                f"?q={location},US&limit=1&appid={self.api_key}"
            )
            try:
                geo_response = requests.get(geo_url, timeout=10)
                geo_response.raise_for_status()
                geo_data = geo_response.json()
            except requests.exceptions.HTTPError as err:
                print(
                    f"HTTP error occurred during city lookup: {err}. Please check your city name."
                )
                return {"cod": 404}, ""
            except requests.exceptions.ConnectionError:
                print(
                    "Network connection error. Please check your internet connection."
                )
                return {"cod": 503}, ""
            except requests.exceptions.Timeout:
                print("The request timed out. Please try again later.")
                return {"cod": 504}, ""
            except requests.exceptions.RequestException as err:
                print(f"An unexpected error occurred: {err}")
                return {"cod": 404}, ""

            if not geo_data:
                return {"cod": 404}, ""

            location_name = geo_data[0].get("name", "")
            lat = geo_data[0]["lat"]
            lon = geo_data[0]["lon"]

        # Second API call: Weather using lat/lon
        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={self.api_key}&units=imperial"
        )
        try:
            response = requests.get(weather_url, timeout=10)
            response.raise_for_status()
            return response.json(), location_name
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred retrieving weather: {err}.")
            return {"cod": 404}, ""
        except requests.exceptions.ConnectionError:
            print("Unable to connect to the weather service server.")
            return {"cod": 503}, ""
        except requests.exceptions.Timeout:
            print("Weather request timed out.")
            return {"cod": 504}, ""
        except requests.exceptions.RequestException:
            print("Unable to retrieve weather information.")
            return {"cod": 404}, ""

    def open_weather(self):
        while True:
            weather_data, location_name = self.weather_lookup()

            if weather_data.get("cod") != 200:
                print("Location not found. Please try again.")
                continue

            print(f"""
            City: {location_name}
            Country: {weather_data['sys']['country']}
            Temperature: {weather_data['main']['temp']}°F
            High Temperature: {weather_data['main']['temp_max']}°F
            Low Temperature: {weather_data['main']['temp_min']}°F
            Pressure: {weather_data['main']['pressure']} hPa
            Cloud Coverage: {weather_data['clouds']['all']}%
            Humidity: {weather_data['main']['humidity']}%
            Conditions: {weather_data['weather'][0]['description']}
            """)

            while True:

                again = input("\nWould you like to continue (y/n)? ").strip().lower()

                if again == "y":
                    break

                elif again == "n":
                    print("\n" + "-" * 50)
                    print("Thank you for using my Application. Have a good one")
                    print("-" * 50)
                    return
                else:
                    print("\n" + "-" * 50)
                    print("Please enter only [y] for yes or [n] for no.")
                    print("-" * 50)


def main():
    print("=" * 50)
    print("WEATHER LOOKUP APPLICATION")
    print("=" * 50)
    app = WeatherForecast(API_KEY)
    app.open_weather()



if __name__ == "__main__":
    main()


