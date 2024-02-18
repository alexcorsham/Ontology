# Ontology

An ontology represents collections of entities, concepts and data by showing the categories they belong to, the
properties they have, and any relations between them.

A simple example ontology is shown in the graph below:

![](ontology.png)

This ontology uses edges that represent either the 'Instance Of' or 'Subclass Of' relationships between entities.
This graph can be represented as a table of edges as shown below:

| Edge Type  | Head Entity | Tail Entity |
| ---------- | ----------- | ----------- |
| SubclassOf | Organism    | Entity      |
| SubclassOf | Animal      | Organism    |
| InstanceOf | Lassie      | Dog         |
| ...        | ...         | ...         |

In addition, an ontology can be used to represent more than just a class tree.
It can be extended to include additional edge types, such as 'Has Attribute', as shown below:

| Edge Type    | Head Entity | Tail Entity    |
| ------------ | ----------- | -------------- |
| HasAttribute | Pufferfish  | Poisonous      |
| HasAttribute | Heihei      | Accident-prone |
| ...          | ...         | ...            |

Taking three arbitrary entities `X`, `Y` and `Z`, these 3 edge types abide by the following rules:

- If `X` is an instance of `Y`, and `Y` is a subclass of `Z`, then `X` is also an instance of `Z`.
  - E.g. if Lassie is an instance of dog, and dog is a subclass of mammal, then Lassie is also an instance of mammal.
- If `X` is a subclass of `Y`, and `Y` is a subclass of `Z`, then `X` is also a subclass of `Z`.
  - E.g. if dog is a subclass of mammal, and mammal is a subclass of animal, then dog is also a subclass of animal.
- If `X` has the attribute `Y`, and `Z` is an instance of `X`, then `Z` also has the attribute `Y`.
  - E.g. if dog has the attribute 4-legged, and Lassie is an instance of dog, then Lassie also has the attribute
    4-legged.
