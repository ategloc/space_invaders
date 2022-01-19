

def my_table():
    signs = []
    signs.append('┌' + '─' * 62 + '┐')
    for i in range(62):
        signs.append('│' + ' ' * 62 + '│')
    signs.append('└' + '─' * 62 + '┘')
    for i in signs:
        print(i)


my_table()
