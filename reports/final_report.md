# Taxation and Evolution in Sugarscape
### By Vicky McDermott and Emily Lepert

## Abstract
We replicated the work done by Bäck, Vermeulen, and Eiben([1](#Bibliography)) by implementing taxation and evolution systems in a Sugarscape model. With the same parameters used in the paper and a few tweaks to our model we were able to see results that were qualitatively similar to the ones in the paper. We then extended on the work they had done by experimenting with different welfare and taxation brackets. We found that the population as a whole does just about the same or even better when different percentages of it are given to different wealth brackets as opposed to when the welfare sugar is divided equally.
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

To move all of the agents, we shuffle the order of the agents and move them one by one. We run the simulation for 800 time steps. Below is a comparison of the result of our simulation to the paper's.

##### Figure 1a (left) and 1b (right)

<img width="400" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/modelempty.png"> <img width="400" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/taxation1.png">

| Figure 1a | Figure 1b |
| ---- | ---- |
| *Graph of population without evolution or tax over time. Population starts out at 400 agents and drops to approximately 230 in 100 time steps.* | *Bäck, Vermeulen, and Eiben([1](#Bibliography))'s graph of population over time with no evolution and with and without taxation. Population without tax starts out at 400 agents and drops to approximately 240 in 100 time steps.* |

Figure 1a matches very closely the behavior of Figure 1b's "no-tax" line quantitatively. It makes sense for the population to suddenly drop within the first 100 time steps, because there are too many agents for the space and resources provided. The population falls until there are enough resources to support all agents.

### Taxation
Next, we implemented a taxation system on the agents in our model following the same rules and initial conditions specified in the paper. We took taxes from the agents proportional to their wealth at these rates:

| Wealth Between | Base Amount | Additional Taxation |
| ------- | ------- | ------- |
| 0 - 5 | 0 | 30% |
| 5 - 12 | 1.5 | 40% |
| 12 - 20 | 4.8 | 50% |
| 20 - &infin; | 10 | 60% |

We then added up the total taxation in the environment and gave each agent welfare equal to the total amount of sugar collected from taxation divided by the total number of agents. We found that doing this produced results that were qualitatively similar to the paper but it seemed as if the taxation system in the paper was less generous because larger populations of our agents were surviving. In the sugarscape model with no taxation the population dips down and evens out at an average population of about 225. With taxation, the average population of agents evens out at about 375 agents whereas the average population of agents evens out at about 310 agents in the paper's model with taxation. This can be seen in the graph below.

##### Figures 2a(left) and 2b(right)

<img width="400" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/noevol_noredist_govttakesnone.png"> <img width="400" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/taxation1.png">

| Figure 2a | Figure 2b |
| ---- | ---- |
| *Our graph of population over time for a system with taxation.* | **Bäck, Vermeulen, and Eiben([1](#Bibliography))'s graph of population over time for a system with taxation.* |

Because they did not fully specify how the welfare was awarded in the paper, we decided to try subtracting a percentage of the sugar from the total taxation collected before dividing it up to give out as welfare. We tried subtracting various values from the total welfare before settling on a level of 15% because 15% gave us a graph which was quantitatively similar to the graph from the original paper. In the application of our model, we can think of this as the proportion of the taxes that the government might take. This seemed to produce results that were more similar to the results from the original paper as can be seen below. In both our model and the paper's model the average population of agents evens out at about 310 agents when there is taxation.

##### Figures 3a(left) and 3b(right)

<img width="400" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/noevol_noredist.png">  <img width="400" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/taxation1.png">

| Figure 3a | Figure 3b |
| ---- | ---- |
| *Our graph of population over time for a system with taxation and some welfare given to government.* | **Bäck, Vermeulen, and Eiben([1](#Bibliography))'s graph of population over time for a system with taxation.* |

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

Below is the result of our implementation and the paper's implementation:

##### Figures 4a (left) and 4b (right)

<img width="400" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/modelEvPop.png"> <img width="400" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/paperEv4.png">

| Figure 4a | Figure 4b |
| ---- | ---- |
| *Graph of population with evolution and no tax over time. Population oscillates around 400 agents.* | *Bäck, Vermeulen, and Eiben([1](#Bibliography))'s graph of population over time with evolution and with and without taxation. Population without tax oscillates then stabilizes to 500.* |

Figure 4a shows the untaxed, but evolving population oscillating around 400 agents, while Figure 4b shows the population stabilizing to 500. While there is a difference in that stabilizing value, qualitatively, our model is similar to the paper's as it stabilizes to a value that is in the range expected. The fact that more agents survive with evolution rather than dying because of their shorter lifespan is because the evolved population can mate and replace its dead agents. The non evolving population can live forever, but cannot replace any of its agents. Further, the evolving population can pass on the good genes that allowed agents to survive thus increasing the likelihood of the survival of the offspring.

### Taxation and Evolution
To combine taxation and evolution into a single model we use the evolution characteristics with the taxation, sex, evolution rules. Below is a comparison of the result of our implementation and the paper's:

##### Figures 5a (left) and 5b (right)

<img width="400" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/modelEvTaxPop.png"> <img width="400" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/paperEv4.png">

| Figure 5a | Figure 5b |
| ---- | ---- |
| *Graph of population with evolution and with and without tax over time. Population without tax oscillates around 400 agents. Population with tax climbs to 1500 agents in 100 time steps.* | *Bäck, Vermeulen, and Eiben([1](#Bibliography))'s graph of population over time with evolution and with and without taxation. Population without tax oscillates then stabilizes to 500. Population with tax and evolution climbs to approximately 2250 agents in 200 time steps.* |

Figure 5 shows the qualitative similarity between the population that is evolving and is taxed of our model (Figure 5a) and of the paper's (Figure 5b). While our population does not go quite as high as the papers (a difference of 750 agents), the overall behavior is quite similar. As shown above, when taxed, more agents survive. When evolved, more agents survive. It makes sense that when we combine both taxation and evolution, many more agents survive. A combination of agents passing down their good attributes, as well as supporting the poorer agents ensures that more agents have a chance to survive longer.

## Extension

### Changing welfare distribution
For our extension, one thing we explore is adding different welfare brackets. We expect that by giving more of the welfare to the poorer agents and less of it to the richer agents we will be able to significantly increase the average population over time. For our first experiment of this hypothesis, we split the welfare evenly among agents who have less than the average amount of sugar that agents have at that time step instead of simply giving an equal amount of welfare to all agents regardless of how much sugar they have. Running this model with both evolution and taxation produces the following graph. It is interesting to note that with this system of splitting the welfare only amongst the poorer agents, the population of agents does not do as well as it did with purely taxation and evolution. It now seems to oscillate and winds up steadying out around an oscillation of 400 agents while before when we distributed welfare equally among the agents the population climbed to 1400 agents. We suspect that the reason the population did so poorly was because our welfare redistribution system was not complex enough.


<img width="500" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/wealth_redistribution_correct_label.png">

| Figure 6 |
| ---- |
| *Our graph of population over time for a system with evolution, taxation, and one welfare bracket.* |

Next we made our welfare redistribution system slightly more complex by creating 3 different brackets instead of simply dividing the welfare amongst the agents who had less than the mean amount of sugar. We created the brackets by dividing the mean wealth by 3 and adding that number to the mean wealth to get the upper limit of the third bracket and subtracting that number from the mean wealth to get the upper limit of the first bracket. We then gave agents who fell into the first bracket 50% of the welfare to divide evenly amongst themselves. Similarly we gave agents who fell into the second bracket 30% of the welfare to divide evenly amongst themselves and agents who fell into the third bracket the remaining 20% of the welfare to divide evenly amongst themselves. Agents with more sugar than the upper limit of the third bracket did not get any welfare. With this system in place, we ran our model with taxation and no evolution and got the following graph. With our complex system, the average population still steadied out at about 310 agents or maybe a bit higher than that.

<img width="500" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/noevol_withredist.png">

| Figure 7 |
| ---- |
| *Our graph of population over time for a system with taxation and three welfare brackets but no evolution.* |

We ran the same model with both taxation and evolution implemented and got the following graph. With this system in place, the average population spikes up to be be as much as 1800 agents at some times. That said, the average seems to oscillate around about 1500 agents, about 100 agents higher than the average was when welfare was split up equally between all agents.

<img width="500" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/wealth_redistribution_3brackets_labels.png">

| Figure 8 |
| ---- |
| *Our graph of population over time for a system with evolution, taxation, and three welfare brackets.* |

We suspect that the reason that our bracketed welfare redistribution system did not improve the survival rate by much (measured by average population over time) was because we were already taking more from the agents with more sugar in our bracketed taxation system. Taking more and giving less most likely meant that the agents with a medium amount of sugar were not able to survive in our model. This explains the oscillation we are seeing in our graphs and why the welfare redistribution did not have as much of an effect as we might have liked.

## Conclusion
From our findings, we can conclude that including a welfare redistribution system in an evolutionary society where taxes are already being taken from members at a rate proportional to their wealth causes overall survival rates to fluctuate greatly. There might be spikes and drops in population over time but the average value for average population over time does not seem to be much of an improvement from when there was no welfare redistribution system. Future work might involve varying the welfare redistribution system more to see if the behavior persists with different parameters or more wealth brackets. It would also be interesting to investigate the cause for the large oscillations in average population over time.

## Bibliography
1. [Tax and Evolution in SugarScape](http://www.cs.vu.nl/~gusz/papers/Tax-and-evolution.ps)
Bäck, Vermeulen, Eiben, S.-H Cheng, P.Wang, Eds., Proceedings of the Second International Workshop on Computational Intelligence in Economics and Financ. JCIS Press, 2002, pp. 1151-1156

This paper implements a SugarScape where taxation on the society and procreation are present. Taxation is implemented so that at each time step, each agent gives up a percentage of their wealth, and the total wealth is redistributed evenly across the population. The percentage taken depends on the wealth of the agent. Evolution is implemented by allowing the agents to reproduce. Each newborn agent gets half of the starting wealth of the father and mother. Its metabolism, vision, age of death, and child bearing age are all influenced by its parents with "Mendelian Rules." The paper finds that with evolution and a taxation system, the sytem has a very high agent population, but lower average wealth, while no taxation or evolution has a low population, but high average wealth. This intuitively makes sense.

2. [Think Complexity](http://greenteapress.com/complexity2/thinkcomplexity2.pdf)
Downey, Green Tea Press. Needham, Massachussetts, 2017, pp. 147-187

This book describes an implementation of Sugarscape and evolution that we based our model off of.

3. [The Specification of Sugarscape](https://arxiv.org/abs/1505.06012v3)
Kehoe, arXiv:1505.06012v3 [cs.MA] 7 Nov 2016
This paper describes various rules of Sugarscape conventionally used. We used this resource to clarify the reproduction rules.
