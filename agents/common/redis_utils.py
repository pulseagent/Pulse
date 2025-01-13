import json
from typing import Any, Optional, List, Dict

import redis

from agents.common.config import SETTINGS


class RedisUtils:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, password: Optional[str] = None):
        """
        Initialize the Redis connection.

        :param host: Redis server host.
        :param port: Redis server port.
        :param db: Redis database index.
        :param password: Redis password (if required).
        """
        self.client = redis.StrictRedis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )

    def set_value(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """
        Set a value in Redis.

        :param key: Key name.
        :param value: Value to set.
        :param ex: Expiration time in seconds (optional).
        :return: True if successful, False otherwise.
        """
        try:
            return self.client.set(key, value, ex=ex)
        except redis.RedisError as e:
            print(f"Error setting value: {e}")
            return False

    def get_value(self, key: str) -> Optional[Any]:
        """
        Get a value from Redis.

        :param key: Key name.
        :return: Value if the key exists, None otherwise.
        """
        try:
            return self.client.get(key)
        except redis.RedisError as e:
            print(f"Error getting value: {e}")
            return None

    def delete_key(self, key: str) -> int:
        """
        Delete a key from Redis.

        :param key: Key name.
        :return: Number of keys removed.
        """
        try:
            return self.client.delete(key)
        except redis.RedisError as e:
            print(f"Error deleting key: {e}")
            return 0

    def push_to_list(self, key: str, value: Any, max_length: Optional[int] = None, ttl: int=None) -> None:
        """
        Push a serialized value to a list in Redis.

        :param key: Key name.
        :param value: Value to push (can be a structure).
        :param max_length: Maximum length of the list (optional).
        :param ttl: Time to live in seconds (default 5 days).
        """
        try:
            serialized_value = json.dumps(value)  # Serialize to JSON
            pipe = self.client.pipeline()
            pipe.rpush(key, serialized_value)
            if ttl:
                pipe.expire(key, ttl)
            if max_length is not None:
                pipe.ltrim(key, -max_length, -1)
            pipe.execute()
        except redis.RedisError as e:
            print(f"Error pushing to list: {e}")

    def get_list(self, key: str, start: int = 0, end: int = -1) -> List[Any]:
        """
        Get a range of deserialized elements from a list in Redis.

        :param key: Key name.
        :param start: Start index (inclusive).
        :param end: End index (inclusive).
        :return: List of deserialized elements.
        """
        try:
            raw_list = self.client.lrange(key, start, end)
            return [json.loads(item) for item in raw_list]  # Deserialize JSON
        except redis.RedisError as e:
            print(f"Error getting list: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return []

    def set_hash(self, key: str, mapping: Dict[str, Any]) -> bool:
        """
        Set multiple fields in a Redis hash.

        :param key: Key name.
        :param mapping: Dictionary of field-value pairs.
        :return: True if successful, False otherwise.
        """
        try:
            return self.client.hmset(key, mapping)
        except redis.RedisError as e:
            print(f"Error setting hash: {e}")
            return False

    def get_hash(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get all fields and values from a Redis hash.

        :param key: Key name.
        :return: Dictionary of field-value pairs, or None if the hash does not exist.
        """
        try:
            return self.client.hgetall(key)
        except redis.RedisError as e:
            print(f"Error getting hash: {e}")
            return None

    def add_to_set(self, key: str, *values: Any) -> int:
        """
        Add one or more members to a set.

        :param key: Key name.
        :param values: Values to add.
        :return: Number of elements added to the set.
        """
        try:
            return self.client.sadd(key, *values)
        except redis.RedisError as e:
            print(f"Error adding to set: {e}")
            return 0

    def get_set_members(self, key: str) -> Optional[set]:
        """
        Get all members of a set.

        :param key: Key name.
        :return: Set of members, or None if the key does not exist.
        """
        try:
            return self.client.smembers(key)
        except redis.RedisError as e:
            print(f"Error getting set members: {e}")
            return None

redis_utils = RedisUtils(
    host=SETTINGS.REDIS_HOST,
    port=SETTINGS.REDIS_PORT,
    db=SETTINGS.REDIS_DB,
    password=SETTINGS.REDIS_PASSWORD
)
