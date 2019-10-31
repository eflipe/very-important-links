import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'vil_project.settings')
import django
django.setup()
from vil_app.models import Category, Page # , FrasesRandom
from django.utils import timezone


def populate():
    # dictonario con las páginas que queremos agregar a cada categoría
    # luego, dicc de dicc para nuestras categorias
    vil_pages = [
        {'title': 'I Just Found 12 Bricks',
         'url': 'https://youtu.be/jQmlVEBQYig',
         'views': 128,
         'likes': 1, },
        {'title': 'Congratulations!',
         'url': 'https://youtu.be/oyFQVZ2h0V8',
         'views': 128,
         'likes': 1, },
        {'title': 'Vine ATM card fail',
         'url': 'https://youtu.be/YfNVJkx20ig',
         'views': 129,
         'likes': 2, }
        ]
    musica = [
        {'title': 'IC3PEAK - концерт в Саратове 04.12.2018 (полная версия)',
         'url': 'https://youtu.be/drWXBjWFhJ8',
         'views': 130,
         'likes': 3, },
        {'title': 'Tool Live Philadelphia 1992 Remastered (JC Dobbs) FULL CONCERT',
         'url': 'https://youtu.be/fScQo9jA9VI',
         'views': 133,
         'likes': 3, },
        {'title': 'ＳＡＤ ＴＲＡＰ８．ＭＰ４： ＦＯＲＧＩＶＥ ＭＥ',
         'url': 'https://youtu.be/DNWjmGxAbag',
         'views': 134,
         'likes': 4, },
        {'title': 'DELROY EDWARDS - SLOWED DOWN FUNK VOL. I',
         'url': 'https://www.youtube.com/watch?v=xpTB4dp6p1g',
         'views': 222,
         'likes': 5, },
        {'title': 'R y a n C e l s i u s ° U_SCARE_ME.MP4',
            'url': 'https://soundcloud.com/ryan-celsius/sets/u_scare_me-mp4',
            'views': 222,
            'likes': 15, }
        ]
    otros_etc = [
        {'title': 'Learn Python in 10 Minutes',
         'url': 'http://www.korokithakis.net/tutorials/python/',
         'views': 135,
         'likes': 5,
         },
         ]

    categorias = {'Very-important-videos': {'pages': vil_pages, 'views': 128, 'likes': 64},
                  'Música': {'pages': musica, 'views': 64, 'likes': 32},
                  'Varios etc': {'pages': otros_etc, 'views': 32, 'likes': 16}}
    for cat, cat_data in categorias.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['likes'], p['views'])
    # print out
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print('- {0} - {1} - {2} - {3} - {4} - {5} - {6}'.format(str(c), str(c.views), str(c.likes), str(p), str(p.views), str(p.likes), str(p.fecha_agregado)))


def add_page(cat, title, url, likes, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.likes = likes
    p.fecha_agregado = timezone.now()
    p.save()
    return p


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.likes=likes
    c.views=views
    c.save()
    return c


if __name__ == '__main__':
    print('Empezando la population...')
    populate()
