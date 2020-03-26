from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction
import random
import numpy

user_score=0
bot_score=0
sounds = {'1':['meong', 'yaong', 'nyan', 'näu', 'mjav'],'2':['nyam','njamka', 'gnam', 'nefis', 'umai'], '3':['beurk', 'yök', 'fuj', 'æsj', 'waek']}
random_sound = 'mjav'

class ChooseGame(Action):

    def name(self) -> Text:
        return "action_choose_game"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

     choice = tracker.latest_message.get('text')
     if(choice==str(1)):
         return [FollowupAction("utter_instruction")]
     elif(choice==str(2)):
         return [FollowupAction("action_meow_yum_yuck")] 

class ResetScore(Action):

    def name(self) -> Text:
        return "action_reset_score"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global user_score
        global bot_score
        user_score=0
        bot_score=0

        return

class MeowYumYuck(Action):

    def name(self) -> Text:
        return "action_meow_yum_yuck"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sounds = {'1':['meong', 'yaong', 'nyan', 'näu', 'mjav'],'2':['nyam','njamka', 'gnam', 'nefis', 'umai'], '3':['beurk', 'yök', 'fuj', 'æsj', 'waek']} 

        global random_sound
        random_key = random.choice(list(sounds.keys()))
        random_sound = random.choice(sounds[random_key])
        dispatcher.utter_message(text="Does \"" + str(random_sound) + "\" mean (1) meow, (2) yum, or (3) yuck? Enter a digit corresponding to your choice.")

        return


class EvaluateAnswer(Action):

    def name(self) -> Text:
        return "action_evaluate_answer"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        global user_score
        global bot_score
        global random_sound
        #dispatcher.utter_message(text="Random sound: " + str(random_sound))  

        choice = tracker.latest_message.get('text')
        #dispatcher.utter_message(text="Choice: " + str(choice))  
        for k,v in sounds.items():
            if(random_sound in v):
                correct_answer = k
   
        #dispatcher.utter_message(text="correct_answer: " + str(correct_answer))
        if(choice==correct_answer):
            user_score+=1
            dispatcher.utter_message(text="Correct! One point to you.")
        else:
            bot_score+=1
            dispatcher.utter_message(text="Wrong! One point to me.")

        dispatcher.utter_message(text="Bot: " + str(bot_score) + ", You: " + str(user_score))

        if(user_score < 3 or bot_score < 3):
            dispatcher.utter_message(text="Here's another one:")
            return [FollowupAction('action_meow_yum_yuck')]
        elif(user_score > 2):
            dispatcher.utter_message(text="Congratulations, you won!")
            user_score = 0
            bot_score = 0
            dispatcher.utter_message(text="Wanna play again?")
            return [FollowupAction("utter_choose_game")] 
        elif(bot_score > 2):
            dispatcher.utter_message(text="Yay, I won! Better luck next time.")
            user_score = 0
            bot_score = 0
            dispatcher.utter_message(text="Wanna play again?")
            return [FollowupAction("utter_choose_game")] 

        return

class UpdateScore(Action):
    
    def name(self) -> Text:
        return "action_evaluate_score"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        bot_right = ["I'm on a roll.", "Wow, I'm a good bot.", "Hah!", "This is going fabulous." ]
        bot_wrong = ["My bad...", "Oh no.", "Dang.", "Wow, I'm considering changing career.", ":((("]
        global user_score
        global bot_score

        intent=tracker.latest_message['intent'].get('name')

        if(intent=='affirm'):
            bot_score+=1
            dispatcher.utter_message(text=random.choice(bot_right) + " One point to me.")
        elif (intent=='deny'):
            user_score+=1
            dispatcher.utter_message(text=random.choice(bot_wrong) + " One point to you.")
        
        dispatcher.utter_message(text="Bot: " + str(bot_score) + ", You: " + str(user_score))
        
        if(user_score < 3 or bot_score < 3): 
            dispatcher.utter_message(text="Give me another one.")
        elif(user_score > 2):
            dispatcher.utter_message(text="Congratulations, you won!")
            user_score=0
            bot_score=0
            dispatcher.utter_message(text="Wanna play again?")
            return [FollowupAction("utter_choose_game")]
        elif(bot_score > 2):
            dispatcher.utter_message(text="Yay, I won! Better luck next time.")
            bot_score=0
            user_score=0
            dispatcher.utter_message(text="Wanna play again?")
            return [FollowupAction("utter_choose_game")] 

        return 
