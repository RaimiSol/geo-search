#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import spacy
import numpy as np
import syntok.segmenter as segmenter
from flair.models import SequenceTagger
from flair.data import Sentence
flairTagger = SequenceTagger.load('de-ner')


# ## Prepare
# ### Load Spacy model


nlp = spacy.load('de_core_news_sm')


# ### Read reports

pol_df=pd.read_json('policereports.json')


# ## Process
# ### Tokenize with Spacy

pol_df_extended = pol_df.copy()

pol_df_extended['Token'] = pol_df["Content"].apply(lambda doc: nlp(doc) )


# ### Named entity recognition
# Only locations


pol_df_extended["LocationsFromNER"] = pol_df_extended["Token"].apply(
    lambda doc: {ent for ent in doc.ents if ent.label_ == 'LOC' }
)


# ### Sentence offsets

pol_df_extended["SentenceOffsets"] = pol_df_extended["Content"].apply(lambda content: np.asarray([
    list(sent)[0].offset
    for parag in segmenter.analyze(content) 
    for sent in parag 
]+[len(content)]))


# ### NE offsets


pol_df_extended["LocationsOffsets"] = pol_df_extended["LocationsFromNER"].apply(
    lambda locations: np.asarray([location.start_char for location in locations ])
)


# ### Relevant sentence indices

def getRelevantSentenceIndexes(row):
    sentenceOffsets = row[0]
    locationsOffsets = row[1]
    return set((np.searchsorted(sentenceOffsets, locationsOffsets)-1).clip(min=0))
    


pol_df_extended["RelevantSentenceIndexes"] = pol_df_extended[["SentenceOffsets","LocationsOffsets"]].apply(getRelevantSentenceIndexes , axis=1)


# ### Relevant sentences



def pairwise(sequence):
    return np.asarray(list(zip(sequence[:-1],sequence[1:])))


def getRelevantSentences(row):
    contentString = row[0]
    sentenceOffsets = row[1]
    relevantSentenceIndexes = row[2]
    sentenceOffsetPairs = pairwise(sentenceOffsets)
    relevantSentences = []
    for idx in relevantSentenceIndexes:
        start, end = sentenceOffsetPairs[idx]
        relevantSentences.append(Sentence(contentString[start:end], use_tokenizer=True))
    return relevantSentences


pol_df_extended["RelevantSentences"] = pol_df_extended[["Content","SentenceOffsets", "RelevantSentenceIndexes"]].apply(getRelevantSentences , axis=1)




def getLocationsFromFlair(relevantSentences):
    predictions = flairTagger.predict(relevantSentences)
    named_entities = []
    for p in predictions:
        current_spans = p.get_spans('ner')
        for span in current_spans:
            if(span.tag=='LOC'):
                named_entities.append(span.text) 
    return set(named_entities)


# ## Mini-Batch processing

start = 400
for end in range(500,pol_df.shape[0], 100):
    pol_df_extended["LocationFromNERflair"]=pol_df_extended["RelevantSentences"][start:end].apply(getLocationsFromFlair)
    pol_df_extended.to_csv(f"Output/output_{end}.csv")
    start = end

end = pol_df.shape[0]
pol_df_extended["LocationFromNERflair"]=pol_df_extended["RelevantSentences"][start:end].apply(getLocationsFromFlair)
pol_df_extended.to_csv(f"Output/output_{end}.csv")


# ## Result concatenation



frames = []
start = 0
for end in range(100,pol_df.shape[0], 100):
    current_frame = pd.read_csv(f"Output/output_{end}.csv")
    frames.append(current_frame[:][start:end])
    start = end

end = pol_df.shape[0]
current_frame = pd.read_csv(f"Output/output_{end}.csv")
frames.append(current_frame[:][start:end])



result = pd.concat(frames)

