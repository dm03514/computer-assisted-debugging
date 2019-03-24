# computer-assisted-debugging
Heuristic based debug engine.  A happy medium between structured anomaly detection and unstructured/playbook based debugging.

Computer Assisted Debugging 

Debugging software is a foundational skill for software engineering.  Unfortunately, industry and academia do a poor job of teaching it.  This results in a wide range of skills between effective debuggers and ineffective debuggers. Computer assisted debugging provides a way for effective debuggers to encode their strategies and approaches into executable playbooks, by modeling debugging as a graph.  We see this with artifacts like playbooks. In much the way there are patterns for software construction and playbooks for service operation there exists patterns and playbooks for debugging.  I think as an industry we can do much better job of teaching techniques to assist in debugging.


### Commands

#### Generating Heuristic/Playbook Sequence Graph

```
$ python bin/generate_graph.py examples.provider_strategy:build_for_display
```

#### Generating Heuristic/Playbook Table States

```
$ python bin/generate_graph.py examples.provider_strategy:build_for_display --type=md_table
```

# Playbook Examples

## Deploy

### Playbook
![cad heuristics deploy](https://user-images.githubusercontent.com/321963/54880914-bab73680-4e20-11e9-84a8-0ab20dbd8783.png)
### State Transitions
| Node Name | Evaluator | Query Source | Yes Threshold |
| ------- | --------- | -------- | ----------- |
|LastDeploy < X hours|SingleValueThresholdEvaluator|StubQuery|LastDeploy < X hours|

---

## Provider Outage
### Playbook
![examples provider_strategy](https://user-images.githubusercontent.com/321963/54880855-0d442300-4e20-11e9-95a5-b17a477d42a5.png)

### State Transitions
| Node Name | Evaluator | Query Source | Yes Threshold |
| ------- | --------- | -------- | ----------- |
|Strategy Error Rate > 50%|OneOfManyValuesThresholdEvaluator|StubQuery|Strategy Error Rate > 50%|
|Region Strategy Error Rate > 50%|ManyValuesThresholdEvaluator|StubQuery|Region Strategy Error Rate > 50%|
|Many Customers Error Rate > 50%|ManyValuesThresholdEvaluator|StubQuery|Many Customers Error Rate > 50%|
