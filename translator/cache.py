import json
import os


class TranslationCache:

    def __init__(self, cache_path="output/translation_cache.json"):
        self.cache_path = cache_path
        self.cache = {}

        self._load()

    def _load(self):

        if not os.path.exists(self.cache_path):
            return

        with open(
            self.cache_path,
            "r",
            encoding="utf-8"
        ) as f:
            self.cache = json.load(f)

    def _save(self):

        os.makedirs(
            os.path.dirname(self.cache_path),
            exist_ok=True
        )

        with open(
            self.cache_path,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                self.cache,
                f,
                ensure_ascii=False,
                indent=2
            )

    def get(self, text):

        return self.cache.get(text)

    def set(self, text, translation):

        self.cache[text] = translation

        self._save()

    def has(self, text):

        return text in self.cache