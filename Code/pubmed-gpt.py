from bs4 import BeautifulSoup
from math import ceil
from os import path, remove
from pandas import concat, DataFrame
from requests import get, exceptions
from transformers import pipeline, AutoTokenizer
from datetime import datetime

# downloading the model and tokenizer
detector = pipeline("text-classification", model="roberta-base-openai-detector")
tokenizer = AutoTokenizer.from_pretrained("roberta-base-openai-detector")

# setting the journals to scrape
journals = [
    "Nature",
    "Science",
    "The New England journal of medicine",
    "Radiology",
    "Arch Pathol Lab Med"
]

# build the dataframe that has the search page urls
def make_url(journals, start_year, end_year):
    url_df = DataFrame(columns=["journal", "start_year", "end_year", "url"])
    base_url = "https://pubmed.ncbi.nlm.nih.gov/?"
    for journal in journals:
        y0 = start_year
        while y0 <= end_year:
            y1 = ceil((y0 + 1) / 5) * 5 - 1
            y1 = end_year if y1 > end_year else y1
            url = (
                base_url
                + "term=%22"
                + journal.replace(" ", "%20")
                + "%22%5BJournal%5D%29&filter=simsearch1.fha&size=200&filter=years."
                + str(y0)
                + "-"
                + str(y1)
            )

            soup = BeautifulSoup(get(url).text, "html.parser")
            page = 1
            pages = ceil(int(soup.find("meta", {"name": "log_resultcount"})["content"])/200)
            pages = 5 if pages > 5 else pages
            while page <= pages:
                pg_url = url + "&page=" + str(page)
                x_df = DataFrame(
                    {"journal": journal, "start_year": y0, "end_year": y1, "url": pg_url},
                    index=[0],
                )
                url_df = concat([url_df, x_df], ignore_index=True)
                page += 1
            y0 = y1 + 1
    return url_df

# use the search page urls to get the abstracts and scores
def get_abstracts(url):
    abs_df = DataFrame(
        columns=[
            "journal",
            "year_range",
            "url",
            "article_url",
            "abstract",
            "characters",
            "tokens",
            "segment",
            "score"
        ]
    )
    try:
        soup = BeautifulSoup(get(url).text, "html.parser")
    except exceptions.ConnectionError:
        print("Connection Error. Retrying...")
        soup = BeautifulSoup(get(url).text, "html.parser")
    links = soup.find_all("a", {"class": "docsum-title"})
    for link in links:
        article_url = "https://pubmed.ncbi.nlm.nih.gov" + link.get("href")
        try:
            soup = BeautifulSoup(get(article_url).text, "html.parser")
        except exceptions.ConnectionError:
            print("Connection Error. Retrying...")
            soup = BeautifulSoup(get(article_url).text, "html.parser")
        abstract = soup.find("div", {"class": "abstract"})
        if abstract is None:
            continue
        abstract = abstract.text.strip()[8:].strip()
        tokens = tokenizer.tokenize(abstract)
        if 200 <= len(tokens) <= 512:
            abs_len = len(abstract)
            for length in range(3):
                abstract = abstract[0:abs_len]
                result = None
                try:
                    result = detector(abstract)
                except:
                    print("Detector error with: ", article_url, " with segment: ", 0.5 ** length)
                    print("")
                    continue
                journal = url.split("%22")[1]
                year_range = url.split("years.")[1]
                x_df = DataFrame(
                    {
                        "journal": journal.replace("%20", " "), 
                        "year_range": year_range,
                        "url": url,
                        "article_url": article_url,
                        "abstract": abstract,
                        "characters": abs_len,
                        "tokens": len(tokens),
                        "segment": 0.5 ** length,
                        "score": result[0]["score"] if result[0]["label"] == "Fake" else 1 - result[0]["score"],
                    },
                    index=[0],
                )
                abs_df = concat([abs_df, x_df], ignore_index=True)
                abs_len = int(abs_len / 2)
        else:
            continue
    return abs_df

# running the function to get the initial search page function
url_df = make_url(journals, 1980, 2023)

# if the abstracts.csv file exists, delete it
if path.exists("Data/abstracts.csv"):    
    remove("Data/abstracts.csv")

dt_start = datetime.now()
tot_abs = 0

# running the abstract function on each line of the search page dataframe
for url in url_df["url"]:
    dt_mid = datetime.now()
    abs_df = get_abstracts(url)
    # using headers on first batch
    if not path.exists("abstracts.csv"):
        abs_df.to_csv("abstracts.csv", mode="a", header=True, index=False)
    else:
        abs_df.to_csv("abstracts.csv", mode="a", header=False, index=False)
    dt_end = datetime.now()
    tot_abs += len(abs_df)

    # printing information
    print("URL: ", url)
    print(
        "Segment minutes: ", round((dt_end - dt_mid).seconds / 60, 1), " | ",
        "Total minutes: ", round((dt_end - dt_start).seconds / 60, 1), " | ",
        "Segment abstracts: ", len(abs_df), " | ",
        "Total abstracts: ", tot_abs
    )
