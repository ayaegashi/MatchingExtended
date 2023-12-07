### CS 136 Final Project README
Lily Orgeron and Ayana Yaegashi

## Usage

In the directory with sim.py, to run with default tags:
```bash
python3 sim.py
```
Tags:
```bash
--numMen x
``` 
where "x" is the number of men that will participate in the simulation.
```bash
--numWomen x
```
where "x" is the number of women that will participate in the simulation.
```bash
--numNonBinary x
``` 
where "x" is the number of non-binary people that will participate in the simulation.
```bash
--checkStability
``` 
so that the simulation will also check for stability.
```bash
--numReps x
``` 
where "x" is the number of repetitions the simulation will run to aggregate the data.
```bash
--percentTruthful x
``` 
where "x" is the proportion of agents that are truthful (1 means all agents are truthful, 0 means all agents are strategic. x must be between 0 and 1 inclusive).
```bash
--flex
``` 
to change sexuality distribution from the default uniform random to weighting all-genders the all-genders sexuality more heavily.

Example:
```bash
python3 sim.py --numWomen 10 --numMen 10 --numNonBinary 10 --checkStability --numReps 100 --percentTruthful 0 --flex
``` 
runs the simulation with 10 women, 10 men, 10 non-binary people, checking for stability, for 100 reps, with all agents playing strategically and with sexuality being weighted more heavily toward all-gendered sexuality.

## Output
Running the simulation will first return output from each repetition, which will show which participants are matched and with whom (as well are which are unmatched). If the stability flag is set to true, each repetition will also return if that matching is stable. Average utility per agent is also returned, as well as the percent of participants that are matched. The output ends with aggregated data, such as percent of matches that are stable, average utility over all repetitions, and the average percent of participants that are matched among all repetitions.
