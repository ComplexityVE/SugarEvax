# Taxation and Evolution in Sugarscape
### By Vicky McDermott and Emily Lepert

## Abstract
We replicated the work done in the paper by implementing taxation and evolution systems in a Sugarscape model. With the same parameters used in the paper and a few tweaks to our model we were able to see results that were qualitatively similar to the ones in the paper. We then extended on the work they had done by experimenting with what different welfare and taxation brackets. We found that the population as a whole does just about the same or even better when the welfare sugar is divided equally as opposed to when different percentages of it are given to different wealth brackets.
_________________________________________________________

## Replication

### Sugarscape
We replicate the first experiment done by Bäck, Vermeulen, and Eiben([1](#Bibliography)). We simulate agents living in Sugarscape with no taxation or evolution system present. The characteristics of the world are as follows:

| Characteristic | Value | Characteristic | Value |
| ----- | ----| ---- | ----- |
| Height of the world | 50 | Minimum metabolism | 1 |
| Width of the world | 50 | Maximum metabolism | 4 |
| Number of agents | 400 | Minimum vision | 1 |
| Sugar growth rate (α) | 1 | Maximum vision | 6 |
| Replacement | off | Minimum death age | 99998 |
| Minimum initial sugar | 5 | Maximum death age | 100000 |
| Maximum initial sugar | 25 |

Using these values we build the Sugarscape. The metabolism, vision, initial sugar, and death age of the agents are determined using the minimum and maximum values given above. We choose a random value between each minimum and maximum for each agent.

Each agent starts out at a random location on the Sugarscape with a starting amount of sugar determined by the minimum and maximum values from above. We choose a random value between those two values.

Every time step, an agent moves by looking at the cells around it with the maximum distance of a cell being that agent's vision value. It then finds the empty cell with the greatest amount of sugar and moves to that cell. It collects the sugar from that cell and then its metabolism burns some sugar from the agent's stock.

Agents die when the amount of sugar they have is less than their metabolism or when their death age is reached.

To move all of the agents, we shuffle the order of the agents and move them one by one. Below is a comparision of the result of our simulation to the paper's.

### Taxation
Next, we implemented a taxation system on the agents in our model following the same rules and initial conditions specified in the paper. We took taxes from the agents proportional to their wealth at these rates:

| Wealth Between | Base Amount | Additional Taxation |
| ------- | ------- | ------- |
| 0 - 5 | 0 | 30% |
| 5 - 12 | 1.5 | 40% |
| 12 - 20 | 4.8 | 50% |
| 20 - &infin; | 10 | 60% |

We then added up the total taxation in the environment and gave each agent welfare equal to the total amount of sugar collected from taxation divided by the total number of agents. We found that doing this produced results that were qualitatively similar to the paper but it seemed as if the taxation system in the paper was less generous because larger populations of our agents were surviving. In the sugarscape model with no taxation the population dips down and evens out at an average population of about 225. With taxation, the average population of agents evens out at about 375 agents whereas the average population of agents evens out at about 310 agents in the paper's model with taxation. This can be seen in the graph below.

<img width="280" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/noevol_noredist_govttakesnone.png">

Because they did not fully specify how the welfare was awarded in the paper, we decided to try subtracting a percentage of the sugar from the total taxation collected before dividing it up to give out as welfare. We decided to subtract 15% of the total welfare. In the application of our model, we can think of this as the proportion of the taxes that the government might take. This seemed to produce results that were more similar to the results from the original paper as can be seen below. In both our model and the paper's model the average population of agents evens out at about 310 agents when there is taxation.

<img width="280" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/noevol_noredist.png">


### Sex and Evolution
To implement sex and evolution in our model, we change the values of some characteristics and include more. Below is the table with the updated values:

| Characteristic | Value | Characteristic | Value |
| ----- | ----| ----- | ----|
| Height of the world | 50  | Minimum vision | 1 |
| Width of the world | 50  | Maximum vision | 6 |
| Number of agents | 400 | Minimum initial sugar | 50 |
| Sugar growth rate (α) | 1 | Maximum initial sugar | 100 |
| Replacement | off | Minimum death age | 60 |
| Minimum metabolism | 1 | Maximum death age | 100 |
| Maximum metabolism | 4 | Minimum end child bearing age male | 50 |
| Minimum begin child bearing age | 12 | Maximum end child bearing age male | 60 |
| Maximum begin child bearing age | 15 | Minimum end child bearing age female | 40 |
| Maximum end child bearing age male | 50 |

We add reproduction to the model. After an agent moves, it finds all of it's neighbors that are able to mate, mates with them, and produce a new agent (b_agent). 

An agent is able to mate if it meets these requirements:
- It is of child bearing age
- Its current sugar is greater than or equal to the amount of sugar it started with

Two agents mate if they are of opposite sexes. The b_agent they produce is born on a neighboring cell if there is an empty one available. If not, then no new b_agent is created. The b_agent receives sugar from both parents. The amount of sugar each parent donates is equivalent to half of the amount of sugar the parents's initial sugar.

Evolution is added to the model through the values of the characteristics of the b_agents. The gender of the b_agent is randomly chosen. The b_agent's metabolism, vision, age of death, and child bearing age are set by randomly choosing each one from the parent's characteristics. For example, if parent 1 had m,v,d,c as it's genetic makeup, and parent 2 had M,V,D,C, then the b_agent has a 50% chance of getting either values. There are 16 possibilities: (m,V,D,C), (m,v,D,c), (M,V,d,C), etc...

### Taxation and Evolution

## Extension

### Changing welfare distribution
For our extension, one thing we decided to explore was adding different welfare brackets. Instead of simply giving an equal amount of welfare to all agents regardless of how much sugar they had, we instead decided to split the welfare evenly among agents who had less than the mean amount of sugar that agents had. Running this model with both evolution and taxation produced the following graph. It is interesting to note that with this system of splitting the welfare only amongst the poorer agents, the population of agents does not do as well as it did with purely taxation and evolution. It now seems to oscillate and winds up steadying out around an oscillation of 400 agents while before when we distributed welfare equally among the agents the population climbed to 1400 agents.

<img width="280" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/wealth_redistribution.png">

Next we made our welfare redistribution system slightly more complex by creating 3 different brackets instead of simply dividing the welfare amongst the agents who had less than the mean amount of sugar. We created the brackets by dividing the mean wealth by 3 and adding that number to the mean wealth to get the upper limit of the third bracket and subtracting that number from the mean wealth to get the upper limit of the first bracket. We then gave agents who fell into the first bracket 50% of the welfare to divide evenly amongst themselves. Similarly we gave agents who fell into the second bracket 30% of the welfare to divide evenly amongst themselves and agents who fell into the third bracket the remaining 20% of the welfare to divide evenly amongst themselves. Agents with more sugar than the upper limit of the third bracket did not get any welfare. With this system in place, we ran our model with taxation and no evolution and got the following graph. It turned out that even with our complex welfare system, the average population dipped to about 275 agents as compared to when it had only dipped to 310 when we were splitting the welfare equally among all the agents.

<img width="280" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/noevol_withredist.png">

We ran the same model with both taxation and evolution implemented and got the following graph. Although the average population of agents does spike up to be much higher at some points with this bracketed wealth redistribution system it appears that the average population still oscillates around 1400 (or maybe even a little less), the same number of agents that was produced with the taxation and evolution systems in place and a welfare system where welfare was split up equally between all agents.

<img width="280" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/wealth_redistribution_3brackets_labels.png">

We suspect that the reason that our bracketed welfare redistribution system did not improve the survival rate (measured by average population over time) was because we were already taking more from the agents with more sugar in our bracketed taxation system. Taking more and giving less most likely meant that the agents with a medium amount of sugar were not able to survive in our model. This explains the oscillation we are seeing in our graphs and why the welfare redistribution did not work as well as we might have liked.

## Bibliography
1. sldkjflskdjfs
