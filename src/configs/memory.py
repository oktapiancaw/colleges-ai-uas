from redis import Redis
from typica import BaseConnection, ConnectionMeta

from src.common import envs


class MainMemory(BaseConnection):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            ConnectionMeta(
                host=envs.REDIS_HOST,
                port=envs.REDIS_PORT,
                database=envs.REDIS_DATABASE,
            ),
            **kwargs
        )

        try:
            self.client = Redis(
                **self._metadata.model_dump(
                    exclude={"uri", "clustersUri", "type_connection", "database"}
                ),
                db=self._metadata.database,
                **kwargs
            )
        except:
            raise

    def add_data(self, name: str, value: str, expired: int = 43200):
        try:
            if self.client == False:
                raise ValueError("Fail connect")

            self.client.set(name=name, value=value, ex=expired)
        except Exception:
            raise

    def get_data(self, name: str):
        try:
            if self.client == False:
                raise ValueError("Fail connect")

            result = self.client.get(name=name)
            return result
        except Exception:
            raise

    def remove_data(self, name: str):
        try:
            if self.client == False:
                raise ValueError("Fail connect")

            self.client.delete(name)
        except Exception:
            raise

    def remove_by_pattern(self, pattern: str):
        try:
            if self.client == False:
                raise ValueError("Fail connect")
            for key in self.client.scan_iter(pattern):
                self.client.delete(key)
        except Exception:
            raise

    def close(self):
        self.client.close()
