"""

Simple recommendation tool for traveler

"""

__author__ = "ZHANG DECHAO"
__date__ = "2019.3.11"


from destinations import Destinations


def main():
    # Task 1: Ask questions here
    hasDestination = False
    print("Welcome to Travel Inspiration!\n")
    
    getName = input("What is your name? ")
    print("\nHi,", getName + "!\n")

    
################## The first part questions(begin) ############################
    
    def theFirstQuestion() :
        
        """
        1,Return the choice from traveler
        2,obtain multiple input from traveler
        3,Judge whether the traveler input the invalid choice
        
        """
        
        print("Which continents would you like to travel to?")
        print("  1) Asia\n  2) Africa\n  3) North America\n  4) South America\n",
              " 5) Europe\n  6) Oceania\n  7) Antarctica")
        
        sortMutipleInput = []
        obtainChoice = input("> ") # obtain multiple input
        obtainChoiceAsList = [] # use for storing all inputs into the list.
        
        for i in obtainChoice :
            if i not in ["1", "2", "3","4", "5", "6", "7", ",", " "]: 
                return obtainChoice
                break
            else :
                obtainChoiceAsList.append(i) 

        for i in obtainChoiceAsList : 
            if i.isdigit() : 
                sortMutipleInput.append(i) 
        
        finalMultipleChoice = list(set(sortMutipleInput)) # eliminate repeat values and get the final multiple choices

        collections = [] # use for collecting the choice number : 1),2) ... 7)
        getChoice = []
        result = ["asia", "africa", "north america", "south america", "europe", "oceania", "antarctica"]
        for i in finalMultipleChoice :
            collections.append(int(i))
            
        for i in collections :
            getChoice.append(result[i - 1]) 
            
        return getChoice
        
    def theSecondQuestion() :
        
        """
        1,Return the choice from traveler
        2,Judge whether the traveler input the invalid choice
        
        """
        
        print("\nWhat is money to you?")
        print("  $$$) No object\n",
              " $$) Spendable, so long as I get value from doing so\n",
              " $) Extremely important; I want to spend as little as possible")
        getChoice = input("> ")
        if getChoice == "$$$" and getChoice == "$$" and getChoice == "$" :
            result = getChoice
            return result
        else :
            return getChoice
        
    def theThirdQuestion() :
        
        """
        1,Return the choice from traveler
        2,Judge whether the traveler input the invalid choice
        
        """
        
        print("\nHow much crime is acceptable when you travel?")
        print("  1) Low\n  2) Average\n  3) High")
        getChoice = int(input("> "))
        result = ["low", "average", "high"]
        if getChoice == 1 or getChoice == 2 or getChoice == 3 :
            return result[getChoice - 1]
        else :
            return getChoice
        
    def theForthQuestion() :
        
        """
        1,Return the choice from traveler
        2,Judge whether the traveler input the invalid choice
        
        """
        
        print("\nWill you be travelling with children?")
        print("  1) Yes\n  2) No")
        getChoice = input("> ")
        if getChoice == "1" :
            return True
        elif getChoice == "2" :
            return False
        else :
            return getChoice

    def theFifthQuestion() :
        
        """
        1,Return the choice from traveler
        2,obtain multiple input from traveler
        3,Judge whether the traveler input the invalid choice
        
        """
        
        print("\nWhich seasons do you plan to travel in?")
        print("  1) Spring\n  2) Summer\n  3) Autumn\n  4) Winter")
        
        sortMutipleInput = [] 
        obtainChoice = input("> ") # obtain multiple input
        obtainChoiceAsList = [] # use for storing all inputs into the list.
        for i in obtainChoice :
            if i not in ["1", "2", "3","4", ",", " "]:
                return obtainChoice
                break
            else :
                obtainChoiceAsList.append(i) 

        for i in obtainChoiceAsList : 
            if i.isdigit() : 
                 sortMutipleInput.append(i) 
                
        finalMultipleChoice = list(set(sortMutipleInput)) # eliminate repeat values and get the final multiple choices

        collections = [] # use for collecting the choice number : 1),2)...7)
        getChoice = []
        result = ["spring", "summer", "autumn", "winter"]
        for i in finalMultipleChoice :
            collections.append(int(i))
            
        for i in collections :
            getChoice.append(result[i - 1]) 
            
        return getChoice
        

    def theSixthQuestion() :

        """
        1,Return the choice from traveler
        2,Judge whether the traveler input the invalid choice
        
        """
        
        print("\nWhat climate do you prefer?")
        print("  1) Cold\n  2) Cool\n  3) Moderate\n  4) Warm\n  5) Hot")
        getChoice = int(input("> "))
        result = ["cold", "cool", "moderate", "warm", "hot"]
        if getChoice == 1 or getChoice == 2 or getChoice == 3 or getChoice == 4 or getChoice == 5 :
            return result[getChoice - 1]
        else :
            return getChoice

