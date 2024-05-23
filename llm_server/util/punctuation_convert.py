def punctuation_chinese_to_english(target_str):
    punctuation_convert_dict = {
        '：': ': ',
        '，': ', ',
        '。': '. ',
    }
    for key, value in punctuation_convert_dict.items():
        target_str = target_str.replace(key, value)
    return target_str
