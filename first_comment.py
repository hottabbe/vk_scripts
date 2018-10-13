# vkscripts
# Fcomment
# Оставляет "первонахи" в любом паблике
# 0.3
###

import os
import random
import sys
import time

import vk

group_id = [ ]
comments = [ ]
threads = []
_api_ = []


def api():
    _appids_ = [5821493, 6063579, 6063581, 6063639, 6477148]
    if len(_api_) == 0:
        __data__ = [input('Введите логин от ВК: '), input('Введите пароль от ВК: ')]
        print('Для обхода ограничений ВК на запросы сделаем несколько авторизаций\n'
              'Не пугайтесь, все норм :)')
        time.sleep(1)
        for _id_ in _appids_:
            print('Авторизация #%i' % (len(_api_) + 1))
            _api_.append(
                vk.API(
                    vk.AuthSession(app_id=_id_, user_login=__data__[0], user_password=__data__[1], scope='groups,wall'),
                    lang='ru', v='5.85'))
            _api_[len(_api_) - 1].stats.trackVisitor()
    else:
        return random.choice(_api_)


def idle():
    post = {}
    last_post = {}
    for group in group_id:
        try:
            post[group] = api().wall.get(owner_id='-%s' % group, count=1)['items'][0]['id']
        except IndexError:
            print('Стена пустая,жду постов...')
            post[group] = 0
        print('Запущено ожидание постов в группе id%s' % group)
    time.sleep(1)
    while True:
        for group in group_id:
            try:
                last_post[group] = api().wall.get(owner_id='-%s' % group, count=1)['items'][0]['id']
                if post[group] != last_post[group]:
                    api().wall.createComment(owner_id='-%s' % group, post_id=last_post[group],
                                             message=random.choice(comments))
                    print('https://vk.com/wall-%s_%s - Есть комментарий' % (group, last_post[group]))
                post[group] = last_post[group]
            except KeyboardInterrupt:
                sys.exit(0)
            except IndexError:
                post[group] = 0
            time.sleep(0.5)


if len(group_id) > 0:
    if len(comments) > 0:
        api()
        idle()
    else:
        print('Комментарии не заполнены\n'
              'Вводите комментарии и нажимайте Enter\n'
              'Когда закончите - нажмите Enter еще раз')
        comments_ = []
        while True:
            text = input('==>')
            if len(text) == 0:
                with open('%s/first_comment.py' % os.path.dirname(os.path.abspath(__file__)), 'r',
                          encoding='utf-8') as file:
                    new = file.read().replace("comments = [ ]", 'comments = %s' % str(comments_))
                with open('%s/first_comment.py' % os.path.dirname(os.path.abspath(__file__)), 'w',
                          encoding='utf-8') as file:
                    file.write(new)
                sys.exit(0)
            else:
                comments_.append(text)
else:
    print('Группа не заполнена\n'
          'Вводите id групп и нажимайте Enter\n'
          'Когда закончите - нажмите Enter еще раз')
    groups = []
    while True:
        text = input('==>')
        if len(text) == 0:
            with open('%s/first_comment.py' % os.path.dirname(os.path.abspath(__file__)), 'r',
                      encoding='utf-8') as file:
                new = file.read().replace("group_id = [ ]", "group_id = %s" % str(groups))
            with open('%s/first_comment.py' % os.path.dirname(os.path.abspath(__file__)), 'w',
                      encoding='utf-8') as file:
                file.write(new)
            sys.exit(0)
        else:
            groups.append(text)
