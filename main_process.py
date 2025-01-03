import os
files = ('main.py', '.gitignore', '.env', '.env.example')
dirs = (
    'services_data',
    'handlers_data',
    'middlewares_data',
    'keyboards_data',
    'lexicon_data',
    'services_data',
    'filters_data',
    'database_data',
    'config_data'
    )

for i in files:
    adress = os.path.join(os.getcwd(), i)
    if os.path.exists(adress) == False:
        with open(adress, 'x') as file:
            pass

for i in dirs:
    adress = os.path.join(os.getcwd(), i)
    if os.path.exists(adress) == False:
        os.mkdir(adress)