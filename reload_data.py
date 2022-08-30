import json
import pymorphy2


FILE_NAME = 'data/'



def f0(): #задание 4
    pass


def f1(): #задание 10
    pass


def f2(): # задание7 - мне ч
    with open(FILE_NAME, encoding='utf8') as f:
        a = list(map(lambda s:s.strip().lower(), f.readlines()))
    morph = pymorphy2.MorphAnalyzer()
    ans = []
    for e in a:
        e = e.lower()
        if '(' in e:
            s = e.split()
            x, y = s[0], ' '.join(s[2:])
        else:
            x = e
            y = ''
        res = morph.parse(x)[0]
        try:
            t = res.inflect({'sing'}).word
        except Exception:
            t = x
        d = {}
        d['question'] = t
        d['response'] = x
        d['comment'] = y
        ans.append(d)
    print(ans)
    if input() != 'ok':
        print('canceled')
        return
    with open('data/tests.json') as f:
        file_content = f.read()
        data = json.loads(file_content)

    data['tasks']['task7(1)'].extend(ans)
    data['tasks']['task7(1)'] = list(set(data['tasks']['task7(1)']))
    print(data)
    with open('data/tests.json', 'w') as f:
        json.dump(data, f)
    print('ready')


f2()




