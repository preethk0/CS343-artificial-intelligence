Preeth Kanamangala
PK9297

1. For the value iteration portion of the project, I basically
directly applied what we learned in class. In the computeQValueFromValues()
function, the Q value of taking an action from a certain state is an
explicit formula. We just had to keep a cumulative sum, since the transition
function has different possible states with different probabilities. In the
computeActionFromValues() function, we just wanted to find the action that
results in the highest value. Computing the values for each action, choosing
the max value, and picking out the action that resulted in that value does just
that. Finally, in the main part of the class, we just ran value iteration,
which was just for each state picking an action and calculating the Q value
of taking that action from that state, for a given number of iterations.

2. N/A

3. N/A

4. In the computeValueFromQValues() function, we just wanted to run through
every action and store the max value produced. This was straightforward because
we already had a getQValue() function. In the computeActionFromQValues() function,
we wanted to find the best action to take from a state. So, we just went
through all actions from a state and their resulting Q values, storing the
action that resulted in that Q value if the value was a max thus far. Finally,
in the update() function, we simply used the update formula provided in class.

5. Here, we very simply, with probability epsilon, took a random action out of the
legal ones and took an action according to the best policy otherwise.

6. N/A

7. N/A

8. In the getQValue() function, we used the formula on the project page. We just
kept a running sum (Q value) of all the features times their feature weight. In
the update() function, we also used the other 2 formulas on the project page.
Specifically, we calculate the difference, and then use it to update the 
weights for all given features.
