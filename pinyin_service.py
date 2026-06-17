from typing import List, Union
from pypinyin import pinyin, lazy_pinyin, Style


class PinyinService:

    def __init__(self):
        self._style_map = {
            ('full', True): Style.TONE,
            ('full', False): Style.NORMAL,
            ('first', True): Style.FIRST_LETTER,
            ('first', False): Style.FIRST_LETTER,
        }

    def to_pinyin(
        self,
        text: str,
        mode: str = 'full',
        with_tone: bool = False,
        separator: str = ' ',
    ) -> str:
        if mode not in ('full', 'first'):
            raise ValueError("mode must be 'full' or 'first'")

        style = self._style_map[(mode, with_tone)]

        if mode == 'full':
            result = pinyin(text, style=style, heteronym=False)
            pinyin_list = [item[0] for item in result]
        else:
            result = lazy_pinyin(text, style=style)
            pinyin_list = [char[0].lower() if char else '' for char in result]

        return separator.join(pinyin_list)

    def to_pinyin_list(
        self,
        text: str,
        mode: str = 'full',
        with_tone: bool = False,
    ) -> List[List[str]]:
        if mode not in ('full', 'first'):
            raise ValueError("mode must be 'full' or 'first'")

        style = self._style_map[(mode, with_tone)]
        result = pinyin(text, style=style, heteronym=False)

        if mode == 'first':
            result = [[char[0].lower()] if char else [''] for char in result]

        return result

    def full_pinyin(self, text: str, with_tone: bool = False, separator: str = ' ') -> str:
        return self.to_pinyin(text, mode='full', with_tone=with_tone, separator=separator)

    def first_letter(self, text: str, separator: str = '') -> str:
        return self.to_pinyin(text, mode='first', with_tone=False, separator=separator)

    def full_pinyin_with_tone(self, text: str, separator: str = ' ') -> str:
        return self.to_pinyin(text, mode='full', with_tone=True, separator=separator)

    def first_letter_with_tone(self, text: str, separator: str = '') -> str:
        return self.to_pinyin(text, mode='first', with_tone=True, separator=separator)
