# vkscripts
# Fcomment
# Оставляет "первонахи" в любом паблике
# 0.21
###

import vk
import sys
import random
import time
import os
import threading

group_id = []
comments = []
threads = []


def idle(group):
    isClear = False
    try:
        post = api.wall.get(owner_id='-%i' % group, count=1)['items'][0]['id']
    except IndexError:
        if not isClear:
            print('Стена пустая,жду постов...')
        isClear = True
        post = 0
    print('Запущено ожидание постов в группе id%s' % group)
    while True:
        try:
            last_post = api.wall.get(owner_id='-%i' % group, count=1)['items'][0]['id']
            if post != last_post:
                api.wall.createComment(owner_id='-%i' % group, post_id=last_post, message=random.choice(comments))
                print('https://vk.com/wall-%s_%s - Есть комментарий' % (group, last_post))
            post = last_post
            time.sleep(0.7)
        except KeyboardInterrupt:
            sys.exit(0)
        except IndexError:
            if not isClear:
                print('Стена пустая,жду постов...')
            isClear = True


if len(group_id) > 0:
    if len(comments) > 0:
        api = vk.API(
            vk.AuthSession(app_id=5821493, user_login=input('login: '), user_password=input('password:'),
                           scope='groups,wall'),
            lang='ru', v='5.85')
        api.stats.trackVisitor()
        for group in group_id:
            t = threading.Thread(target=idle, args=(group,))
            t.start()
            threads.append(t)
            time.sleep(1)
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
                    new = file.read().replace("comments = []", 'comments = %s' % str(comments_))
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
                new = file.read().replace("group_id = []", "group_id = %s" % str(groups))
            with open('%s/first_comment.py' % os.path.dirname(os.path.abspath(__file__)), 'w',
                      encoding='utf-8') as file:
                file.write(new)
            sys.exit(0)
        else:
            groups.append(text)
