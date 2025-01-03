---
title: Building an AI powered Fantasy Search Engine
date: 2025-01-03
time: 1:22pm
---

I’ve been a fan of Brandon Sanderson’s Fantasy novels for a long time. He is known for creating a vast universe dubbed the “Cosmere” in which many of his stories are interconnected. The various magic systems, characters, and story lines are all part of this world and the lore can get very complicated. My friend and I aimed to create a search engine that will help Brandon Sanderson fans get their cosmere related questions answered. With the goal of having a minimal tech stack we used Flask for our backend / results management and boostrap for styling.

### The Data

After receiving permission from the moderators we decided to use an open-source and fan-maintained website, the Coppermind (coppermind.net), as our data source. We crawled about 100,000 pages from this site and stored all of the data locally in order to reduce the amount of requests made to their website as we process all of the content. 

The crawling was done using a simple python script. It began at the root domain of the website and added any links on that root domain to a queue. As we crawled the pages in the queue, the script continuously looks for links that have not been visited yet and adds them to the queue. We also verify that each link is still within the original coppermind domain before adding it the queue because we want to make sure that the data we are collecting will be relevant to cosmere lore. 

### Whoosh

The backbone of our search engine was created using the whoosh python library. I stuck with a simple schema to be able to identify the file names for later retrieval and I stored the contents of each file inside the whoosh index as well. Here is the schema: 

<pre><code class="language-python">
schema = Schema(
    file_name=ID(stored=True, unique=True),
    cleaned_content=TEXT(stored=True)
)
</code></pre>

Whoosh then iterates over the contents of the coppermind that we crawled earlier. As it does, it calculates the necessary values in order to impliment the **Term Frequency Inverted Document Frequency** **(TD-IDF)** algorithm. [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) is a standard algorithm used in information retrieval that allows for retrieval of relevant documents based on a query. It combines the frequency of a term within a document with the frequency of a term overall to determine which documents are likely to be most relevant given the terms provided in a query. 

Our document retrieval system was created using a combination of Whoosh’s default TF-IDF algorithm with our own implementation of [PageRank](https://www.notion.so/Fantastic-Machine-1602c5fc048a8098a9e0e98e2b4c32e9?pvs=21). The optimal weight distribution after normalizing each score was 30% TF-IDF and 70% pagerank. After some testing with a variety of queries these weights seemed to provide the most relevant documents.

### Related Results (Word2Vec)

Another facet of information retrieval that excited me was training a word2vec model to see what relationships it would identify between different terms within our corpus. I used [gensim’s](https://radimrehurek.com/gensim/models/word2vec.html) word2vec library to train a model on our corpus of data from the coppermind. Using this model, whenever a user makes a query we would take the top 5 most closely related terms to the query and make a secondary query to get a list of results that may be related to the original user’s query. 

It was interesting to experiment and see what terms were closely related. I tested the term *Kaladin* which refers to a main character in Brandon Sanderson’s Stormlight Archive series. The top 5 closely related terms were *Rlain*, *Adolin*, *Lirin*, *Teft*, and *Dalinar*. These are 5 other characters that are part of the same series and all have some sort of relationship with Kaladin. 

### Retrieval-Augmented Generation (RAG) Model

The last aspect of our search engine was the implimentation of the AI RAG model which was done by my partner Noah. To interact with the AI model there is a secondary search bar that the user can submit queries to. Upon submitting the query, we use a model that is similar to word2vec that retrieves 3 relevant chunks of content rather than terms. We then provide these 3 chunks of content as context to an OpenAI API request. The LLM uses the provided context to provide an answer to the question submitted by the user. 

### Conclusion/Postmortem

Working on this project provided me with many great learning experiences. The process of reaching out to the community moderators of the Coppermind and getting their approval to crawl their site taught me about how to use user-agents and how to manage permissions. Testing the different weights when implementing our retrieval system taught me a lot about the differences between different ranking algorithms and how they can be combined to get optimal results. I enjoyed learning about word2vec and seeing it in action as it identified relationships between various terms that are unique to Brandon Sanderson’s novels. Using OpenAI’s API to create a RAG Model helped me better understand the stengths and weaknesses of LLMs as they are now and the necessity to provide quality data in order to get good results.

There are a few things that I would have done differently if I were to do this project again. Doing a better job of cleaning the content on each webpage and identifying what portions of the page are relevant would go a long way in cleaning up our results. Using this cleaned up content I think training an LLM on this set of data would be a cool experiment. We could reach out to the Coppermind community and ask them to help train our LLM.