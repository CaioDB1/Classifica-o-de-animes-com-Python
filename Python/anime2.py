import requests
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
from datetime import datetime
import calendar



# Lista de animes
animes = [
    "30-sai made Doutei dato Mahoutsukai ni Nareru Rashii",
    "Akuyaku Reijou Level 99: Watashi wa Ura-Boss desu ga Maou dewa Arimasen",
    "Ao no Exorcist: Shimane Illuminati-hen",
    "Boku no Kokoro no Yabai Yatsu Season 2",
    "Bucchigiri?!",
    "Cardfight!! Vanguard: Divinez",
    "Chiyu Mahou no Machigatta Tsukaikata",
    "Chou Futsuu Ken Chiba Densetsu",
    "Dosanko Gal wa Namara Menkoi",
    "Dungeon Meshi",
    "Gekai Elise",
    "Gekkan Mousou Kagaku",
    "Harimaware! Koinu",
    "Heart Cocktail Colorful: Fuyu-hen",
    "High Card Season 2",
    "Hikari no Ou 2nd Season",
    "Himesama 'Goumon' no Jikan desu",
    "Isekai de Mofumofu Nadenade suru Tame ni Ganbattemasu.",
    "Ishura",
    "Jaku-Chara Tomozaki-kun 2nd Stage",
    "Kekkon Yubiwa Monogatari",
    "Kingdom 5th Season",
    "Kyuujitsu no Warumono-san",
    "Loop 7-kaime no Akuyaku Reijou wa, Moto Tekikoku de Jiyuu Kimama na Hanayome Seikatsu wo Mankitsu suru",
    "Mahou Shoujo ni Akogarete",
    "Majo to Yajuu",
    "Mashle 2nd Season",
    "Mato Seihei no Slave",
    "Meiji Gekken: 1874",
    "Meitou 'Isekai no Yu' Kaitakuki: Around 40 Onsen Mania no Tensei Saki wa, Nonbiri Onsen Tengoku deshita",
    "Momochi-san Chi no Ayakashi Ouji",
    "Nozomanu Fushi no Boukensha",
    "Ore dake Level Up na Ken",
    "Oroka na Tenshi wa Akuma to Odoru",
    "Pon no Michi",
    "Saijaku Tamer wa Gomi Hiroi no Tabi wo Hajimemashita.",
    "Saikyou Tank no Meikyuu Kouryaku: Tairyoku 9999 no Rare Skill-mochi Tank, Yuusha Party wo Tsuihou sareru",
    "Sasaki to Pii-chan",
    "Sengoku Youko",
    "Shaman King: Flowers",
    "Shin no Nakama ja Nai to Yuusha no Party wo Oidasareta node, Henkyou de Slow Life suru Koto ni Shimashita 2nd",
    "Snack Basue",
    "Sokushi Cheat ga Saikyou sugite, Isekai no Yatsura ga Marude Aite ni Naranai n desu ga.",
    "Synduality: Noir Part 2",
    "Tsuki ga Michibiku Isekai Douchuu 2nd Season",
    "Urusei Yatsura (2022) 2nd Season",
    "Yami Shibai 12",
    "Youkoso Jitsuryoku Shijou Shugi no Kyoushitsu e 3rd Season",
    "Yubisaki to Renren",
    "Yuuki Bakuhatsu Bang Bravern",
]

# Função para obter dados do anime usando a API Jikan
def get_anime_data(anime_title):
    url = f'https://api.jikan.moe/v4/anime?q={anime_title}&limit=1'
    response = requests.get(url)
    anime_data = response.json()['data'][0] if response.status_code == 200 else None
    return anime_data

# Dicionários para armazenar dados
anime_types = {}
anime_sources = {}
anime_statuses = {}
popularity_data = {}
genres_data = {}
release_dates = defaultdict(list)

# Alterações nas datas de lançamento
release_dates["Jan"].extend([
    ("Ao no Exorcist: Shimane Illuminati-hen", 7),
    ("Urusei Yatsura (2022) 2nd Season", 12),
    ("Cardfight!! Vanguard: Divinez", 13),
    ("Mashle 2nd Season", 6),
])

