class QTable :

    """
    QTable_dict : Represents the Qtable using (state) as key and action as value 
    alpha : learning rate
    epsilon : parameter for the random restart based exploration. 
    """    
    def __init__(self) :
        self.Qtable_dict = {}
        

    """
    Method : Create_States_Tuple
    Uses a Tuple to represent states. 
    This is done because a dictionary needs the key to be hashable.
    """
    def Create_States_Tuple(self,lights,next_waypoints) :

        states = [(s1,s2,light,next_waypoint) for s1 in [True,False] for s2 in [True,False] \
                  for light in lights for next_waypoint in next_waypoints]

        return states
    

    """
    Method : Init_Qtable
    Initializes the values of the Qtabel to 0.0 
    """
    def Init_Qtable(self,states,actions) :
        for state in states :
            for action in actions :
                self.Qtable_dict[(state,action)] = 0.0

    def Get_Keys_With_Matching_State(self,state) :
        match_keys = []
        keys = self.Qtable_dict.keys()
        for key in keys :
            temp_state = key[0]
            if state == temp_state :
                match_keys.append(key)    
        return match_keys

    """
    Method : Get_Max_Action_For_State
    Find the action with the best Q-value and return. This is used by the agent to decide the next action. 
    
    """
    def Get_Max_Action_For_State(self,state) :
        match_keys = self.Get_Keys_With_Matching_State(state)
        best_action = None
        max_value = 0.0
        for key in match_keys :
            temp_state = key[0]
            temp_action = key[1]
            value = self.Qtable_dict[key]
            if value >= max_value :
                max_value = value
                best_action = temp_action    
        return (best_action,max_value)


    def Update_Qtable(self,alpha,gamma,reward,state,action) :
        current_value = self.Qtable_dict[(state,action)]
        (best_action,max_value) = self.Get_Max_Action_For_State(state)
        update_value = ((1-alpha) * current_value) + (alpha * (reward + gamma * max_value))
        self.Qtable_dict[(state,action)] = update_value




    
        
