from typing import Annotated

import typer
import pandas as pds

from loguru import logger
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


from .base import client

app = typer.Typer()


@app.command()
def main(
    topic: Annotated[str, typer.Option()], pages: Annotated[int, typer.Option()] = 1
):
    logger.info(f"searching for {topic}")
    cursor = None
    payload = []
    for _ in range(pages):
        params = {"query": topic}
        if cursor:
            params["cursor"] = cursor
        raw_data = client.search(params)
        for raw in raw_data.timeline:
            payload.append(
                {"user": raw.screen_name, "text": raw.text, "lang": raw.lang}
            )
        logger.info(f"Success get {len(raw_data.timeline)} data")
        cursor = raw_data.next_cursor

    df = pds.DataFrame(payload)
    print(df)


@app.command()
def frequency(
    topic: Annotated[str, typer.Option()], pages: Annotated[int, typer.Option()] = 1
):
    logger.info(f"searching for {topic}")
    cursor = None
    payload = []
    for _ in range(pages):
        params = {"query": topic}
        if cursor:
            params["cursor"] = cursor
        raw_data = client.search(params)
        for raw in raw_data.timeline:
            payload.append(
                {"user": raw.screen_name, "text": raw.text, "lang": raw.lang}
            )
        logger.info(f"Success get {len(raw_data.timeline)} data")
        cursor = raw_data.next_cursor

    df = pds.DataFrame(payload)
    print(df.groupby("lang").describe())


@app.command()
def frequency(
    topic: Annotated[str, typer.Option()], pages: Annotated[int, typer.Option()] = 1
):
    logger.info(f"searching for {topic}")
    cursor = None
    payload = []
    for _ in range(pages):
        params = {"query": topic}
        if cursor:
            params["cursor"] = cursor
        raw_data = client.search(params)
        for raw in raw_data.timeline:
            payload.append(
                {"user": raw.screen_name, "text": raw.text, "lang": raw.lang}
            )
        logger.info(f"Success get {len(raw_data.timeline)} data")
        cursor = raw_data.next_cursor

    df = pds.DataFrame(payload)
    print(df.groupby("lang").describe())


@app.command()
def classification(
    whos: Annotated[list[str], typer.Option()],
    pages: Annotated[int, typer.Option()] = 1,
    lang: Annotated[str, typer.Option()] = None,
):
    cursor = None
    break_loop = False
    payload = []
    for who in whos:
        logger.info(f"searching for {who}")
        for _ in range(pages):
            if break_loop:
                break
            params = {"query": who}
            if cursor:
                params["cursor"] = cursor
            raw_data = client.search(params)
            for raw in raw_data.timeline:
                if lang and raw.lang == lang:
                    payload.append({"who": who, "text": raw.text})
                else:
                    payload.append({"who": who, "text": raw.text})
            cursor = raw_data.next_cursor
            if not cursor:
                break_loop = True

    df = pds.DataFrame(payload)

    logger.info("Describe data:")
    print(df.describe())

    logger.info("Head data:")
    print(df.head())

    corpus = df["text"].to_list()
    vectorizer = TfidfVectorizer(stop_words="english")
    predictor = vectorizer.fit_transform(corpus)

    targets = df["who"]

    x_train, x_test, y_train, y_test = train_test_split(
        predictor, targets, test_size=0.3j
    )

    logger.info("Training model...")

    print(x_train.shape)
    print(x_test.shape)

    classifier = GaussianNB().fit(x_train.toarray(), y_train)

    prediction = classifier.predict(x_test.toarray())

    logger.info("Confusion matrix:")
    print(confusion_matrix(y_test, prediction))

    logger.info("Accuracy score:")
    print(accuracy_score(y_test, prediction))

    logger.info("Classification report:")
    print(classification_report(y_test, prediction))


@app.command()
def clustering(
    whos: Annotated[list[str], typer.Option()],
    pages: Annotated[int, typer.Option()] = 1,
    lang: Annotated[str, typer.Option()] = None,
):
    cursor = None
    break_loop = False
    payload = []
    for who in whos:
        logger.info(f"searching for {who}")
        for _ in range(pages):
            if break_loop:
                break
            params = {"query": who}
            if cursor:
                params["cursor"] = cursor
            raw_data = client.search(params)
            for raw in raw_data.timeline:
                if lang and raw.lang == lang:
                    payload.append({"text": raw.text})
                else:
                    payload.append({"text": raw.text})
            cursor = raw_data.next_cursor
            if not cursor:
                break_loop = True

    df = pds.DataFrame(payload)

    logger.info("Describe data:")
    print(df.describe())

    logger.info("Head data:")
    print(df.head())

    corpus = df["text"].to_list()
    vectorizer = TfidfVectorizer(stop_words="english")
    predictor = vectorizer.fit_transform(corpus)

    model = KMeans(n_clusters=3)
    model.fit(predictor)
    prediction = model.predict(predictor)

    logger.info("Prediction:")
    print(prediction)

    payload = []
    for i in range(0, prediction.size):
        payload.append({"text": df["text"][i], "prediction": prediction[i]})

    result = pds.DataFrame(payload)

    logger.info("Cluster 1:")
    print(result.loc[result["prediction"] == 0].head(10))
    logger.info("Cluster 2:")
    print(result.loc[result["prediction"] == 1].head(10))
    logger.info("Cluster 3:")
    print(result.loc[result["prediction"] == 2].head(10))
