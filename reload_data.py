import json
import pymorphy2

FILE_NAME = 'data/1.txt'


def f4():  # задание 4 (task4)
    pass


def f10():  # задание 10 (task10)
    with open(FILE_NAME, encoding='utf8') as f:
        a = list(map(lambda s: s.strip().lower(), f.readlines()))
    ans = []
    for e in a:
        e = e.lower()
        if '(' in e:
            s = e.split()
            x, y = s[0], ' '.join(s[2:])
        else:
            x = e
            y = ''
        t = x[:2] + '_' + x[3:]
        d = {}
        d['question'] = t
        d['response'] = x
        d['comment'] = y
        ans.append(d)
    print(ans)
    print('do you agree?')
    if input() != 'ok':
        print('canceled')
        return
    with open('data/tests.json') as f:
        file_content = f.read()
        data = json.loads(file_content)

    data['tasks']['task10'].extend(ans)
    print(data)
    with open('data/tests.json', 'w') as f:
        json.dump(data, f)
    print('ready')


def f7_1():  # задание7 - мн ч  (task7(1))
    with open(FILE_NAME, encoding='utf8') as f:
        a = list(map(lambda s: s.strip().lower(), f.readlines()))
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
    print('do you agree?')
    if input() != 'ok':
        print('canceled')
        return
    with open('data/tests.json') as f:
        file_content = f.read()
        data = json.loads(file_content)

    data['tasks']['task7(1)'].extend(ans)
    print(data)
    with open('data/tests.json', 'w') as f:
        json.dump(data, f)
    print('ready')


def f7_2():  # задание7 - р п мне ч   (task7(2))
    with open(FILE_NAME, encoding='utf8') as f:
        a = list(map(lambda s: s.strip().lower(), f.readlines()))
    ans = []
    for e in a:
        e = e.lower()
        s = e.split(' - ')
        x, y = s[0], s[1]
        d = {}
        d['question'] = x
        d['response'] = y
        d['comment'] = ''
        ans.append(d)
    print(ans)
    if input() != 'ok':
        print('canceled')
        return
    with open('data/tests.json') as f:
        file_content = f.read()
        data = json.loads(file_content)

    data['tasks']['task7(2)'].extend(ans)
    print(data)
    with open('data/tests.json', 'w') as f:
        json.dump(data, f)
    print('ready')



def create_new():
    task_name = None
    info = None
    kod_name = None
    if task_name is None:
        print('failed')
        return
    with open('data/tests.json') as f:
        file_content = f.read()
        data = json.loads(file_content)
    data['tasks'][kod_name] = []
    data["tasks_info"][task_name] = {}
    data["tasks_info"][task_name]['instruction'] = info
    data["tasks_info"][task_name]['name'] = kod_name
    with open('data/tests.json', 'w') as f:
        json.dump(data, f)
    print(data)
    print('ready')


def delete_dublicats(kod_name):
    with open('data/tests.json') as f:
        file_content = f.read()
        data = json.loads(file_content)
    if kod_name not in data['tasks']:
        print('failed')
        return
    mas = []
    ind = []
    for i in range(len(data['tasks'][kod_name])):
        e = data['tasks'][kod_name][i]
        x, y, z = e['question'], e["response"], e['comment']
        if (x, y, z) not in mas:
            mas.append((x, y, z))
        else:
            print(x, y, z)
    res = []
    for x, y, z in mas:
        e = {}

        e['question'], e["response"], e['comment'] = x, y, z
        res.append(e)
    data['tasks'][kod_name] = res
    print(res)
    print(f'{kod_name} complited. do you agree')
    if input() != 'ok':
        print('canceled')
        return
    with open('data/tests.json', 'w') as f:
        json.dump(data, f)
    print(data)
    print('ready', kod_name)


def delete_all_dublicats():
    with open('data/tests.json') as f:
        file_content = f.read()
        data = json.loads(file_content)
    for kod_name in data['tasks']:
        delete_dublicats(kod_name)

f10()

