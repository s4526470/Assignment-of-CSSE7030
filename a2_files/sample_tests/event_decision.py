"""
    Simple application to help make decisions about the suitability of the
    weather for a planned event. Second assignment for CSSE1001/7030.

    Event: Represents details about an event that may be influenced by weather.
    EventDecider: Determines if predicted weather will impact on a planned event.
    UserInteraction: Simple textual interface to drive program.
"""

__author__ = ""
__email__ = ""

from weather_data import WeatherData
from prediction import WeatherPrediction, YesterdaysWeather, SimplePrediction, SophisticatedPrediction
# Import your SimplePrediction and SophisticatedPrediction classes once defined.


# Define your Event Class here
#class Event(object):
    #pass

class Event(object) :
    """holds data about a single event and provides access to that data."""
    def __init__ (self, name, outdoors, cover_available, time):
        """
        Parameters:
            name (str): a string represent the name of the event.
            outdoors (bool): a boolean value represent whether the event is outdoors.
            cover_available (bool): a boolean value representing whether there is cover available.
            time (int): an integer from 0 up to, but not including, 24, indicating the closest hour to the starting time of the event.

        """
        self._name = name
        self._outdoors = outdoors
        self._cover_available = cover_available
        self._time = time

    def __str__(self):
        """
        Returns a string representation of the Event in the following format:
        ‘Event(name @ time, outdoors, cover_available)’
            
        """
        return f"Event({self._name} @ {self._time}, {self._outdoors}, {self._cover_available})"

    def get_name(self) :
        """(str) get the name of event."""
        return self._name

    def get_time(self) :
        """(int) get the time of event."""
        return self._time

    def get_outdoors(self) :
        """(bool) get the value whether the event is outdoors."""
        return self._outdoors

    def get_cover_available(self) :
        """(bool) get the value whether there is cover available."""
        return self._cover_available


class EventDecision(object):
    """Uses event details to decide if predicted weather suits an event."""

    def __init__(self, event, prediction_model):
        """
        Parameters:
            event (Event): The event to determine its suitability.
            prediction_model (WeatherPrediction): Specific prediction model.
                           An object of a subclass of WeatherPrediction used 
                           to predict the weather for the event.
        """
        self._event = event
        self._prediction_model = prediction_model

    def _temperature_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted temperature

        Return:
            (float) Temperature Factor
        """
        
        high_temperature = self._prediction_model.high_temperature()
        low_temperature = self._prediction_model.low_temperature()
        humidity = self._prediction_model.humidity()

        # Calculate the humidity factor
        # and the value of adjusted temperature
        if humidity > 70 :
            humidity /= 20
            if high_temperature > 0 and low_temperature > 0 : 
                high_temperature += humidity
                low_temperature += humidity
            elif high_temperature < 0 and low_temperature < 0 :
                high_temperature -= humidity
                low_temperature -= humidity  
            elif high_temperature > 0 and low_temperature < 0 :
                high_temperature += humidity
                low_temperature -= humidity
                
        
        init_temperature_factor = 0
        # high temperature
        if (self._event.get_time() >= 6 and self._event.get_time() <= 19) \
           and (high_temperature >= 30 and self._event.get_outdoors()) :
            
            init_temperature_factor = high_temperature / -5 + 6 
           

        elif high_temperature >= 45 : 
            init_temperature_factor = high_temperature / -5 + 6 
            
            
        # low temperature   
        if ((self._event.get_time() >= 0 and self._event.get_time() <= 5) or (self._event.get_time() >= 20 and self._event.get_time() <= 23)) \
            and (low_temperature < 5 and high_temperature < 45) :
            
            init_temperature_factor = low_temperature / 5 - 1.1
                
        if low_temperature > 15 and high_temperature < 30 :
            init_temperature_factor = (high_temperature - low_temperature) / 5

        if init_temperature_factor < 0 :
            if self._event.get_cover_available() :
                init_temperature_factor += 1
            if self._prediction_model.wind_speed() > 3 and self._prediction_model.wind_speed() < 10 :
                init_temperature_factor += 1
            if self._prediction_model.cloud_cover() > 4 :
                init_temperature_factor += 1
            
        
        print(init_temperature_factor)
        return init_temperature_factor 
        

    def _rain_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted rainfall

        Return:
            (float) Rain Factor
        """
        init_rain_factor = 0
        chance_of_rain = self._prediction_model.chance_of_rain()
        wind_speed = self._prediction_model.wind_speed()

        # Calculate the initial rain factor
        if chance_of_rain < 20 :
            init_rain_factor = chance_of_rain / -5 + 4
            
        if chance_of_rain > 50 :
            init_rain_factor = chance_of_rain / -20 + 1

        elif init_rain_factor < 2 and wind_speed > 15 :
            init_rain_factor = init_rain_factor + wind_speed / -15
                
        if (self._event.get_outdoors() and self._event.get_cover_available()) and (wind_speed < 5) :
            init_rain_factor += 1

        if init_rain_factor < -9 :    
            init_rain_factor = -9
        print(init_rain_factor)
        return init_rain_factor 

        

    def advisability(self):
        """
        Determine how advisable it is to continue with the planned event.

        Return:
            (float) Value in range of -5 to +5,
                    -5 is very bad, 0 is neutral, 5 is very beneficial
        """

        total_score = self._rain_factor() + self._temperature_factor() 
        
        if total_score < -5 : 
            total_score = -5
        elif total_score > 5 :
            total_score = 5

        return total_score 
    
        


