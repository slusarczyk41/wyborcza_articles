# Analyzing and predicting emotions from internet newspeper articles and comments
I decided to learn more about how deep learning NLP works

## Introduction
I was looking for an idea for a NLP project, so it can be both challenging, so I can learn as much as I can about
natural language processing, and as close as it can be to real life task. I came with an idea that an internet
news publisher would like to know, what can be a response of article they publish on the website. The reason why
that could be useful is that in this example (like at many others) very often just some part of article is available
for everyone - if you want to real all of it you have to buy a premium, which is (I assume) very important from
business perspective.
Because I do not have data about page views/users I decided to use information which is hidden inside comments. I assume
here that the better (stronger) response is, the more subscriptions will be sold. But I think that just two numbers of
comments and likes won't be sufficient so I want to add one more metric - human emotions. As we all know the more
emotionally engaged we are in any topic (take a hobby as an example) the more money we are eager to spend. Hence, the
more emotions some article evokes in us, the more likely we are to buy a premium (and uncover the rest of article).
So I take the standpoint of data scientist in this company and want to answer a question asked by the executive:
> "Which articles will give us the most subscriptions you smart ass?"

## Steps

#### 1. Scrap data
For each old index page (list) of 'newest articles' go to listed url and scrap the article and comments below it. I also found in source code that some of them are labeled as suspicious, so that can be useful in terms of model accuracy. I had also to handle login and premium account, since content of most of those articles is limited to first few paragraphs.

#### 2. Try to label records
The main idea behind most NLP tasks is that we assume that word meaning and word context is the same thing. Thanks to assumption we can analyze text and find a way to define word context in code in such way that it will represents the word meaning. Those definitions (vectors) we can then use to things like calculating word similarities or for a better representation of a word corpus, and both things we will learn in this project.
I want to use this task to learn more about core concepts of NLP.

##### &nbsp;&nbsp;&nbsp;2.1. Singular value decomposition
The fastest and the simple one. By reducing dimension (length) of word
vectors with SVD each row (which represents one word) will shrink so the
values inside has to change. Those vectors should now represent word embedding.


##### &nbsp;&nbsp;&nbsp;2.2. Word2Vec
The idea is the same, but this time to obtain those vectors we will create neural network with just one hidden layer, feed it with pairs train_word - surrounding_word (a Skip Gram model). The hidden layer then becomes our word embedding which tells us about the context for this word.

##### &nbsp;&nbsp;&nbsp;2.3. GloVe



#### 3. Predict emotions from comment
The purpose of this step is to do first steps with tensorflow and NLP. I want to get to know with
this tool and find out what hyperparameters are the best for polish language. I had to filter the input
a bit since the vocabulary size was too huge and couldn't fit vectors into my computer memory.

#### 4. Train model to predict emotions from article
That is the main purpose of this project - be able to know before publishing an article user engagement.

- title
- image
- content (short or long one)
- dummy datetime
- division category
- author category
- media type

##### &nbsp;&nbsp;&nbsp; 4.1. Try to predict three different measures
- what emotions could it
- what is the diversity of emotions
- how many comments will there be
- how many reactions (upvote/downvote) will there be

##### &nbsp;&nbsp;&nbsp; 4.2. Try to predict one combined score
- each emotion has some score
- the more different emotions the better discussion
- the more comments the better
- the more reactions (upvote/downvote) the better reaction

#### 5. Write simple flask API with two endpoints for each model
- take article and comments
- return score from article and statistics from comments

#### 6. Write chrome extension

#### 7. Analyze users by emotions they mostly represent

#### 8. Find people who got paid to write rage comments

features:
- sentiment
- regularity
- connections with other commenters
- vocabulary
- response speed
- posting hours
