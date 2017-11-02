# Sugar Evax
### Authors: Emily Lepert and Vicky McDermott
We will extend the SugarScape model to implement a taxation system and evolution. We will be using the paper "Tax and Evolution in SugarScape" to compare our results. We plan on extending the work to introduce a secondary species. 

The experiments we are going to replicate involve building up the sugarscape model described in the paper and incurring a tax on the population. We will compare the population with and without tax and see if we are able to generate the same results as they generated for population of agents over time with and without taxation. We will also compare our results for average metabolism over time with and without taxation. The other experiment we will replicate will involve implementing the sexual reproduction and evolutionary aspects of their model and adding that to our implementation of the replicated sugarscape model.

For our extension, we plan on introducing a secondary species that cannot mate with the original species and vice versa. This species will have the same characteristics as the original agents. We will initially see if there is a difference in the evolution between both species. After, we will introduce attacking or aggressiveness, where an agent can kill another agent of another species and see how they evolve with this new characteristics. The goal of the extension is to simulate more real life characteristics of animals on Earth.

For the replication portion of our project we expect to see these figures (from the original paper).

<img width="425" src="https://github.com/ComplexityVE/SugarEvax/blob/master/images/taxation1.png">  <img  width="425" src="https://github.com/ComplexityVE/SugarEvax/blob/master/images/taxation2.png"> 


The figures above are graphs of the characteristics of agents in a society with taxation implemented. From these results, we conclude that with a taxation system, resources are spread around the system more equally so more agents manage to stay alive. Because there are more agents, the average metabolism of the system is greater than when there are no taxes.


<img width="280" src="https://github.com/ComplexityVE/SugarEvax/blob/master/images/evolution3.png">  <img  width="280" src="https://github.com/ComplexityVE/SugarEvax/blob/master/images/evolution4.png">  <img width="280" src="https://github.com/ComplexityVE/SugarEvax/blob/master/images/evolution5.png">


The figures above are graphs of the characteristics of agents in a society with taxation and evolution implemented. Figure 4 shows us that with reproduction implemented, more agents will be produced in a taxed society. This is because in individuals need to be "healthy" to reproduce, and the greater spread of wealth in a taxed society allows more individuals to be "healthy". Interestingly we see that a non-taxed society will have a higher average vision and wealth. This may be because there are less individuals to average values over and the individuals that are successful in a non-taxed society are ones that have a lot of wealth and high vision.

We anticipate some difficulty in computing results from the model as the paper uses a simulation framework, but we will have to use our laptops. The computation time might be bigger than anticipated.

We will pair program and implement the replication over the next week.


## Bibliography:
### [Tax and Evolution in SugarScape](http://www.cs.vu.nl/~gusz/papers/Tax-and-evolution.ps)
Bäck, Vermeulen, Eiben, S.-H Cheng, P.Wang, Eds., Proceedings of the Second International Workshop on Computational Intelligence in Economics and Financ. JCIS Press, 2002, pp. 1151-1156

This paper implements a SugarScape where taxation on the society and procreation are present. Taxation is implemented so that at each time step, each agent gives up a percentage of their wealth, and the total wealth is redistributed evenly across the population. The percentage taken depends on the wealth of the agent. Evolution is implemented by allowing the agents to reproduce. Each newborn agent gets half of the starting wealth of the father and mother. Its metabolism, vision, age of death, and child bearing age are all influenced by its parents with "Mendelian Rules." The paper finds that with evolution and a taxation system, the sytem has a very high agent population, but lower average wealth, while no taxation or evolution has a low population, but high average wealth. This intuitively makes sense.
