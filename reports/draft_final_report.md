# Taxation and Evolution in Sugarscape
### By Vicky McDermott and Emily Lepert

### Abstract


_________________________________________________________

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

Each agent starts out at a random location on the Sugarscape with a starting amount of sugar deterimned by the minimum and maximum values from above. We choose a random value between those two values.

Every time step, an agent moves by looking at the cells around it with the maximum distance of a cell being that agent's vision value. It then finds the empty cell with the greatest amount of sugar and moves to that cell. It collects the sugar from that cell and then its metabolism burns some sugar from the agent's stock.

Agents die when the amount of sugar they have is less than their metabolism or when their death age is reached. 

To move all of the agents, we shuffle the order of the agents and move them one by one. Below is a comparision of the result of our simulation to the paper's.

### Taxation
We then

### Evolution

### Taxation and Evolution

### Changing welfare distribution

## Bibliography
1. sldkjflskdjfs