# Loop através da lista de animes
for anime_title in animes:
    anime_data = get_anime_data(anime_title)

    if anime_data and anime_data['aired']['from']:
        release_date = datetime.strptime(anime_data['aired']['from'], "%Y-%m-%dT%H:%M:%S+00:00")
        release_dates[calendar.month_abbr[release_date.month]].append((anime_title, release_date.day))

    if anime_data:
        # Coletar dados de tipo
        anime_types[anime_title] = anime_data['type'] if 'type' in anime_data else 'Unknown'

        # Coletar dados de fonte
        anime_sources[anime_title] = anime_data['source'] if 'source' in anime_data else 'Unknown'

        # Coletar dados de status
        anime_statuses[anime_title] = anime_data['status'] if 'status' in anime_data else 'Unknown'

        if anime_title == "Ao no Exorcist: Shimane Illuminati-hen":
            anime_data['members'] = 46430
        if anime_title == "Mashle 2nd Season":
            anime_data['members'] = 84620
        if anime_title == "Cardfight!! Vanguard: Divinez":
            anime_data['members'] = 692
        if anime_title == "Urusei Yatsura (2022) 2nd Season":
            anime_data['members'] = 22588

        # Coletar dados de popularidade (com base em members)
        popularity_data[anime_title] = anime_data['members'] if 'members' in anime_data else 0

        # Coletar dados de gêneros
        genres = anime_data['genres'] if 'genres' in anime_data else []
        for genre in genres:
            if genre['name'] in genres_data:
                genres_data[genre['name']] += 1
            else:
                genres_data[genre['name']] = 1

# Criar um gráfico de barras para tipos de anime
plt.figure(figsize=(10, 6))
plt.bar(anime_types.keys(), [1]*len(anime_types), color='lightblue')  # Atribuindo o valor 1 para cada anime
plt.xticks(rotation=45, ha='right')
plt.xlabel('Anime')
plt.ylabel('Tipo')
plt.title('Tipos de Anime')
plt.tight_layout()
plt.show()

# Criar um gráfico de barras para distribuição de fontes
sources_counts = {}
for source in anime_sources.values():
    if source in sources_counts:
        sources_counts[source] += 1
    else:
        sources_counts[source] = 1

plt.figure(figsize=(10, 6))
plt.bar(sources_counts.keys(), sources_counts.values(), color='lightgreen')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Fonte')
plt.ylabel('Número de Animes')
plt.title('Distribuição de Fontes dos Animes')
plt.tight_layout()
plt.show()

# Criar um gráfico de pizza para popularidade (baseado em members)
# Ordenar por popularidade
sorted_popularity_data = dict(sorted(popularity_data.items(), key=lambda item: item[1], reverse=True))

# Agrupar os menos populares em "Outros"
threshold = 15
top_animes = dict(list(sorted_popularity_data.items())[:threshold])
others_total = sum(list(sorted_popularity_data.values())[threshold:])
top_animes['Outros'] = others_total

plt.figure(figsize=(8, 8))
plt.pie(top_animes.values(), labels=top_animes.keys(), autopct='%1.1f%%', startangle=140, textprops={'fontsize': 8})
plt.title('Animes mais aguardados (Baseado nos membros do MAL)')
plt.show()

# Criar um gráfico de barras para gêneros
plt.figure(figsize=(10, 6))
plt.bar(genres_data.keys(), genres_data.values(), color='salmon')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Gênero')
plt.ylabel('Número de Animes')
plt.title('Distribuição de Gêneros dos Animes')
plt.tight_layout()
plt.show()

# Criar uma tabela com os dias exatos de estreias dos animes
def create_anime_table(release_dates):
    df_data = {'Dia': [], 'Animes': []}

    for month, anime_list in release_dates.items():
        for anime_title, day in anime_list:
            df_data['Dia'].append(f"{calendar.month_abbr.index(month):02d}/{day:02d}")
            df_data['Animes'].append(anime_title)

    df = pd.DataFrame(df_data)
    print(df)

create_anime_table(release_dates)
