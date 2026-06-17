import unicodedata
from pypinyin import pinyin, Style


NEUTRAL_TONE_CHARS = {
    '了': 'le',
    '的': 'de',
    '地': 'de',
    '得': 'de',
    '吗': 'ma',
    '呢': 'ne',
    '吧': 'ba',
    '啊': 'a',
    '呀': 'ya',
    '哇': 'wa',
    '嘛': 'ma',
    '么': 'me',
    '啦': 'la',
    '咯': 'lo',
    '呗': 'bei',
    '嘞': 'lei',
}


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


def _has_tone_mark(py):
    tone_chars = 'āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ'
    return any(c in tone_chars for c in py.lower())


def _get_phrase_pinyin_map(text):
    py_results = pinyin(text, style=Style.TONE, heteronym=False)
    py_map = []
    chars = list(text)
    py_idx = 0
    i = 0
    while i < len(chars):
        ch = chars[i]
        if _is_cjk_char(ch):
            py_str = py_results[py_idx][0] if (py_idx < len(py_results) and py_results[py_idx]) else ch
            py_map.append((ch, py_str))
            py_idx += 1
            i += 1
        else:
            seg_start = i
            while i < len(chars) and not _is_cjk_char(chars[i]):
                i += 1
            seg_py = py_results[py_idx][0] if (py_idx < len(py_results) and py_results[py_idx]) else ''
            py_idx += 1
            for j in range(seg_start, i):
                py_map.append((chars[j], chars[j]))
    return py_map


def _resolve_pinyin(ch, py_from_phrase, prev_char=None):
    if not _is_cjk_char(ch):
        return ch
    if ch in NEUTRAL_TONE_CHARS:
        neutral_py = NEUTRAL_TONE_CHARS[ch]
        if py_from_phrase and _has_tone_mark(py_from_phrase):
            if prev_char and _is_cjk_char(prev_char):
                return neutral_py
            return py_from_phrase
        if py_from_phrase and py_from_phrase.lower() == neutral_py.lower():
            return neutral_py
        return neutral_py
    return py_from_phrase if py_from_phrase else ch


def _annotate_chars(text):
    py_map = _get_phrase_pinyin_map(text)
    resolved = []
    for i, (ch, py) in enumerate(py_map):
        prev = py_map[i - 1][0] if i > 0 else None
        resolved_py = _resolve_pinyin(ch, py, prev)
        resolved.append((ch, resolved_py))
    return resolved


def annotate_inline(text):
    parts = []
    for ch, py in _annotate_chars(text):
        if _is_cjk_char(ch):
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
    for ch, py in _annotate_chars(text):
        if _is_cjk_char(ch):
            pinyin_cells.append(_pad_center(py, COL_WIDTH))
            hanzi_cells.append(_pad_center(ch, COL_WIDTH))
        else:
            pinyin_cells.append(ch)
            hanzi_cells.append(ch)
    pinyin_line = ''.join(pinyin_cells)
    hanzi_line = ''.join(hanzi_cells)
    return f"{pinyin_line}\n{hanzi_line}"


def annotate(text, fmt='above', **kwargs):
    if fmt == 'inline':
        return annotate_inline(text)
    if fmt == 'html':
        return annotate_html(text, **kwargs)
    return annotate_above(text)


def annotate_html(text, css=True):
    html_parts = []
    if css:
        html_parts.append(
            '<style>ruby { display: inline-flex; flex-direction: column-reverse; '
            'text-align: center; line-height: 1.2; margin: 0 0.1em; } '
            'rt { font-size: 0.6em; line-height: 1.2; color: #666; } '
            'rp { display: none; }</style>'
        )
    i = 0
    chars = _annotate_chars(text)
    while i < len(chars):
        ch, py = chars[i]
        if _is_cjk_char(ch):
            start = i
            while i < len(chars) and _is_cjk_char(chars[i][0]):
                i += 1
            html_parts.append('<ruby>')
            for j in range(start, i):
                c, p = chars[j]
                html_parts.append(f'{c}<rp>(</rp><rt>{p}</rt><rp>)</rp>')
            html_parts.append('</ruby>')
        else:
            seg_start = i
            while i < len(chars) and not _is_cjk_char(chars[i][0]):
                i += 1
            seg = ''.join(chars[j][0] for j in range(seg_start, i))
            html_parts.append(seg)
    return ''.join(html_parts)


if __name__ == '__main__':
    samples = [
        "你好",
        "中华人民共和国",
        "学习python编程",
        "春天来了，花儿开了。",
        "我的书在桌子上。",
        "他跑得很快。",
        "你好吗？我们走吧！",
        "这是为什么呢？",
        "了解情况的目的",
        "飞快地跑",
        "好得很",
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
        print("【HTML 标注】")
        print(annotate(s, fmt='html'))
        print()
