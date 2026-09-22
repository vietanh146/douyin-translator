import json

from google import genai
from google.genai import types

from translator.translator import Translator
from translator.cache import TranslationCache

from dotenv import load_dotenv


class GeminiTranslator(Translator):

    def __init__(self):
        load_dotenv()
        self.client = genai.Client()
        self.cache = TranslationCache()

    def translate(self, text: str) -> str:

        prompt = f"""
Bạn là công cụ dịch phụ đề video.

Dịch đoạn tiếng Trung sau sang tiếng Việt.

Yêu cầu:
- Chỉ trả về bản dịch tiếng Việt.
- Không giải thích.
- Không phân tích.
- Giữ nguyên ý nghĩa và sắc thái.
- Ưu tiên cách dịch tự nhiên cho phụ đề video.

Tiếng Trung:
{text}
"""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return response.text.strip()

    def translate_batch(self, texts: list[str]) -> list[dict]:

        items = []

        for i, text in enumerate(texts):
            items.append({
                "id": i,
                "text": text
            })

        input_json = json.dumps(
            items,
            ensure_ascii=False,
            indent=2
        )

        prompt = f"""
Bạn là công cụ dịch phụ đề video.

Hãy dịch tất cả các đoạn tiếng Trung dưới đây sang tiếng Việt.

QUY TẮC:
- Mỗi id phải có đúng một bản dịch.
- Không bỏ sót id nào.
- Giữ nguyên thứ tự id.
- Không thêm id mới.
- Chỉ dịch nội dung.
- Không giải thích.
- Không phân tích.
- Không thêm "Bản dịch:".
- Dịch tự nhiên, phù hợp với phụ đề video.
- Không gộp nhiều câu thành một câu.
- Không thay đổi ý nghĩa.

Dữ liệu:
{input_json}
"""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer"
                            },
                            "translation": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "id",
                            "translation"
                        ]
                    }
                }
            )
        )

        return json.loads(response.text)

    def translate_batch_with_cache(
        self,
        texts: list[str]
    ) -> list[str]:

        translations = [None] * len(texts)

        texts_to_translate = []
        indexes = []

        # Kiem tra cache
        for i, text in enumerate(texts):

            cached = self.cache.get(text)

            if cached is not None:
                translations[i] = cached

            else:
                texts_to_translate.append(text)
                indexes.append(i)

        print(
            f"Cache hit: "
            f"{len(texts) - len(texts_to_translate)}"
        )

        print(
            f"Can dich: "
            f"{len(texts_to_translate)}"
        )

        # Tat ca deu co trong cache
        if not texts_to_translate:
            return translations

        # Goi Gemini cho cac text chua co
        results = self.translate_batch(
            texts_to_translate
        )

        # Luu ket qua
        for result, index in zip(
            results,
            indexes
        ):

            translation = result["translation"]

            translations[index] = translation

            self.cache.set(
                texts[index],
                translation
            )

        return translations