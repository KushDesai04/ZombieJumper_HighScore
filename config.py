from os import path

ROOT = path.dirname(path.realpath(__file__))



class Config(object):
    TITLE = 'Zombie Jumper - High Scores'
    DATABASE = path.join(ROOT, "HighScore.db")
    DEBUG = True
    SECRET_KEY = 'HananFokkensPleaseStop!'
