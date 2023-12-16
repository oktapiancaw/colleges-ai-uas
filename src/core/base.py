from typing import Annotated

import typer
import requests

from loguru import logger

from src.configs.rapidapi import RapidApi

# from src.configs.memory import MainMemory

app = typer.Typer()
# redis = MainMemory()
client = RapidApi()


@app.command()
def search(
    query: Annotated[str, typer.Option()], cursor: Annotated[str, typer.Option()] = None
):
    logger.info(f"search of {query}")
    params = {"query": query}
    if cursor:
        params["cursor"] = cursor
    search = client.search(params)

    print(search)


@app.command()
def timeline(screen_name: Annotated[str, typer.Option()]):
    logger.info(f"Get timeline of {screen_name}")
    timeline = client.get_timeline(screen_name)

    print(timeline)


@app.command()
def followers(screen_name: Annotated[str, typer.Option()]):
    logger.info(f"Get followers of {screen_name}")
    followers = client.get_followers(screen_name)

    print(followers)


@app.command()
def following(screen_name: Annotated[str, typer.Option()]):
    logger.info(f"Get following of {screen_name}")
    following = client.get_following(screen_name)

    print(following)
