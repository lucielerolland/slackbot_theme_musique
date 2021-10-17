import numpy as np
import pandas as pd
import json
import requests


def pick_theme(db_path):
    themes = pd.read_csv(db_path, header= None)
    themes.columns = ('user', 'theme')
    themes = themes.set_index('user').join(themes.groupby('user')['theme'].count().rename('n_theme')).reset_index()
    themes['weights'] = 1/themes['n_theme']
    themes['weights'] = themes['weights'] / themes['weights'].sum()

    picked_theme_rank = np.random.choice(range(0, len(themes)), size=1, p=themes['weights'])[0]

    return themes.loc[picked_theme_rank, 'theme'], themes.loc[picked_theme_rank, 'user']


def announce_theme(db_path, url):
    picked_theme, picked_user = pick_theme(db_path)
    message = f'''
Debout les campeurs, et haut les coeurs ! Le thème du jour sera...
{picked_theme.capitalize()} ! Proposé par @{picked_user}.\n
Bonne musique !
'''
    json_message = json.dumps({
        "text": message,
    })

    headers = {'Content-type': 'application/json'}
    lets_go = requests.post(url, headers = headers, data = json_message)

if __name__ == '__main__':
    url = 'https://hooks.slack.com/services/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'
    announce_theme('/home/lucie/bot/themes.csv', url)