################## The first part questions(end) ############################

    """
    
    1,Collect the answer from the first part questions by defining value1, value2, ... value6
    2,tell the travelers when they enter the wrong value
    
    """ 
    
    isWrongInput = True
    while isWrongInput : #assume the input is wrong and get in the while loop
        value1 = theFirstQuestion()
        for i in value1 :
            if i not in ["asia", "africa", "north america", "south america", "europe", "oceania", "antarctica"] :
                print("\nI'm sorry, but" , value1 , "is not a valid choice. Please try again.")
                break
            else :
                isWrongInput = False 
                
        
    value3 = theSecondQuestion()
    while value3 != "$$$" and value3 != "$$" and value3 != "$" :    
        print("\nI'm sorry, but" , value3 , "is not a valid choice. Please try again.")
        value3 = theSecondQuestion() 
    
    value4 = theThirdQuestion()
    while value4 != "low" and value4 != "average" and value4 != "high" :
        print("\nI'm sorry, but" , value4 , "is not a valid choice. Please try again.")
        value4 = theThirdQuestion() 
    
    value2 = theForthQuestion()
    while value2 != False and value2 != True :
        print("\nI'm sorry, but" , value2 , "is not a valid choice. Please try again.")
        value2 = theForthQuestion() 
    

    isWrongEnter = True
    while isWrongEnter : # assume the enter is wrong and get in the while loop
        value6 = theFifthQuestion()
        for i in value6 :
            if i not in ["spring", "summer", "autumn", "winter"] :
                print("\nI'm sorry, but" , value6 , "is not a valid choice. Please try again.")
                break
            else :
                isWrongEnter = False 
    
   
    value5 = theSixthQuestion()
    while value5 != "cold" and value5 != "cool" and value5 != "moderate" and value5 != "warm" and value5 != "hot"  :
        print("\nI'm sorry, but" , value5 , "is not a valid choice. Please try again.")
        value5 = theSixthQuestion() 
    
    print("\nNow we would like to ask you some questions about your interests," 
      + " on a scale of -5 to 5. -5 indicates strong dislike,"
      + " whereas 5 indicates strong interest, and 0 indicates indifference.\n")
    



################## The Second part questions(begin) ############################



    def levelOfPerference() :
        
        """

        1, return the degree from different perference
        2, use list as the value of return
        
        """
        
        LevelOfPerference = []
        
        print("How much do you like sports? (-5 to 5)")
        getLevel1 = int(input("> "))
        LevelOfPerference.append(getLevel1)
        

   
        print("\nHow much do you like wildlife? (-5 to 5)")
        getLevel2 = int(input("> "))
        LevelOfPerference.append(getLevel2)

    
        print("\nHow much do you like nature? (-5 to 5)")
        getLevel3 = int(input("> "))
        LevelOfPerference.append(getLevel3)

    
        print("\nHow much do you like historical sites? (-5 to 5)")
        getLevel4 = int(input("> "))
        LevelOfPerference.append(getLevel4)

    
        print("\nHow much do you like fine dining? (-5 to 5)")
        getLevel5 = int(input("> "))
        LevelOfPerference.append(getLevel5)

    
        print("\nHow much do you like adventure activities? (-5 to 5)")
        getLevel6 = int(input("> "))
        LevelOfPerference.append(getLevel6)

    
        print("\nHow much do you like the beach? (-5 to 5)")
        getLevel7 = int(input("> "))
        LevelOfPerference.append(getLevel7)

        return LevelOfPerference


