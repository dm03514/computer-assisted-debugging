# computer-assisted-debugging
Codify, Execute, and Visualize Playbooks.  A happy medium between structured anomaly detection and unstructured/playbook based debugging.

Computer Assisted Debugging Supports:

- Codify playbooks by composing graphs  
- Execute playbooks programmatically  during incidents 
- Common Debugging Heursitcs out of the Box
- Automatic Documentation
- Testability

---

Debugging software is a foundational skill for software engineering.  Unfortunately, industry and academia do a poor job of teaching it.  This results in a wide range of skills between effective debuggers and ineffective debuggers. Computer assisted debugging provides a way for effective debuggers to encode their strategies and approaches into executable playbooks, by modeling debugging as a graph.  We see this with artifacts like playbooks. In much the way there are patterns for software construction and playbooks for service operation there exists patterns and playbooks for debugging.  I think as an industry we can do much better job of teaching techniques to assist in debugging.

The purpose of computer assisted debugging is to allow different individuals to arrive at the same correct root conclusions in the shortest time possible.  In order to accomplish this "Playbooks" are used.  These are artifacts that provide a responder with an approach to arriving at common causes of issues.  

The problem with traditional playbooks are many:

- **Unstructured** - If there even are playbooks, structure often varies widly between teams, services, and companies.  Without a structure, humans are responsible for interpreting and executing playbooks; playbooks are programs and people are computers and, it can (and does) fail spectacularly.
- **Uniform - visually** - Playbook structures may vary wildly between teams, some may be lists, some may refrence images and links.  Standardizing Playbooks support a uniform feel across services, saving potentially precious seconds or minutes during incidents.
- **Executable** - By modeling playbooks as a graph with rules to traverse the graph, a computer can trivially traverse the program and execute the playbooks.  This results in a huge time savings when compared to manually executing playbooks.
- **Testable** - Since playbooks become programs they become trivially tested

Computer assisted debugging is a proof of concept to attempt to address some of the issues with manual debugging by allowing playbooks to be defind as a series of states and executed programmatically.  This achieves a consistent structure supporting sharing of debug techniques between multiple services, teams or companies.  

# Getting Started
Computer Assisted Debugging models playbooks as a Directed Graph.  FirstweEach state is only allowed to transition to one or more states, with the start of the playbook represented by a `Start` node and the end of the playbook represented by the `End` node.  Execution begins at `Starts` and traverses the playbook until `End` is reached.  There are two classes of Nodes other than Start/End:

- `Heuristic` - A common debugging pattern.  A number of these will be exposed by Computer Assisted Debugging, only requiring the end user to specify where to get data, and the thresholds that will be evaluated.
- `Playbook` - A graph that follows the Computer Assisted Debugging rules, enabling evaluation, and automatic documentation generation
- `TransitionEvaluator` - This node contains a `query` and a `comparator`, it is responsible for invoking a `query` and applying the `comparator` to the query results.  It then returns `True|False` based on the comparator results.
- `query` - is an adapter responsible for pulling numeric data from a datasource.  Common datasources are Jenkins, Datadog, ElasticSearch, Prometheus, etc.
- `comparator` - is a function used to evaluate a query result. This is applied to all results returned from the query.
- `Alert` - This node performs an action such as logging or notification whenever it is traversed.

In order to illustrate these concepts consider a common debug hueristic: **Last Deploy**.  The Last Deploy is one of the first things consulted when debugging.  This heursitic looks at the time of the last deploy and check to see if it is within some amount of time (recent).  The recency of the last deploy may be a strong enough signal to rollback on its own, or it may be combined with other signals (such as across the board errors, or errors associated with the changeset that was deployed).

This heuristic looks like:

![cad heuristics deploy](https://user-images.githubusercontent.com/321963/54880914-bab73680-4e20-11e9-84a8-0ab20dbd8783.png)
### State Transitions
| Node Name | Evaluator | Query Source | Yes Threshold |
| ------- | --------- | -------- | ----------- |
|LastDeploy < X hours|SingleValueThresholdEvaluator|StubQuery|LastDeploy < X hours|

Computer Assisted Debugging includes the Deploy heuristic as part of the framework.  Using it requires a `TransitionEvaluator`, which then needs aa `query` and a comparator.  The full configuration required to generate the documentation above is:

```
    deploy_playbook = Deploy(
        last_deploy=SingleValueThresholdEvaluator(
            name='LastDeploy < X hours',
            query=StubQuery(result=False),
            comparator=lambda x: x >= datetime.now() - timedelta(hours=6)
        )
    )
```

A production ready implementation would use a Query that access a real datasource.  A common source of truth for deploy information may be AWS or Jenkins builds.  The framework leaves these adapters up to the end user.  

```
    deploy_playbook = Deploy(
        last_deploy=SingleValueThresholdEvaluator(
            name='LastDeploy < X hours',
            query=JenkinsLastSuccessfulBuildQuery(
              api_url,
              project_name
            ),
            comparator=lambda x: x >= datetime.now() - timedelta(hours=6)
        )
    )
```
Computer Assisted Debugging supports executing any playbook using:

```
       ex = Executor(deploy_playbook)
       ex.run()
```
This will traverse the deploy graph, querying the datasource and comparing the output when an evaluator node is reached, and traversing the rest of the nodes according to their individual rules.

# Playbook Examples

## Provider Outage
### Playbook
![examples provider_strategy](https://user-images.githubusercontent.com/321963/54880855-0d442300-4e20-11e9-95a5-b17a477d42a5.png)

### State Transitions
| Node Name | Evaluator | Query Source | Yes Threshold |
| ------- | --------- | -------- | ----------- |
|Strategy Error Rate > 50%|OneOfManyValuesThresholdEvaluator|StubQuery|Strategy Error Rate > 50%|
|Region Strategy Error Rate > 50%|ManyValuesThresholdEvaluator|StubQuery|Region Strategy Error Rate > 50%|
|Many Customers Error Rate > 50%|ManyValuesThresholdEvaluator|StubQuery|Many Customers Error Rate > 50%|


# Commands

## Generating Heuristic/Playbook Sequence Graph

```
$ python bin/generate_graph.py examples.provider_strategy:build_for_display
```

## Generating Heuristic/Playbook Table States

```
$ python bin/generate_graph.py examples.provider_strategy:build_for_display --type=md_table
```
