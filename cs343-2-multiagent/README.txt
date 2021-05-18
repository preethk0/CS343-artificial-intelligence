Preeth Kanamangala 
PK9297 

1. Reflex Agent. This was a very simple evaluation function. We know that the
goal of the game is for pacman to eat all the food AND not get eaten by any of
the ghosts. Well, a simple way to guide him is to eat food is to use the closest
food manhattan distance. I used the reciprocal of this value due to the hint
on the assignment page. To cover the portion of the game where pacman cannot
get eaten by a ghost, I simply used the manhattan distance to the closest ghost.
If this distance is less than 4 (I just guess-checked values from 1 - 10 and found
4 to be good), then we'd want to early return a very bad value (negative infinity) so
that pacman strays away from the ghosts. And, of course, I also used the score of
the successor game state.

2. Minimax. This implementation was inspired by the slides from week 4. This implementation
is also used as a boiler plate on questions 3 and 4. In getActionHelper(), the simple base
cases are if we win, if we lose, or if we reach our specified depth limit, then we've reached the
end and need to return. Otherwise, we have two cases. Either we need to calculate the value/action
pair for pacman (max) or for the other agent (min). This can be differentiated by the index number.
Its also important to note that I used the same function for both pacman and other agents, but
differentiated by toggling the isMax() variable to either true or false.
Once in the valueRecursion() function, we do most of the work. First, we iterate through the 
the legal actions. Next, we update the depth and index to prepare for the recursive call. Then, 
we make the recursive call with updated depth, index, and a successor given our action, and store that value.
If we're pacman, we keep saving the action that corresponds to the max value. If we're the other
agenets, we keep saving the action that corresponds to the min value. We can then return this best
value and best action to extract.

3. Alpha-Beta Pruning. The only difference between this and minimax is after our recursive call.
Essentially, if we're pacman, we early return if our value (from recursion) is already better than beta.
If it's not, we update alpha and move along. If we're the other agents, we early return if our value
is already better than alpha. If it's not, we update beta and move along. This portion of the code was
taken directly from slides during week 4.

4. Expectimax. The only difference between this and minimax is also after our recursive call.
Pacman will still keep saving the action that corresponds to the max value. However, the other agents
will average over the values of all actions from that current state (which are equally likely). This is
also inspired from slides during week 4.

5. Evaluation Function. This better evaluation function is only minorly different than the
original one. The original one got all points except for 1 (not high enough score). That means
I had to alter ever so slightly. The only other thing in the game that I thought was relevant
are the capsules. Therefore, I just subtracted the total number of capsules and was able to hit
the average score requirement. I chose to subtract TOTAL capsules rather than 1/total capsules
or min distance to capsules because this makes it such that pacman tends to take the capsule
if he is in a situation where ghosts are less than 4 squares away from him AND he doesn't
chase capsules (since total capsules is a fairly constant value) directly. We will want him to mostly
rely on where the closest food is.