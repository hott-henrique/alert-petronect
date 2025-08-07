import os


class KeyValueStorage(object):

    def __init__(self, base_folder: str = "./.data/s3") -> None:
        self.base_folder = base_folder

        os.makedirs(self.base_folder, exist_ok=True)

    def _get_path(self, key: str) -> str:
        return os.path.join(self.base_folder, key)

    def exists(self, key: str) -> bool:
        return os.path.exists(self._get_path(key))

    def load(self, key: str) -> bytes:
        path = self._get_path(key)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Key '{key}' not found in storage.")

        with open(path, "rb") as f:
            return f.read()

    def save(self, key: str, value: bytes) -> None:
        path = self._get_path(key)

        with open(path, "wb") as f:
            f.write(value)
