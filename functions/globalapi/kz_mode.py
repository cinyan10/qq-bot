
def format_kzmode(mode) -> str:
    """return kz_timer, kz_simple or kz_vanilla """
    mode = mode.lower()

    if mode in ('v', 'vnl', 0, 'kz_vanilla'):
        return 'kz_vanilla'
    elif mode in ('s', 'skz', 1, 'kz_simple'):
        return 'kz_simple'
    else:
        return 'kz_timer'


if __name__ == '__main__':
    rs = format_kzmode('SKZ')
    print(rs)

