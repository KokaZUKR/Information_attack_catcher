a = ['b', 't', 'c']
b = ['a', 'b', 't', 'c']


def new_news(new_parsed, old_parsed):
    new = []
    for i in new_parsed:
        if i not in old_parsed:
            new.append(i)
    return new


new = new_news(b, a)

print(new)
