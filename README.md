# Nlu_Assignment_1
## Language Models

Using Brown and Gutenburg corpus from nltk.
For simple bi-gram backoff:<br />
      Train Data = 90% of total corpus <br />
      Test Data = 10% of total corpus

For katz's backoff bi_gram model:<br />
      Train Data = 80% of total corpus<br />
      Development Data = 10% of total corpus<br />
      Test Data = 10% of total corpus

|Test Data|Perpexilityuisng simple back-off back-off model|Perpexility using katz's backoff bi-gram model|
|---------|----------------------------------------|--------------------------------------|
|Brown Corpus(Train1+Test1)|299.0379|233.7419|
|Gutenburg Corpus(Train2+Test2)|128.0240|113.9109|
|Train1+Train2 and testing on Test1|307.8040|278.3778|
|Train1+Train2 and testing on Test2|135.1297|115.5543|

Time taken by simple backoff model : 43.01 sec<br />
Time taken by katz's backoff model(includes hyperparameter tuning) : 646.69 sec 
