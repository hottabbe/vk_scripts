# vkscripts
# Fcomment
# Оставляет "первонахи" в любом паблике
# 0.1
###

import vk
import sys
import random
import time

group_id = ''
comments = []


def idle():
    isClear = False
    try:
        post = api.wall.get(owner_id='-%i' % group_id, count=1)['items'][0]['id']
    except IndexError:
        if not isClear:
            print('Стена пустая,жду постов...')
        isClear = True
        post = 0
    while True:
        try:
            last_post = api.wall.get(owner_id='-%i' % group_id, count=1)['items'][0]['id']
            if post != last_post:
                api.wall.createComment(owner_id='-%i' % group_id, post_id=last_post, message=random.choice(comments))
                print('https://vk.com/wall-%s_%s - Есть комментарий' % (group_id, last_post))
            post = last_post
            time.sleep(0.7)
        except KeyboardInterrupt:
            sys.exit(0)
        except IndexError:
            if not isClear:
                print('Стена пустая,жду постов...')
            isClear = True


if type(group_id) is not str:
    if len(comments) > 0:
        api = vk.API(
            vk.AuthSession(app_id=5821493, user_login=input('login: '), user_password=input('password:'),
                           scope='groups,wall'),
            lang='ru', v='5.85')
        api.stats.trackVisitor()
        idle()
    else:
        print('Комментарии не заполнены\n'
              'Вводите комментарии и нажимайте Enter\n'
              'Когда закончите - нажмите ctrl + c')
        comments_ = []
        try:
            while True:
                comments_.append(input('==>'))
        except KeyboardInterrupt:
            with open('first_comment.py', 'r', encoding='utf-8') as file:
                new = file.read().replace("comments = ['Пахом пидор']", 'comments = %s' % str(comments_))
            with open('first_comment.py', 'w', encoding='utf-8') as file:
                file.write(new)
            sys.exit(0)
else:
    print('Группа не заполнена\n'
          'Вводите id группы и нажмите Enter')
    with open('first_comment.py', 'r', encoding='utf-8') as file:
        new = file.read().replace('group_id = \'\'', 'group_id = %s' % input('==>'))
    with open('first_comment.py', 'w', encoding='utf-8') as file:
        file.write(new)
    sys.exit(0)
