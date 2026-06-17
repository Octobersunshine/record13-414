from pinyin_service import PinyinService


def main():
    service = PinyinService()

    test_texts = [
        '你好世界',
        '中华人民共和国',
        'Python编程',
        '天气预报',
    ]

    for text in test_texts:
        print(f'原文: {text}')
        print(f'  全拼(无声调):    {service.full_pinyin(text)}')
        print(f'  全拼(带声调):    {service.full_pinyin_with_tone(text)}')
        print(f'  首字母(无声调):  {service.first_letter(text)}')
        print(f'  首字母(带声调):  {service.first_letter_with_tone(text)}')
        print()

    print('--- 自定义分隔符 ---')
    text = '北京欢迎你'
    print(f'原文: {text}')
    print(f'  全拼(连字符分隔): {service.to_pinyin(text, mode="full", with_tone=False, separator="-")}')
    print(f'  全拼(下划线分隔): {service.to_pinyin(text, mode="full", with_tone=True, separator="_")}')
    print()

    print('--- 获取列表格式 ---')
    text = '好好学习'
    result = service.to_pinyin_list(text, mode='full', with_tone=True)
    print(f'原文: {text}')
    print(f'  带声调列表: {result}')
    print()

    print('=== 多音字处理演示 ===')
    polyphone_tests = [
        ('重庆', 'chóng qìng'),
        ('重庆大学', 'chóng qìng dà xué'),
        ('重量', 'zhòng liàng'),
        ('重要', 'zhòng yào'),
        ('重新', 'chóng xīn'),
        ('长度', 'cháng dù'),
        ('长大', 'zhǎng dà'),
        ('银行', 'yín háng'),
        ('行走', 'xíng zǒu'),
        ('快乐', 'kuài lè'),
        ('音乐', 'yīn yuè'),
        ('爱好', 'ài hào'),
        ('好人', 'hǎo rén'),
        ('睡觉', 'shuì jiào'),
        ('感觉', 'gǎn jué'),
        ('还是', 'hái shì'),
        ('归还', 'guī huán'),
        ('朝阳', 'zhāo yáng'),
        ('朝代', 'cháo dài'),
    ]

    for text, expected in polyphone_tests:
        result = service.full_pinyin_with_tone(text)
        status = '✓' if result == expected else '✗'
        print(f'  {status} {text}: {result}')
    print()

    print('--- 多音字读音查询 ---')
    for char in ['重', '长', '行', '乐', '好']:
        readings = service.get_polyphone_readings(char, with_tone=True)
        print(f'  「{char}」的所有读音: {", ".join(readings)}')
    print()

    print('--- 自定义词典注册 ---')
    print('  注册前:')
    print(f'    人行: {service.full_pinyin_with_tone("人行")}')

    service.register_phrase('人行', [['rén'], ['háng']])
    print('  注册「人行」为 rén háng 后:')
    print(f'    人行: {service.full_pinyin_with_tone("人行")}')


if __name__ == '__main__':
    main()
