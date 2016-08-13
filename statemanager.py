
class StateManager(object):
    def __init__(self, states):
        # Must pass a dictionary of initialized states
        # Starting from key 1 (key 1 will be initial state)
        self.statedict = states
        self.changeState(self.statedict[1])
        self.initState = True

    def changeState(self, state):
        # Actual state object
        self.state = state
        self.state.manager = self

    def start(self):
        # Only call when self.state exists
        if self.state == None:
            raise MissingState("Trying to start State Manager without a state")
        nextState = 1
        while nextState != 0:
            if not self.initState:
                self.changeState(self.statedict[nextState])
            nextState = self.state.run()

            if self.initState:
                self.initState = False

        print "State Manager Finished"
                
        
            

class State(object):
    
    def __init__(self):
        self.name = None
        self.description = None
        self.nextState = 0 # All states default to being the last state
        
    def __str__(self):
        return str(self.name) + str(self.description)
    

    def run(self):
        # Run functions of State objects should return info on the
        # next state the machine should turn to
        # Run should return 0 to end statemanager
        raise MissingFunction("Child of State Class has no Run Function")
