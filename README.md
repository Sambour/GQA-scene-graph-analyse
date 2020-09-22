# GQA-scene-graph-analyse
Scene Graph Checking: using scene graph provided by GQA official, check how many such questions are there, where there are multiple objects that satisfy the question context.

For example, for the image below, a question asks who is wearing a shirt. The answer tells “girl”, but obviously the boys are also wearing shirts.

![Image 1](https://github.com/Sambour/GQA-scene-graph-analyse/raw/master/example.jpg)

Our method is to make use of the semantic nodes given from GQA questions. These nodes parse a question in a semantic way using several operations.

For example, for the question mentioned before, “Who is wearing a shirt?” In GQA dataset, it is parsed into 3 steps: first to find shirt in the image, calling “select”, then find the object that has a relation “wearing” with the shirt, called “relate”, and finally we query for this object’s name, called “query”.

Some other operations are listed as below. Here “A” in operations are attributes that could be any descriptive words like “red”, “running”, etc.

operation | usage
--------- | -----
Filter A | Select the objects that match the feature of description from “select” operation.
Verify A/rel | Verify whether the object has the questioned attribute/relation.
Choose A/rel/name | Choose which option given by question fits the object.
Same (A) | If there is an attribute, questions whether the 2 objects have the same attribute; otherwise then questions whether the objects are of same type.
Different (A) | Same as “Same” operation.
Exist | Verify whether the object mentioned in question exists.
Common | Ask what are the objects in common.
And | Like ‘and’ in logic that get the conjunctive of 2 sentences.
Or | Like ‘or’ in logic that get the disjunctive of 2 sentences.

I divided these operations into 3 types. “And” and “or” are conjunctions that only process “True” and “False” following the truth table. “Select”, “relate” and “filter” are to understand the semantic meaning of the question and find the corresponding object(s) that the question requires. The others left are question operations that conduct questions towards the selected objects.

After analyzing the structure of semantic nodes, it would be easier to use these semantic operations to find whether there are multiple objects alleged in the image. The expansion order of the nodes is just the order of the semantic processing. So we could just follow it step by step to see whether there are multiple objects alleged.

In “select” operation, we find all possible objects that have the same name as the selected object. In this step, if the object searches for a general word, there is a lower word dictionary to look up all possible instances. For example, if the question asks for a vehicle, it would find all possible vehicles (bus, track, car, etc.) from the dictionary, and see whether there is one of them in the image.

In “relate” operation, we find all possible objects that not only have the same name as the object required, but also have the same relation to the selected possible objects. Lower word dictionary is also provided here for general words.

In “filter” operation, we traverse all the possible objects, checking whether they have (or have not) attributes required.

In question operation, we check whether the objects selected by former steps could get different answers. If there exists different answers, then we add those answers to the label.