################## The Second part questions(end) ############################


     
    
    nameStore = [] # record the city name later
    scoreStore = [] # record the total score later

    
    """ collect the answer from the second part questions by defining answer1, answer2, ... answer7 """
    answer = levelOfPerference()
    answer1 = answer[0]
    answer2 = answer[1]
    answer3 = answer[2]
    answer4 = answer[3]
    answer5 = answer[4]
    answer6 = answer[5]
    answer7 = answer[6]
    
    
    
    for destination in Destinations().get_all():
        
        # Task 2+: Add comparison logic here
        def filter1() :
            judge = False 
            
            """

            1,judge that whether the choice is equal to the "contients" from datebase
            2,return a list of boolean value when the contients are equal or unequal to the traveler choice

            """
            for i in value1 :
                judgeSingleChoice = i == destination.get_continent() # filter the boolean value when the single choice is equal to continent. 
                judge = judge or judgeSingleChoice 
            return judge # return the boolean value
            
        def filter2() :

            """

            1,judge that whether the choice is equal to the "kids" from datebase
            2,return a list of boolean value when the kid friendly is equal or unequal to the traveler choice
            3,satisfy the criteria that If the user will be travelling with children, it must be kid friend

            """
            
            if value2 == False :
                judge = False == destination.is_kid_friendly() or True == destination.is_kid_friendly()
            else :
                judge = False == destination.is_kid_friendly()
            return judge # return the boolean value

        def filter3() :

            """

            1,judge that whether the choice is equal to the "cost" from datebase
            2,return a list of boolean value when the anticipant cost is equal or unequal to the traveler choice
            3,satisfy the criteria that cost must be less than or equal to the user's response to the money question

            """
            
            if value3 == "$$$" :
                judge = destination.get_cost() == "$$$" or destination.get_cost() == "$$" or destination.get_cost() == "$"
                return judge
            elif value3 == "$$" :
                judge = destination.get_cost() == "$$" or destination.get_cost() == "$"
                return judge
            elif value3 == "$" :
                judge = destination.get_cost() == "$"
                return judge

        def filter4() :

            """

            1,judge that whether the choice is equal to the "crime" from datebase
            2,return a list of boolean value when the anticipant safety is equal or unequal to the traveler choice
            3,satisfy the criteria that crime cannot be greater than is acceptable to the user

            """
        
            if value4 == "high" :
                judge = destination.get_crime() == "high" or destination.get_crime() == "average" or destination.get_crime() == "low"
                return judge
            elif value4 == "average" :
                judge = destination.get_crime() == "average" or destination.get_crime() == "low"
                return judge
            elif value4 == "low" :
                judge = destination.get_crime() == "low"
                return judge

        def filter5() :
            
            """

            1,judge that whether the choice is equal to the "climate" from datebase
            2,return a list of boolean value when the climate perference is equal or unequal to the traveler choice

            """
            
            judge = value5 == destination.get_climate()
            return judge

        def calculate_sum_score() :

            """

            1,use the list[] to store the sum of score
            2,return the max score

            """
            
            score1 = answer1 * destination.get_interest_score('sports')
            score2 = answer2 * destination.get_interest_score('wildlife')
            score3 = answer3 * destination.get_interest_score('nature')
            score4 = answer4 * destination.get_interest_score('historical')
            score5 = answer5 * destination.get_interest_score('cuisine')
            score6 = answer6 * destination.get_interest_score('adventure')
            score7 = answer7 * destination.get_interest_score('beach')
            interest_score = score1 + score2 + score3 + score4 + score5 + score6 + score7
            season_factor_score = [] 
            for i in value6 :
                season_factor_score.append(destination.get_season_factor(i)) # store the season factor in the list
            
            total_score = []
            for i in season_factor_score :
                total_score.append(i * interest_score) # store the total score in the list
           
            return max(total_score) # return the max score in the list
        
       
        if filter1() and filter2() and filter3() and filter4() and filter5():
            hasDestination = True
            nameStore.append(destination.get_name())
            
            scoreStore.append(calculate_sum_score())
            
            
    
    """ obtain the max score and city name in the scoreStore and nameStore """
    if hasDestination == True :   
        the_max_score = scoreStore[0]
        the_max_score_name = nameStore[0]
        counter = 1
        while counter < len(nameStore) :
            if the_max_score < scoreStore[counter] :
                the_max_score = scoreStore[counter]
                the_max_score_name = nameStore[counter]

            counter += 1
    
    # Task 2+: Output final answer here
    if hasDestination == True :
        print("\nThank you for answering all our questions. Your next travel destination is:\n" + the_max_score_name)
    else :
        print("\nThank you for answering all our questions. Your next travel destination is:", "None")

   
    
if __name__ == "__main__":
    main()





