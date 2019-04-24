class Queue:
    """A basic first in last out data structure"""
    def __init__(self):
        self.list = []
    def push(self, item):
        self.list.append(item)
        print(self.list)
    def megapush(self, item):
        self.list = [item] + self.list
    def pop(self):
        to_ret = self.list[0]
        del self.list[0]
        return to_ret
    def empty(self):
        if len(self.list)==0:
            return True
        else:
            return False
    def contents(self):
        if self.empty():
            print("Queue is empty!")
            return
        for i, item in enumerate(self.list):
            print("Item {}: {}".format(i+1, str(item)))

class State:
    """A single class the stores all important states of the program. The instance
    of this class is endearingly named bob."""
    def __init__(self,debug=False):
        self.terminate = False # if true, close the program
        self.kill = False # if true, kill the current command
        self.commands = Queue()
        self.debug = debug # this doesn't actually do anything


def command_handler(queue=None):
    global bob
    # returns True if the subroutine calling this function
    # should terminate
    if bob.terminate:
        print("bye main")
        exit()
    if bob.kill:
        bob.kill = False
        return True

allowed_commands = {
    "straight":["straight_forwards", "cm"],
    "back":["straight_backwards","cm"],
    "turn":["turn","deg"],
    "letters":["write_letters","charS"],
    "hold":["hold"],
    "down":["open_claw"],
    "up":["close_claw"],
    "say":["say", "phraseS"],
    "dance":["dance"],
    "scan":["move_and_scan"],
    "shimmer":["shimmer", "how long"],
    "print":["print_to_screen","messageS"],
    "grab":["turn_and_grab_box"],
    "explore":["explore_and_find_boxes"]
}

bob = State()