class UserInteraction(object):
    """Simple textual interface to drive program."""

    def __init__(self):
        """non-attribute constructor"""
        self._event = None
        self._prediction_model = None

    def get_event_details(self):
        """Prompt the user to enter details for an event.

        Return:
            (Event): An Event object containing the event details.
        """
        # Create a list which uses for judging the input of users whether it is invalid.
        valid_choice = ["YES", "Y", "NO", "N"]

        # Create a list which uses for judging the input of time of users whether it is invalid.
        valid_time = []
        for time in range(0, 24) :
            valid_time.append(str(time))
        
        event_name = input("What is the name of the event? ")
        event_outdoors = input("Is the event outdoors? ")

        # If users give invalid input, ask them try again.
        while event_outdoors.upper() not in valid_choice :
            print("Please enter a valid value.")
            event_outdoors = input("Is the event outdoors? ")
            
        event_cover_available = input("Is there covered shelter? ")
        while event_cover_available.upper() not in valid_choice :
            print("Please enter a valid value.")
            event_cover_available = input("Is there covered shelter? ")
            
        event_time = input("What time is the event? ")
        while event_time not in valid_time :
            print("Please enter a valid value.")
            event_time = input("What time is the event? ") 

        
        if event_outdoors.upper() == valid_choice[0] or event_outdoors.upper() == valid_choice[1] :
            event_outdoors = True
        else :
            event_outdoors = False

        if event_cover_available.upper() == valid_choice[0] or event_cover_available.upper() == valid_choice[1] :
            event_cover_available = True
        else :
            event_cover_available = False

        # convert event_time from string to integer. 
        event_time = int(event_time) 
            
        self._event = Event(event_name, event_outdoors, event_cover_available, event_time)
        return self._event
    
        

    def get_prediction_model(self, weather_data):
        """Prompt the user to select the model for predicting the weather.

        Parameter:
            weather_data (WeatherData): Data used for predicting the weather.

        Return:
            (WeatherPrediction): Object of the selected prediction model.
        """

        # Create a list which uses for judging the input of users whether it is invalid.
        valid_choice = ["1", "2", "3"]
        print("Select the weather prediction model you wish to use:")
        print("  1) Yesterday's weather.\n  2) Simple prediction.\n  3) Sophisticated prediction.")
        model_choice = input("> ")
        number_of_days = ""
        
        
        # Error handling can be added to this method.
        while model_choice not in valid_choice :
            print("Please enter a valid value.")
            print("Select the weather prediction model you wish to use:")
            print("  1) Yesterday's weather.\n  2) Simple prediction.\n  3) Sophisticated prediction.")
            model_choice = input("> ") 
        
        if model_choice == '1' :
            self._prediction_model = YesterdaysWeather(weather_data)
            
        # Cater for other prediction models when they are implemented.
        elif model_choice == "2" :
            number_of_days = input("Enter how many days of data you wish to use for making the prediction: ")

            # If users give invalid input, ask them try again.
            while number_of_days.isdigit() == False :
                print("Please enter a valid value")
                number_of_days = input("Enter how many days of data you wish to use for making the prediction: ")
                
            self._prediction_model = SimplePrediction(weather_data, int(number_of_days))
        else :
            number_of_days = input("Enter how many days of data you wish to use for making the prediction: ")

            # If users give invalid input, ask them try again.
            while number_of_days.isdigit() == False :
                print("Please enter a valid value")
                number_of_days = input("Enter how many days of data you wish to use for making the prediction: ")

            self._prediction_model = SophisticatedPrediction(weather_data, int(number_of_days))
            
        return self._prediction_model

    def output_advisability(self, impact):
        """Output how advisable it is to go ahead with the event.

        Parameter:
            impact (float): Impact of the weather on the event.
                            -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        # The following print statement is an example of printing out the
        # class name of an object, which you may use for making the
        # advisability output more meaningful.
        print("based on", type(self._prediction_model).__name__, "model, the advisability of holding", self._event.get_name(), "is"\
              , impact) 
        
        

    def another_check(self):
        """Ask user if they want to check using another prediction model.

        Return:
            (bool): True if user wants to check using another prediction model.
        """

        # Create a list which uses for judging the input of users whether it is invalid.
        valid_choice = ["YES", "Y", "NO", "N"]
        user_choice = input("\nWould you like to check again? ")

        # If users give invalid input, ask them try again.
        while user_choice.upper() not in valid_choice :
            print("Please enter a valid value.")
            user_choice = input("Would you like to check again? ")
        if user_choice.upper() == valid_choice[0] or user_choice.upper() == valid_choice[1] :
            user_choice = True
        else :
            user_choice = False 

        return user_choice
        


def main():
    """Main application's starting point."""
    check_again = True 
    weather_data = WeatherData()
    weather_data.load("weather_data.csv")
    user_interface = UserInteraction()

    print("Let's determine how suitable your event is for the predicted weather.")
    event = user_interface.get_event_details()

    while check_again:
        prediction_model = user_interface.get_prediction_model(weather_data)
        decision = EventDecision(event, prediction_model)
        impact = decision.advisability()
        user_interface.output_advisability(impact)
        check_again = user_interface.another_check()


if __name__ == "__main__":
    main()
