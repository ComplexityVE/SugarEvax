# Taxation and Evolution in Sugarscape
### By Vicky McDermott and Emily Lepert

## Abstract
We replicated the work done in the paper by implementing taxation and evolution systems in our sugarscape model. With the same parameters used in the paper and a few tweaks to our model we were able to see results that were qualitatively similar to the ones in the paper. We then extended on the work they had done by experimenting with what would happen when the welfare given out from the collected taxes was given in proportional amounts to agents with varying amounts of sugar instead of just splitting up the welfare sugar equally between all agents. We found that the population as a whole does just about the same or even better when the welfare sugar is divided equally as opposed to when different percentages of it are given to different wealth brackets.
_________________________________________________________

## Introduction

## Replication

### Sugarscape
We replicate the first experiment done by Bäck, Vermeulen, and Eiben([1](#Bibliography)). We simulate agents living in Sugarscape with no taxation or evolution system present. The characteristics of the world are as follows:
| Characteristic | Value |
| ----- | ----|
| Height of the world | 50 |
| Width of the world | 50 |
| Number of agents | 400 |
| Sugar growth rate (α) | 1 |
| Replacement | off |
| Minimum metabolism | 1 |
| Maximum metabolism | 4 |
| Minimum vision | 1 |
| Maximum vision | 6 |
| Minimum initial sugar | 5 |
| Maximum initial sugar | 25 |
| Minimum death age | 99998 |
| Maximum death age | 100000 |

Using these values we build the Sugarscape. The metabolism, vision, initial sugar, and death age of the agents are determined using the minimum and maximum values given above. We choose a random value between each minimum and maximum for each agent.

Each agent starts out at a random location on the Sugarscape with a starting amount of sugar determined by the minimum and maximum values from above. We choose a random value between those two values.

Every time step, an agent moves by looking at the cells around it with the maximum distance of a cell being that agent's vision value. It then finds the empty cell with the greatest amount of sugar and moves to that cell. It collects the sugar from that cell and then its metabolism burns some sugar from the agent's stock.

Agents die when the amount of sugar they have is less than their metabolism or when their death age is reached.

To move all of the agents, we shuffle the order of the agents and move them one by one. Below is a comparision of the result of our simulation to the paper's.

### Taxation
Next, we implemented a taxation system on the agents in our model following the same rules specified in the paper. We took taxes from the agents proportional to their wealth at these rates:
| Wealth Between | Base Amount | Additional Taxation |
| ------- | ------- | ------- |
| 0 - 5 | 0 | 30% |
| 5 - 12 | 1.5 | 40% |
| 12 - 20 | 4.8 | 50% |
| 20 - \infty | 10 | 60% |
We then added up the total taxation in the environment and gave each agent welfare equal to the total amount of sugar collected from taxation divided by the total number of agents. We found that doing this produced results that were qualitatively similar to the paper but it seemed as if the taxation system in the paper was less generous because larger populations of our agents were surviving. This can be seen in the graph below.
<img width="280" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/noevol_noredist_govttakesnone.png">
Because they did not fully specify how the welfare was awarded in the paper, we decided to try subtracting a percentage of the sugar from the total taxation collected before dividing it up to give out as welfare. This seemed to produce results that were more similar to the results from the original paper as can be seen below.
<img width="280" src="https://raw.githubusercontent.com/ComplexityVE/SugarEvax/master/images/noevol_noredist.png">


### Evolution

| Characteristic | Value |
| ----- | ----|
| Height of the world | 50 |
| Width of the world | 50 |
| Number of agents | 400 |
| Sugar growth rate (α) | 1 |
| Replacement | off |
| Minimum metabolism | 1 |
| Maximum metabolism | 4 |
| Minimum vision | 1 |
| Maximum vision | 6 |
| Minimum initial sugar | 50 |
| Maximum initial sugar | 100 |
| Minimum death age | 60 |
| Maximum death age | 100 |
| Minimum begin child bearing age | 12 |
| Maximum begin child bearing age | 15 |
| Minimum end child bearing age male | 50 |
| Maximum end child bearing age male | 60 |
| Minimum end child bearing age female | 40 |
| Maximum end child bearing age male | 50 |

### Taxation and Evolution

## Extension

### Changing welfare distribution

## Bibliography
1. sldkjflskdjfs
