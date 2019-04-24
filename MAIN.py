from threading import Thread
import time
import computations
from CONTROL import main_thread, print_to_screen, s
""" use the threading library to allow multiple threads
this is used to take user input while the main program is running"""

def io_thread():
    """This thread is run from the command line, generally PUTTY or another SSH
    client. Allows you to issue commands as defined in glob.allowed_commands"""
    from bob import bob, allowed_commands
    global bob
    while True:
        inp = input("[command]>").lower()
        if inp == "exit":
            inp = input("[u sure bro?! [Y/N]]>").lower()
            if inp == "y":
                bob.terminate = True
                print("bye io")
                exit()
        elif inp == "igps" or inp == "gps":
            a = float(input("[a?]>"))
            c = float(input("[c?]>"))
            d = float(input("[d?]>"))
            loc = computations.iGPS_math(a,c,d)
            print_to_screen("a: {}".format(a),
                            "c: {}".format(c),
                            "d: {}".format(d),
                            "x: {}".format(loc[0]), 
                            "y: {}".format(loc[1]))
            s.speak("click")
        elif inp == "kill":
            bob.kill = True
        elif inp == "see":
            bob.commands.contents()
        elif inp == "help":
            print("Allowed commands:")
            for command in allowed_commands:
                print("{}, which issues the {} function".format(command, allowed_commands[command][0]))
        elif inp == "mega":
            inp = input("[mega]>").lower()
            if inp in allowed_commands.keys():
                args = []
                for arg in allowed_commands[inp][1:]:
                    arg_inp = input("[{}?]>".format(arg))
                    args.append(arg_inp)
                    if arg[-1]=="S":
                        args[-1] = "\""+str(arg_inp)+"\""
                if args == []:
                    command = allowed_commands[inp][0] + "()"
                else:
                    command = allowed_commands[inp][0] + "({})".format(",".join(args))
                bob.commands.megapush(command)
        else:
            if inp in allowed_commands.keys():
                """Take arguments for a predefined command and then push it to the queue"""
                args = []
                for arg in allowed_commands[inp][1:]:
                    arg_inp = input("[{}?]>".format(arg))
                    args.append(arg_inp)
                    if arg[-1]=="S":
                        args[-1] = "\""+str(arg_inp)+"\""
                if args == []:
                    command = allowed_commands[inp][0] + "()"
                else:
                    command = allowed_commands[inp][0] + "({})".format(",".join(args))
                bob.commands.push(command)

if __name__ == "__main__":
    print("="*50)
    print("Welcome to Bobbert OS :-)")
    print("="*50)
    main = Thread(target=main_thread)
    io = Thread(target=io_thread)
    main.start()
    io.start()

