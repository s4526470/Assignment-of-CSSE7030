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
    """Simple prediction model, based on the average of pass n days weather."""
    def __init__(self, weather_data, number_of_days) :
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.
            number_of_days(str): use pass n day as data for prediction.
                                 If n is greater than the number of days
                                 of weather data that is available,all of the available data
                                 is stored and used,rather than n days.

        Pre-condition:
            weather_data.size() > 0
        
        """

        super().__init__(weather_data)
        self._number_of_days = number_of_days
        if self._number_of_days < self._weather_data.size() :
            self._days_weather = self._weather_data.get_data(self._number_of_days)
        else :
            self._number_of_days = self._weather_data.size()
            self._days_weather = self._weather_data.get_data(self._number_of_days)
            

    def get_number_days(self) :
        """(int) Return the number of days of data being used."""

        return self._number_of_days

    def chance_of_rain(self):
        """
        Calculate the average rainfall for the past n days. Multiply this average by 9.
        If the resulting value is greater than 100, set it to be 100. 

        Return:
            (int) chance of rain

        """
        
        
        total_rainfall = 0
        for day in self._days_weather :
            total_rainfall += day.get_rainfall()

        
        chance_of_rain = (total_rainfall / self._number_of_days) * 9
    
        if chance_of_rain > 100 :
            return 100

        return int(round(chance_of_rain)) 

    def high_temperature(self) :
        """(float) Return the highest temperature recorded in the past n days."""
        hightest_temperature = self._days_weather[0].get_high_temperature()
        for day in self._days_weather :
            high_temperature = day.get_high_temperature()
            if high_temperature > hightest_temperature :
                hightest_temperature = high_temperature

        return hightest_temperature

    def low_temperature(self) :
        """(float) Return the lowest temperature recorded in the past n days."""
        lowest_temperature = self._days_weather[0].get_low_temperature()
        for day in self._days_weather :
            low_temperature = day.get_low_temperature()
            if low_temperature < lowest_temperature :
                lowest_temperature = low_temperature

        return lowest_temperature

    def humidity(self) :
        """(int) Return the average of relative humidity from the pass n days."""
        total_humidity = 0
        for day in self._days_weather :
            total_humidity += day.get_humidity()

        average_humidity = total_humidity / self._number_of_days
        return int(average_humidity) 

    def cloud_cover(self) :
        """(int) Retuen the average of data of cloud cover from the pass n days."""
        total_cloud_cover = 0
        for day in self._days_weather :
            total_cloud_cover += day.get_cloud_cover()

        average_cloud_cover = total_cloud_cover / self._number_of_days
        return int(round(average_cloud_cover)) 

    def wind_speed(self) :
        """(int) Return the average of average wind speed from the pass n days."""
        total_wind_speed = 0
        for day in self._days_weather :
            total_wind_speed += day.get_average_wind_speed()

        average_of_average_wind_speed = total_wind_speed / self._number_of_days
        return int(round(average_of_average_wind_speed)) 
    


class SophisticatedPrediction(WeatherPrediction) :
    """Sophisticated prediction model, the past n days’ worth of weather data."""
    def __init__(self, weather_data, number_of_days) :
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.
            number_of_days(str): use pass n day as data for prediction.
                                 If n is greater than the number of days
                                 of weather data that is available,all of the available data
                                 is stored and used,rather than n days.

        Pre-condition:
            weather_data.size() > 0

        """

        super().__init__(weather_data)
        self._number_of_days = number_of_days
        if self._number_of_days < self._weather_data.size() : 
            self._days_weather = self._weather_data.get_data(self._number_of_days)
        else :
            self._number_of_days = self._weather_data.size() 
            self._days_weather = self._weather_data.get_data(self._number_of_days)

    def get_number_days(self) :
        """(int) Return the number of days of data being used."""
        
        return self._number_of_days

    def chance_of_rain(self) :
        """
        
        Calculate the average rainfall for the past n days.
        If yesterday’s air pressure was lower than the average air pressure for the past n days,
        multiply the average rainfall by 10.
        If yesterday’s air pressure was equal to or higher than the average air pressure for the past n days,
        multiply the average rainfall by 7.
        After taking into account the air pressure,
        if yesterday’s wind direction was from any easterly point (NNE, NE, ENE, E, ESE, SE or SSE)
        multiply the average rainfall by 1.2.
        If the resulting value is greater than 100, set it to be 100.

        Return:
            (int) Chance of rain

        """
        total_air_pressure = 0
        total_rainfall = 0
        chance_of_rain = 0
        yesterday_air_pressure = self._days_weather[self._number_of_days - 1].get_air_pressure()
        yesterday_wind_direction = self._days_weather[self._number_of_days - 1].get_wind_direction()
        easterly_point = ["NNE", "NE", "ENE", "E", "ESE", "SE", "SSE"]
        
        for day in self._days_weather :
            total_air_pressure += day.get_air_pressure()
            total_rainfall += day.get_rainfall()
            
        average_air_pressure = total_air_pressure / self._number_of_days
        average_rainfall = total_rainfall / self._number_of_days
        

        if yesterday_air_pressure < average_air_pressure :
            chance_of_rain = average_rainfall * 10
        else :
            chance_of_rain = average_rainfall * 7

        if yesterday_wind_direction in easterly_point :
            chance_of_rain *= 1.2

        if chance_of_rain > 100 :
            return 100
        else :
            return int(round(chance_of_rain))

    def high_temperature(self) :
        """
        Calculate the average high temperature for the past n days.
        If yesterday’s air pressure was higher than the average air pressure for the past n days,
        add 2 to the calculated average high temperature.

        Return:
            (float) Average of high temperature

        """
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
            average_high_temperature = average_high_temperature + 2
            return average_high_temperature

        return average_high_temperature
            
        
    def low_temperature(self) :
        """
        Calculate the average low temperature for the past n days.
        If yesterday’s air pressure was lower than the average air pressure for the past n days,
        subtract 2 from the calculated average low temperature.
        

        Return:
            (float) Average of low temperature

        """
        total_low_temperature = 0
        total_air_pressure = 0
        yesterday_air_pressure = self._days_weather[self._number_of_days - 1].get_air_pressure()
        
        
        for day in self._days_weather :
            total_low_temperature += day.get_low_temperature()
            total_air_pressure += day.get_air_pressure()

        average_low_temperature = total_low_temperature / self._number_of_days
        average_air_pressure = total_air_pressure / self._number_of_days

        if yesterday_air_pressure < average_air_pressure :
            average_low_temperature = average_low_temperature - 2
            return average_low_temperature
        
        return average_low_temperature
        
    def humidity(self) :
        """
        Calculate the average humidity for the past n days.
        If yesterday’s air pressure was lower than the average air pressure for the past n days,
        add 15 to the calculated average humidity.
        If yesterday’s air pressure was higher than the average air pressure for the past n days,
        subtract 15 from the calculated average humidity.
        If the resulting value is less than 0 or greater than 100, set it to be 0 or 100.
        

        Return:
            (int) Average humidity

        """
        total_humidity = 0
        total_air_pressure = 0
        yesterday_air_pressure = self._days_weather[self._number_of_days - 1].get_air_pressure()

        for day in self._days_weather :
            total_humidity += day.get_humidity()
            total_air_pressure += day.get_air_pressure()

        average_humidity = total_humidity / self._number_of_days
        average_air_pressure = total_air_pressure / self._number_of_days

        if yesterday_air_pressure < average_air_pressure :
            average_humidity = average_humidity + 15
        elif yesterday_air_pressure > average_air_pressure :
            average_humidity = average_humidity - 15

        if average_humidity > 100 :
            return 100
        elif average_humidity < 0 :
            return 0
        else :
            return int(round(average_humidity))
        
        

    def cloud_cover(self) :
        """
        Calculate the average cloud cover for the past n days.
        If yesterday’s air pressure was lower than the average air pressure for the past n days,
        add 2 to the calculated average cloud cover.
        If the resulting value is greater than 9, set it to be 9.


        Return:
            (int) Average of cloud cover 
    
        """
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
        """
        Calculate the average of the average wind speed for the past n days.
        If yesterday's maximum wind speed was greater than four times the calculated average wind speed,
        multiply the calculated average wind speed by 1.2. Return this result.

        Return:
            (int) Average of wind speed

        """
        total_wind_speed = 0
        yesterday_max_wind_speed = self._days_weather[self._number_of_days - 1].get_maximum_wind_speed()
        
        for day in self._days_weather :
            total_wind_speed += day.get_average_wind_speed()

        average_wind_speed = total_wind_speed / self._number_of_days

        if yesterday_max_wind_speed > 4 * average_wind_speed :
            average_wind_speed *= 1.2

        return int(round(average_wind_speed)) 
        
        


if __name__ == "__main__":
    print("This module provides the weather prediction models",
          "and is not meant to be executed on its own.")
