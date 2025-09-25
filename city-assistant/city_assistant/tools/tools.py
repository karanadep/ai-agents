import datetime
import os
import requests
from zoneinfo import ZoneInfo

def get_lat_long(city: str) -> dict:
    """Gets latitude and longitude coordinates for a specified city using geocode.maps.co API.

    Args:
        city (str): The name of the city for which to retrieve coordinates.

    Returns:
        dict: status and result with lat/long or error msg.
    """
    try:
        # Geocode.maps.co API endpoint
        url = "https://geocode.maps.co/search"
        params = {
            "q": city,
            "api_key": os.getenv("GEOCODE_MAPS_API_KEY", "")  # Optional API key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data or len(data) == 0:
            return {
                "status": "error",
                "error_message": f"No coordinates found for city: {city}",
            }
        
        # Get the first result (most relevant)
        result = data[0]
        lat = float(result["lat"])
        lon = float(result["lon"])
        
        return {
            "status": "success",
            "latitude": lat,
            "longitude": lon,
            "display_name": result.get("display_name", city),
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to fetch coordinates: {str(e)}",
        }
    except (KeyError, ValueError, IndexError) as e:
        return {
            "status": "error",
            "error_message": f"Invalid response format from geocoding API: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An unexpected error occurred: {str(e)}",
        }


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    # Get API key from environment variable
    api_key = os.getenv("PIRATE_WEATHER_API_KEY")
    
    if not api_key:
        return {
            "status": "error",
            "error_message": "Pirate Weather API key not found. Please set PIRATE_WEATHER_API_KEY environment variable.",
        }
    
    try:
        # First, get coordinates for the city
        coords_result = get_lat_long(city)
        if coords_result["status"] != "success":
            return coords_result
        
        lat = coords_result["latitude"]
        lon = coords_result["longitude"]
        display_name = coords_result.get("display_name", city)
        
        # Pirate Weather API endpoint using path parameters
        url = f"https://api.pirateweather.net/forecast/{api_key}/{lat},{lon}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract weather information from Pirate Weather API response
        current = data["currently"]
        temperature = current["temperature"]
        feels_like = current["apparentTemperature"]
        humidity = current["humidity"] * 100  # Convert to percentage
        description = current["summary"]
        wind_speed = current["windSpeed"]
        
        # Convert temperature to Fahrenheit for display
        temp_fahrenheit = (temperature * 9/5) + 32
        
        report = (
            f"The weather in {display_name} is {description} with a temperature of "
            f"{temperature:.1f}°C ({temp_fahrenheit:.1f}°F). "
            f"It feels like {feels_like:.1f}°C, with {humidity}% humidity and "
            f"wind speed of {wind_speed} m/s."
        )
        
        return {
            "status": "success",
            "report": report,
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to fetch weather data: {str(e)}",
        }
    except KeyError as e:
        return {
            "status": "error",
            "error_message": f"Invalid response format from weather API: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An unexpected error occurred: {str(e)}",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """
    # Get API key from environment variable
    api_key = os.getenv("PIRATE_WEATHER_API_KEY")
    
    if not api_key:
        return {
            "status": "error",
            "error_message": "Pirate Weather API key not found. Please set PIRATE_WEATHER_API_KEY environment variable.",
        }
    
    try:
        # First, get coordinates for the city
        coords_result = get_lat_long(city)
        if coords_result["status"] != "success":
            # If geocoding fails, fall back to the fallback method
            return _get_time_fallback(city)
        
        lat = coords_result["latitude"]
        lon = coords_result["longitude"]
        display_name = coords_result.get("display_name", city)
        
        # Get timezone from Pirate Weather API using path parameters
        url = f"https://api.pirateweather.net/forecast/{api_key}/{lat},{lon}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Get timezone from Pirate Weather API response
        timezone_name = data.get("timezone", "UTC")
        
        try:
            # Use the timezone from the API response
            tz = ZoneInfo(timezone_name)
            now = datetime.datetime.now(tz)
            report = f'The current time in {display_name} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
            return {"status": "success", "report": report}
        except Exception:
            # If timezone parsing fails, fall back to the fallback method
            return _get_time_fallback(city)
        
    except requests.exceptions.RequestException as e:
        # Fallback to a simple timezone mapping for major cities
        return _get_time_fallback(city)
    except KeyError as e:
        return {
            "status": "error",
            "error_message": f"Invalid response format from API: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An unexpected error occurred: {str(e)}",
        }


def _get_time_fallback(city: str) -> dict:
    """Fallback timezone lookup for major cities when API is unavailable.
    
    Args:
        city (str): The name of the city for which to retrieve the current time.
        
    Returns:
        dict: status and result or error msg.
    """
    # Major city timezone mapping
    city_timezones = {
        "new york": "America/New_York",
        "london": "Europe/London",
        "paris": "Europe/Paris",
        "tokyo": "Asia/Tokyo",
        "sydney": "Australia/Sydney",
        "los angeles": "America/Los_Angeles",
        "chicago": "America/Chicago",
        "denver": "America/Denver",
        "toronto": "America/Toronto",
        "vancouver": "America/Vancouver",
        "mexico city": "America/Mexico_City",
        "sao paulo": "America/Sao_Paulo",
        "buenos aires": "America/Argentina/Buenos_Aires",
        "madrid": "Europe/Madrid",
        "rome": "Europe/Rome",
        "berlin": "Europe/Berlin",
        "moscow": "Europe/Moscow",
        "dubai": "Asia/Dubai",
        "mumbai": "Asia/Kolkata",
        "singapore": "Asia/Singapore",
        "hong kong": "Asia/Hong_Kong",
        "seoul": "Asia/Seoul",
        "beijing": "Asia/Shanghai",
        "shanghai": "Asia/Shanghai",
        "melbourne": "Australia/Melbourne",
        "perth": "Australia/Perth",
        "auckland": "Pacific/Auckland",
        "honolulu": "Pacific/Honolulu",
    }
    
    city_lower = city.lower()
    
    if city_lower in city_timezones:
        try:
            tz_identifier = city_timezones[city_lower]
            tz = ZoneInfo(tz_identifier)
            now = datetime.datetime.now(tz)
            report = f'The current time in {city.title()} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
            return {"status": "success", "report": report}
        except Exception as e:
            return {
                "status": "error",
                "error_message": f"Failed to get time for {city}: {str(e)}",
            }
    else:
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have timezone information for '{city}'. Please ensure the city name is spelled correctly or try a major city.",
        }
