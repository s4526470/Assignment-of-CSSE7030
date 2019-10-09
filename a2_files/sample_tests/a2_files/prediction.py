"""
    Prediction model classes used in the second assignment for CSSE1001/7030.

    WeatherPrediction: Defines the super class for all weather prediction models.
    YesterdaysWeather: Predict weather to be similar to yesterday's weather.
"""

__author__ = ""
__email__ = ""

from weather_data import WeatherData


class WeatherPrediction(object):
    """Superclass for all of the different weather prediction models."""

    def __init__(self, weather_data):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        self._weather_data = weather_data

    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        raise NotImplementedError

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        raise NotImplementedError

    def high_temperature(self):
        """(float) Expected high temperature."""
        raise NotImplementedError

    def low_temperature(self):
        """(float) Expected low temperature."""
        raise NotImplementedError

    def humidity(self):
        """(int) Expected humidity."""
        raise NotImplementedError

    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        raise NotImplementedError

    def wind_speed(self):
        """(int) Expected average wind speed."""
        raise NotImplementedError


class YesterdaysWeather(WeatherPrediction):
    """Simple prediction model, based on yesterday's weather."""

    def __init__(self, weather_data):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data)
        self._yesterdays_weather = self._weather_data.get_data(1)
        self._yesterdays_weather = self._yesterdays_weather[0]

    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        return 1

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        # Amount of yesterday's rain indicating chance of it occurring.
        NO_RAIN = 0.1
        LITTLE_RAIN = 3
        SOME_RAIN = 8
        # Chance of rain occurring.
        NONE = 0
        MILD = 40
        PROBABLE = 75
        LIKELY = 90

        if self._yesterdays_weather.get_rainfall() < NO_RAIN:
            chance_of_rain = NONE
        elif self._yesterdays_weather.get_rainfall() < LITTLE_RAIN:
            chance_of_rain = MILD
        elif self._yesterdays_weather.get_rainfall() < SOME_RAIN:
            chance_of_rain = PROBABLE
        else:
            chance_of_rain = LIKELY

        return chance_of_rain

    def high_temperature(self):
        """(float) Expected high temperature."""
        return self._yesterdays_weather.get_high_temperature()

    def low_temperature(self):
        """(float) Expected low temperature."""
        return self._yesterdays_weather.get_low_temperature()

    def humidity(self):
        """(int) Expected humidity."""
        return self._yesterdays_weather.get_humidity()

    def wind_speed(self):
        """(int) Expected average wind speed."""
        return self._yesterdays_weather.get_average_wind_speed()

    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        return self._yesterdays_weather.get_cloud_cover()


# Your implementations of the SimplePrediction and SophisticatedPrediction
# classes should go here.
class SimplePrediction(WeatherPrediction) :

    def __init__(self, weather_data, number_of_days) :

        super().__init__(weather_data)
        self._number_of_days = number_of_days
        if self._number_of_days < 28 :
            self._days_weather = self._weather_data.get_data(self._number_of_days)
        else :
            self._days_weather = self._weather_data.get_data(28)

    def get_number_days(self) :
        if self._number_of_days < 28 :
            return self._number_of_days

        return 28

    def chance_of_rain(self):
        total_rainfall = 0
        for day in self._days_weather :
            total_rainfall += day.get_rainfall()

        result = (total_rainfall / self._number_of_days) * 9

        if result > 100 :
            return 100

        return int(round(result)) #记得重命名result

    def high_temperature(self) :
        hightest_temperature = self._days_weather[0].get_high_temperature()
        for day in self._days_weather :
            high_temperature = day.get_high_temperature()
            if high_temperature > hightest_temperature :
                hightest_temperature = high_temperature

        return hightest_temperature

    def low_temperature(self) :
        lowest_temperature = self._days_weather[0].get_low_temperature()
        for day in self._days_weather :
            low_temperature = day.get_low_temperature()
            if low_temperature < lowest_temperature :
                lowest_temperature = low_temperature

        return lowest_temperature

    def humidity(self) :
        total_humidity = 0
        for day in self._days_weather :
            total_humidity += day.get_humidity()

        result = total_humidity / self._number_of_days
        return int(result) #记得重命名result

    def cloud_cover(self) :
        total_cloud_cover = 0
        for day in self._days_weather :
            total_cloud_cover += day.get_cloud_cover()

        result = total_cloud_cover / self._number_of_days
        return int(round(result)) #记得重命名result

    def wind_speed(self) :
        total_wind_speed = 0
        for day in self._days_weather :
            total_wind_speed += day.get_average_wind_speed()

        result = total_wind_speed / self._number_of_days
        return int(round(result)) #记得重命名result
    # 2019.4.22 10.17PM 编辑


