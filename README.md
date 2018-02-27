# Nlu_Assignment_1
## Runing Files
For generate_token.sh run command <br />
```
bash generate_token.sh
```
For rest of files run command <br />
```
python3 <filename>.py
```
No need to run token_gen_lang_model.py as that is run by generate_token.sh


## Part A:Language Models

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
<br />
<br />
## Part B:Token Generation(random ten tokens) <br />
Examples of some token of length 10 generated :<br />
      1) straight or to witness the hysterical agitations of his very<br />
      2) shall furnish to the millionaire ireton todd is entertaining in<br />
      3) still done with expecting any course must have heard your<br />
      4) came wise men out of the red hair and sir<br />
      5) paumanok where they had no thoughts of his frankness and<br />
      6) soviet embassy is popularly regarded as an administrator willingly or<br />
      <br />
Total time taken 29.42 sec
