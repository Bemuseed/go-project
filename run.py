import play_problem
import human_vs_human

print("#################################")
print("# Welcome to Caleb's GO PROGRAM #")
print("#################################\n")

MENU = """
Play a game against another human:  [P]
Play a Go Problem:                  [G]
Exit:                               [X]

Selection:  """

exit = False
while not exit:
    choice = input(MENU).lower()
    if choice == "p":
        human_vs_human.main()
    elif choice == "g":
        play_problem.main()
    elif choice == "x":
        exit = True
    else:
        print("'{}' is an invalid choice.\n".format(choice))
