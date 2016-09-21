import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

def Create_States_Tuple(lights,oncomings,lefts,rights,next_waypoints) :
    #states = [(light,oncoming,left,right,next_waypoint) for light in lights for oncoming in oncomings \
    #         for left in lefts for right in rights for next_waypoint in next_waypoints]

    states = [(light,oncoming,left,next_waypoint) for light in lights for oncoming in oncomings \
             for left in lefts for next_waypoint in next_waypoints]
    return states
    

def Init_Qtable(states,actions) :
    Qtable = dict()
    for state in states :
        for action in actions :
            Qtable[(state,action)] = 0.0
    return Qtable

def Get_Keys_With_Matching_State(Qtable,state) :
    match_keys = []
    keys = Qtable.keys()
    for key in keys :
        temp_state = key[0]
        if state == temp_state :
            match_keys.append(key)
            
    return match_keys

            
def Get_Max_Action_For_State(Qtable,state) :
    match_keys = Get_Keys_With_Matching_State(Qtable,state)
    best_action = None
    max_value = 0.0
    for key in match_keys :
        temp_state = key[0]
        temp_action = key[1]
        value = Qtable[key]
        if value >= max_value :
            max_value = value
            best_action = temp_action
            
    return (best_action,max_value)

def Update_Qtable(Qtable,alpha,gamma,reward,state,action) :
    current_value = Qtable[(state,action)]
    
    (best_action,max_value) = Get_Max_Action_For_State(Qtable,state)
    
    update_value = ((1-alpha) * current_value) + (alpha * (reward + gamma * max_value))
    
    Qtable[(state,action)] = update_value
    
    return Qtable


class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    QTable = {}
    alpha = 0.0
    gamma = 0.0
    sim_time = 1.0
    t = 0
    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
       
        self.gamma = 0.35
        self.epsilon = 0.1
        self.t = 0
        # TODO: Initialize any additional variables here
        valid_actions = [None, 'forward', 'left', 'right']

        valid_light = ['green','red']
        valid_left = valid_actions
        valid_right = valid_actions
        valid_oncoming = valid_actions

        states = Create_States_Tuple(valid_light,valid_oncoming,valid_left,valid_right,valid_actions)
        
        actions = valid_actions
        self.Qtable = Init_Qtable(states,actions)
                              
                         
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        self.alpha = 1.0
        self.t += 1
        if self.t != 0 : 
            self.alpha = 1 / float(self.t)
            self.epsilon = 1 / float(self.t)
        #self.alpha = 0.6


        # TODO: Update state
        #self.state = (inputs['light'],inputs['oncoming'],inputs['left'],inputs['right'],self.next_waypoint)
        self.state = (inputs['light'],inputs['oncoming'],inputs['left'],self.next_waypoint)
        
        # TODO: Select action according to your policy
        #action = random.choice(self.env.valid_actions)
        if (random.uniform(0, 1) < self.epsilon) :
            # Choose an action randomly
            action = random.choice(self.env.valid_actions)
        else :
            (action,dummy) = Get_Max_Action_For_State(self.Qtable,self.state)
        
        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        print "LearningAgent.update(): Sim_time = {}, alpha = {}".format(self.t,self.alpha)
        self.Qtable = Update_Qtable(self.Qtable,self.alpha,self.gamma,reward,self.state,action)
        
        
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, ,next_waypoint = {},reward = {}".format(deadline, inputs, action, self.next_waypoint,reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.0001, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
