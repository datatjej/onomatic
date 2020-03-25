## start path
* greet
  - utter_greet
  - action_reset_score
* affirm
  - utter_choose_game
* enter_digit
  - action_choose_game

## guess sound meaning path
  - action_meow_yum_yuck
* enter_digit
  - action_evaluate_answer

## play again path
  - utter_choose_game
* enter_digit
  - action_choose_game

## pig path
* pig
  - utter_pig
* affirm OR deny
  - action_evaluate_score

## cow path
* cow
  - utter_cow
* affirm OR deny
  - action_evaluate_score

## cat path
* cat
  - utter_cat
* affirm OR deny
  - action_evaluate_score

## dog path
* dog
  - utter_dog
* affirm OR deny
  - action_evaluate_score

## rooster path
* rooster
  - utter_rooster
* affirm OR deny
  - action_evaluate_score
