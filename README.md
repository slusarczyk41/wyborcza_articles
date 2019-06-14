# Analyzing and predicting emotions from internet newspeper articles and comments

## Introduction

I decided to learn more about how deep learning NLP works

## Steps

#### 1. Scrap data
For each old index page (list) of 'newest articles' go to listed url and scrap the article and comments below it. I also found in source code that some of them are labeled as suspicious, so that can be useful in terms of model accuracy. I had also to handle login and premium account, since content of most of those articles is limited to first few paragraphs.

#### 2. Try to label records
The main idea behind most NLP tasks is that we assume that word meaning and word context is the same thing. Thanks to assumption we can analyze text and find a way to define word context in code in such way that it will represents the word meaning. Those definitions (vectors) we can then use to things like calculating word similarities or for a better representation of a word corpus, and both things we will learn in this project.

##### &nbsp;&nbsp;&nbsp;2.1. Singular value decomposition
The fastest and the simple one. By reducing dimension (length) of word
vectors with SVD each row (which represents one word) will shrink so the
values inside has to change. Those vectors should now represent word embedding.


##### &nbsp;&nbsp;&nbsp;2.2. Word2Vec
The idea is the same, but this time to obtain those vectors we will create neural network with just one hidden layer, feed it with pairs train_word - surrounding_word (a Skip Gram model). The hidden layer then becomes our word embedding which tells us about the context for this word.

##### &nbsp;&nbsp;&nbsp;2.3. GloVe

##### &nbsp;&nbsp;&nbsp;2.4. TF-ITF

##### &nbsp;&nbsp;&nbsp;2.5. K-means


#### 3) Train model to predict emotions from comment

#### 4) Train model to predict emotions from article

#### 5) Write simple flask API with two endpoints for each model

#### 6) Write chrome extension

#### 7) Analyze users by emotions they mostly represent

#### 8) Find people who got paid to write rage comments

features:
- sentiment
- regularity
- connections with other commenters
- vocabulary
- response speed
- posting hours