class SophisticatedPrediction(WeatherPrediction) :
    def __init__(self, weather_data, number_of_days) :

        super().__init__(weather_data)
        self._number_of_days = number_of_days
        if self._number_of_days < 28 :
            self._days_weather = self._weather_data.get_data(self._number_of_days)
        else :
            self._days_weather = self._weather_data.get_data(28)

    def get_number_days(self) :
        if self._number_of_days < 28 :
            return self._number_of_days

        return 28

    def chance_of_rain(self) :
        total_air_pressure = 0
        total_rainfall = 0
        result = 0
        yesterday_air_pressure = self._days_weather[self._number_of_days - 1].get_air_pressure()
        yesterday_wind_direction = self._days_weather[self._number_of_days - 1].get_wind_direction()
        easterly_point = ["NNE", "NE", "ENE", "E", "ESE", "SE", "SSE"]
        
        for day in self._days_weather :
            total_air_pressure += day.get_air_pressure()
            total_rainfall += day.get_rainfall()
            
        average_air_pressure = total_air_pressure / self._number_of_days
        average_rainfall = total_rainfall / self._number_of_days
        

        if yesterday_air_pressure < average_air_pressure :
            result = average_rainfall * 10
        else :
            result = average_rainfall * 7

        if yesterday_wind_direction in easterly_point :
            result *= 1.2

        if result > 100 :
            return 100
        else :
            return int(round(result))

    def high_temperature(self) :
        total_high_temperature = 0
        total_air_pressure = 0
        yesterday_air_pressure = self._days_weather[self._number_of_days - 1].get_air_pressure()
        result = 0
        
        for day in self._days_weather :
            total_high_temperature += day.get_high_temperature()
            total_air_pressure += day.get_air_pressure()

        average_high_temperature = total_high_temperature / self._number_of_days
        average_air_pressure = total_air_pressure / self._number_of_days

        if yesterday_air_pressure > average_air_pressure :
            result = average_high_temperature + 2
            return result

        return average_high_temperature
            
        
    def low_temperature(self) :
        total_low_temperature = 0
        total_air_pressure = 0
        yesterday_air_pressure = self._days_weather[self._number_of_days - 1].get_air_pressure()
        result = 0
        
        for day in self._days_weather :
            total_low_temperature += day.get_low_temperature()
            total_air_pressure += day.get_air_pressure()

        average_low_temperature = total_low_temperature / self._number_of_days
        average_air_pressure = total_air_pressure / self._number_of_days

        if yesterday_air_pressure < average_air_pressure :
            result = average_low_temperature - 2
            return result
        
        return average_low_temperature
        
    def humidity(self) :
        total_humidity = 0
        total_air_pressure = 0
        yesterday_air_pressure = self._days_weather[self._number_of_days - 1].get_air_pressure()
        result = 0

        for day in self._days_weather :
            total_humidity += day.get_humidity()
            total_air_pressure += day.get_air_pressure()

        average_humidity = total_humidity / self._number_of_days
        average_air_pressure = total_air_pressure / self._number_of_days

        if yesterday_air_pressure < average_air_pressure :
            result = average_humidity + 15
        elif yesterday_air_pressure > average_air_pressure :
            result = average_humidity - 15
        else :
            result = average_humidity

        if result > 100 :
            return 100
        elif result < 0 :
            return 0
        else :
            return int(round(result))
        
        

    def cloud_cover(self) :
        total_cloud_cover = 0
        total_air_pressure = 0
        yesterday_air_pressure = self._days_weather[self._number_of_days - 1].get_air_pressure()
        

        for day in self._days_weather :
            total_cloud_cover += day.get_cloud_cover()
            total_air_pressure += day.get_air_pressure()

        average_cloud_cover = total_cloud_cover / self._number_of_days
        average_air_pressure = total_air_pressure / self._number_of_days

        if yesterday_air_pressure < average_air_pressure :
            average_cloud_cover = average_cloud_cover + 2

        if average_cloud_cover > 9 :
            return 9
        
        return int(round(average_cloud_cover))
    
    def wind_speed(self) :
        total_wind_speed = 0
        yesterday_max_wind_speed = self._days_weather[self._number_of_days - 1].get_maximum_wind_speed()
        
        for day in self._days_weather :
            total_wind_speed += day.get_average_wind_speed()

        average_wind_speed = total_wind_speed / self._number_of_days

        if yesterday_max_wind_speed > 4 * average_wind_speed :
            average_wind_speed *= 1.2

        return int(round(average_wind_speed)) # 2019.4.22 11.29PM 编辑
        
        


if __name__ == "__main__":
    print("This module provides the weather prediction models",
          "and is not meant to be executed on its own.")
