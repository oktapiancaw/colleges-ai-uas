import json

from datetime import datetime
from pydantic import TypeAdapter
from uuid import uuid5, NAMESPACE_URL

import requests

from loguru import logger

from src.common import envs

# from src.configs.memory import MainMemory
from src.models.twitter import (
    Search,
    Timeline,
    FollowingMeta,
    FollowerMeta,
    RequestSchema,
)


class RapidApi:
    def __init__(self) -> None:
        self.url = f"https://{envs.RAPIDAPI_HOST}"
        self.headers = {
            "X-RapidAPI-Key": envs.RAPIDAPI_KEY,
            "X-RapidAPI-Host": envs.RAPIDAPI_HOST,
        }
        # self.redis: MainMemory = redis

    # def save_data(self, sessionId: str, data: dict):
    #     self.redis.add_data(name=sessionId, value=json.dumps(data))

    def search(self, querystring: dict) -> Search | None:
        try:
            payload = RequestSchema(
                uri=f"{self.url}/search.php",
                params=querystring,
                date=datetime.now().strftime("%Y-%m-%d"),
            )

            session_id = str(uuid5(NAMESPACE_URL, payload.model_dump_json()))

            # check = self.redis.get_data(name=session_id)
            # if check:
            #     return TypeAdapter(Search).validate_json(check)

            response = requests.get(
                payload.uri, headers=self.headers, params=payload.params
            )
            data = response.json()

            if data:
                data = Search(**data)
                # self.save_data(session_id, data.model_dump())
                return data
            return None

        except Exception:
            logger.opt(exception=Exception).error("Failed add session")
            raise

    def get_timeline(self, querystring: dict):
        try:
            payload = RequestSchema(
                uri=f"{self.url}/timeline.php",
                params=querystring,
                date=datetime.now().strftime("%Y-%m-%d"),
            )

            session_id = str(uuid5(NAMESPACE_URL, payload.model_dump_json()))

            # check = self.redis.get_data(name=session_id)
            # if check:
            #     return TypeAdapter(Timeline).validate_json(check)

            response = requests.get(
                payload.uri, headers=self.headers, params=payload.params
            )
            data = response.json()

            if data:
                data = Timeline(**data)
                # self.save_data(session_id, data.model_dump())
                return data
            return None

        except Exception:
            logger.opt(exception=Exception).error("Failed add session")
            raise

    def get_following(self, screen_name: str):
        try:
            querystring = {"screenname": screen_name}
            payload = RequestSchema(
                uri=f"{self.url}/following.php",
                params=querystring,
                date=datetime.now().strftime("%Y-%m-%d"),
            )

            session_id = str(uuid5(NAMESPACE_URL, payload.model_dump_json()))

            # check = self.redis.get_data(name=session_id)
            # if check:
            #     return TypeAdapter(FollowingMeta).validate_json(check)

            response = requests.get(
                payload.uri, headers=self.headers, params=payload.params
            )
            data = response.json()

            if data:
                data = FollowingMeta(**data)
                # self.save_data(session_id, data.model_dump())
                return data
            return None
        except Exception:
            logger.opt(exception=Exception).error("Failed add session")
            raise

    def get_followers(self, screen_name: str):
        try:
            querystring = {"screenname": screen_name}
            payload = RequestSchema(
                uri=f"{self.url}/followers.php",
                params=querystring,
                date=datetime.now().strftime("%Y-%m-%d"),
            )

            session_id = str(uuid5(NAMESPACE_URL, payload.model_dump_json()))

            # check = self.redis.get_data(name=session_id)
            # if check:
            #     return TypeAdapter(FollowerMeta).validate_json(check)

            response = requests.get(
                payload.uri, headers=self.headers, params=payload.params
            )
            data = response.json()
            if data:
                data = FollowerMeta(**data)
                # self.save_data(session_id, data.model_dump())
                return data
            return None
        except Exception:
            logger.opt(exception=Exception).error("Failed add session")
            raise
