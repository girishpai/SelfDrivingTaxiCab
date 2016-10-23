import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from qtable import QTable as qt


class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    QTable = qt()
    alpha = 0.0
    gamma = 0.0
    trial_num = 0
    epsilon = 0.0
    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
       
        self.gamma = 0.35
        self.epsilon = 0.6
        
        # TODO: Initialize any additional variables here
        valid_actions = [None, 'forward', 'left', 'right']

        valid_light = ['green','red']
        valid_left = valid_actions
        valid_right = valid_actions
        valid_oncoming = valid_actions

        states = self.QTable.Create_States_Tuple(valid_light,valid_actions)

        actions = valid_actions

        self.QTable.Init_Qtable(states,actions)
                              
                         
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.trial_num += 1

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        #For first part of project, comment out once done.
        #action = random.choice(self.env.valid_actions)

        #Decay alpha
        self.alpha = 1 / float(self.trial_num)

        # After first 80 trials, make epsilon 0, to make sure the agent chooses action based on QTable. 
        if self.trial_num > 80:
            self.epsilon = 0.0
      


        # TODO: Update state

        #Required when traffic_light = 'green' and agent needs to take a left. Agent needs to yield to oncoming traffic before taking left.
        Scenario_1 = (inputs['light'] == 'green' and (inputs['oncoming'] == 'forward' or inputs['oncoming'] == 'right'))

        #Required when traffic_light = 'red' and agent needs to take a right. Agent needs to yiled to left traffic moving forward before taking right. 
        Scenario_2 = (inputs['light'] == 'red' and inputs['left'] == 'forward')
        
        self.state = (Scenario_1,Scenario_2,inputs['light'],self.next_waypoint)
        
        # TODO: Select action according to your policy

        if (random.uniform(0, 1) < self.epsilon) :
            # Choose an action randomly
            action = random.choice(self.env.valid_actions)
        else :
            (action,dummy) = self.QTable.Get_Max_Action_For_State(self.state)
        
        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        #print "LearningAgent.update(): Trial Num = {}".format(self.trial_num)
        self.QTable.Update_Qtable(self.alpha,self.gamma,reward,self.state,action)
        
        
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, ,next_waypoint = {},reward = {}".format(deadline, inputs, action, self.next_waypoint,reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment(50)  # create environment (also adds some dummy traffic)
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
