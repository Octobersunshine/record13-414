import unicodedata
from pypinyin import pinyin, Style


def _is_cjk_char(ch):
    cp = ord(ch)
    return (0x4E00 <= cp <= 0x9FFF or
            0x3400 <= cp <= 0x4DBF or
            0x20000 <= cp <= 0x2A6DF or
            0x2A700 <= cp <= 0x2B73F or
            0x2B740 <= cp <= 0x2B81F or
            0x2B820 <= cp <= 0x2CEAF or
            0xF900 <= cp <= 0xFAFF or
            0x2F800 <= cp <= 0x2FA1F)


def _char_display_width(ch):
    if unicodedata.east_asian_width(ch) in ('W', 'F'):
        return 2
    return 1


def _pinyin_for_char(ch):
    result = pinyin(ch, style=Style.TONE, heteronym=False)
    if result and result[0]:
        return result[0][0]
    return ch


def annotate_inline(text):
    parts = []
    for ch in text:
        if _is_cjk_char(ch):
            py = _pinyin_for_char(ch)
            parts.append(f"{ch}({py})")
        else:
            parts.append(ch)
    return ''.join(parts)


def _pad_center(s, width):
    s_width = sum(_char_display_width(c) for c in s)
    if s_width >= width:
        return s
    pad_total = width - s_width
    left_pad = pad_total // 2
    right_pad = pad_total - left_pad
    return ' ' * left_pad + s + ' ' * right_pad


def annotate_above(text):
    COL_WIDTH = 6
    pinyin_cells = []
    hanzi_cells = []
    for ch in text:
        if _is_cjk_char(ch):
            py = _pinyin_for_char(ch)
            pinyin_cells.append(_pad_center(py, COL_WIDTH))
            hanzi_cells.append(_pad_center(ch, COL_WIDTH))
        else:
            pinyin_cells.append(ch)
            hanzi_cells.append(ch)
    pinyin_line = ''.join(pinyin_cells)
    hanzi_line = ''.join(hanzi_cells)
    return f"{pinyin_line}\n{hanzi_line}"


def annotate(text, fmt='above'):
    if fmt == 'inline':
        return annotate_inline(text)
    return annotate_above(text)


if __name__ == '__main__':
    samples = [
        "你好",
        "中华人民共和国",
        "学习python编程",
        "春天来了，花儿开了。",
    ]
    for s in samples:
        print("=" * 40)
        print(f"原文: {s}")
        print()
        print("【上方标注】")
        print(annotate(s, fmt='above'))
        print()
        print("【行内标注】")
        print(annotate(s, fmt='inline'))
        print()
