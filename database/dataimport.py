#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import re 


pol_df = pd.read_csv('flairresult.csv')



pol_df["District"] = pol_df["Header"].str.extract(
    r"""(Mitte|Friedrichshain *- *Kreuzberg|Pankow|Charlottenburg *- *Wilmersdorf|Spandau|Steglitz *- *Zehlendorf|Tempelhof *- *Schöneberg|Neukölln|Treptow *- *Köpenick|Marzahn *- *Hellersdorf|Lichtenberg|Reinickendorf)""")
pol_df.loc[pol_df["District"].isnull(),"District"] = pol_df[pol_df["District"].isnull()]["Content"].str.extract(
    r"""(Mitte|Friedrichshain *- *Kreuzberg|Pankow|Charlottenburg *- *Wilmersdorf|Spandau|Steglitz *- *Zehlendorf|Tempelhof *- *Schöneberg|Neukölln|Treptow *- *Köpenick|Marzahn *- *Hellersdorf|Lichtenberg|Reinickendorf)""", expand=False)
pol_df["District"] = pol_df["District"].str.replace(" ","")
pol_df["District"] = pol_df["District"].fillna('')


pol_df.head()


# ## Preprocess relevant sentences
# Relevant sentences = Sentences in which Spacy detected locations


def relevantSentencesToList(relevantSentences):
    regexResult= re.findall('Sentence: "(.*?)" - \d+ Tokens', relevantSentences)
    return [sentence for sentence in regexResult]


# ## Normalize columns containing sequences as elements


def normalizeColumn(data, column):
    normalized=pd.DataFrame.from_records(data[column].tolist()).stack().reset_index(level=1, drop=True).rename(column)
    return pd.DataFrame(normalized)


# ## Create dataframes for psql import as tables



relevant_df = pd.DataFrame(pol_df['RelevantSentences'].apply(relevantSentencesToList))
relevant_table = normalizeColumn(relevant_df,'RelevantSentences' )
relevant_table["policereport_id"] = relevant_table.index

policereport_table = pol_df[["URL","Title","Content","Header", "District"]]
policereport_table.reset_index(level=0, inplace=True)

location_df = pd.DataFrame(pol_df['LocationFromNERflair'].apply(lambda loc: eval(loc)))
location_table = normalizeColumn(location_df, 'LocationFromNERflair')
location_table["policereport_id"] = location_table.index


# ## Output to csv


location_table.to_csv("location_psql.csv", index=False)
policereport_table.to_csv("policereport_psql.csv", index=False)
relevant_table.to_csv("relevant_psql.csv", index=False)





