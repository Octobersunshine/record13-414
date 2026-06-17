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


if __name__ == '__main__':
    main()
