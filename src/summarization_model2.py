
# coding: utf-8

# In[1]:


import nltk


# In[3]:


# nltk.download('punkt')


# In[2]:


import numpy as np
import pandas as pd
import re
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import glob
from nltk.tokenize import sent_tokenize


# In[7]:


# !wget http://nlp.stanford.edu/data/glove.6B.zip
# !unzip glove*.zip


# In[3]:


word_embeddings = {}
f = open('glove.6B.100d.txt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()


# In[9]:


# nltk.download('stopwords')


# In[4]:


from nltk.corpus import stopwords
stop_words = stopwords.words('english')


# In[19]:


def get_sentences(tag):
    files = glob.glob("submission_2/Extraction-and-Summarization-of-Tweets/data/tweets/"+tag+"/*")
    sentences = []
    for file in files:
        fd = open(file,"r")
        for line in fd:
            sentences.append(line)
    return sentences


# In[6]:


def sentence_tokenize(tweets):
    sentences = []
    for tweet in tweets:
        sentences.append(sent_tokenize(tweet))
    sentences = [y for x in sentences for y in x]
    return sentences


# In[7]:


def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new


# In[8]:


def text_processing(sentences):
    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
    clean_sentences = [s.lower() for s in clean_sentences]
    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]
    return clean_sentences


# In[9]:


def vector_representations(clean_sentences):
    sentence_vectors = []
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((100,))
        sentence_vectors.append(v)
    return sentence_vectors


# In[10]:


def similarity_matrix(sentence_vectors):
    sim_mat = np.zeros([len(sentence_vectors), len(sentence_vectors)])
    for i in range(len(sentence_vectors)):
        for j in range(len(sentence_vectors)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]
    return sim_mat


# In[11]:


def apply_pagerank(sim_mat):
    nx_graph = nx.DiGraph(sim_mat)
    scores = nx.pagerank(nx_graph)
    return scores


# In[12]:


def summary_extraction(scores,sentences,k):
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    for i in range(k):
        print(ranked_sentences[i][1])


# In[28]:


# tweets = get_sentences("globalwarming")


# In[29]:


# sentences = sentence_tokenize(tweets)


# In[31]:


# clean_sentences = text_processing(sentences)


# In[32]:


# sentence_vectors = vector_representations(clean_sentences)


# In[33]:


# sim_mat = similarity_matrix(sentence_vectors)


# In[34]:


# scores = apply_pagerank(sim_mat)


# In[36]:


# summary_extraction(scores,sentences,5)

