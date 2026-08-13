from metapub import PubMedFetcher
from datetime import datetime as dt

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
        documents[article.title] = article.abstract
    if len(documents) == 0:
        return None
    return documents
