import pandas as pd
import re

# Ler o arquivo CSV
df = pd.read_csv('ClimadoBrasil_5000.csv')


# Remover os primeiros 15 caracteres da coluna 'the_geom'
df['the_geom'] = df['the_geom'].str[16:]

df['the_geom'] = df['the_geom'].str.split(',').str[0]


# Salvar o arquivo CSV atualizado
df.to_csv('clima_brasil_atualizado.csv', index=False)