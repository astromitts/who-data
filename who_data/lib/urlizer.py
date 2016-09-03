from unidecode import unidecode


def urlize(str_in):
    url_name_chars = []
    prev_c = ''
    safe_c = ''
    if str_in:
        for char in str_in.strip():
            if char and char.isalnum():
                safe_c = unidecode(char).lower()
                url_name_chars.append(safe_c)
            elif (char == ' ' or not char.isalnum()) and prev_c != '-':
                safe_c = '-'
                url_name_chars.append(safe_c)
            prev_c = safe_c
        urlname = ''.join(url_name_chars)
        if urlname.endswith('-'):
            urlname = urlname[:-1]
        return urlname
    return None
