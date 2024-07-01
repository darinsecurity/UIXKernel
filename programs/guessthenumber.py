import random
while True:
   print("Can you guess the number? The number is between 1 and 100.")
   guess_count = 0
   actual_number = random.randint(1,100)
   user_number = 0
   while user_number != actual_number:
      user_input = input("> ")
      try:
         user_number = int(user_input)
      except Exception as e:
         print("Please provide a valid number. ")
         continue
   
      if user_number == actual_number:
         print("You guessed the number! It was {}.".format(user_number))
         break
      else:
         print("Try again! The number is ", end="")
         if user_number > actual_number:
            print("smaller.")
         else:
            print("bigger.")
   play_again = input("Play again? (Y/N)")
   if play_again != "Y":
      break