import random
comGuess = int(input("Target: b/w 0-100:"))
userGuess = int(input("Enter your guessed no. b/w 0-100:"))
a = 1


while True:
    # comGuess=random.randint(0,100)
    if userGuess < comGuess:
        userGuess = int(input("Guess Higher:"))
        a+=1
    elif userGuess > comGuess:
        userGuess = int(input("Guess Lower:"))
        a+=1
    else:
        print ("Guessed Corectly after {} guesses".format(a))
        break