
# pip install pandas metapub
import pandas as pd
from metapub import PubMedFetcher
from datetime import datetime as dt
# from metapub import FindIt

def query_pubmed(query):
    fetch = PubMedFetcher()
    d = dt.now()
    date_today = "20" + d.strftime("%y/%m/%d")
    pmids = fetch.pmids_for_medical_genetics_query(
        query=query,
        since='2020/01/01',
        until = date_today,
        retmax=3
    )

    documents = {}

    for pmid in pmids:
        article = fetch.article_by_pmid(pmid)
        # print("title: ", article.url)
        documents[article.title] = article.abstract
        # break
    # print(fetch.article_by_pmid(pmids[0]).url)
    # return fetch.article_by_pmid(pmids[0]).
    if len(documents) == 0:
        return None
    return documents

# def get_pdf(query):
#     pmid = query_pubmed(query)
#     src = FindIt(pmid)

#     if src.url:
#         print("PDF available: ", src.url)
#     else:
#         print("No access: ", src.reason)
#     return




# query = "what causes hiv aids?"

# query_pubmed(query)
# get_pdf(query)

# for pmid in pmids:
    
# print(articles)
# d = dt.now()
# stime = "20" + d.strftime("%y/%m/%d")
# print(f"date = {stime}")