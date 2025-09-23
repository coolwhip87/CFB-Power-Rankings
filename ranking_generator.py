import cfbd

with open('collegefootballdata api key.txt', 'r') as file:
    for line in file:
        key=line

configuration = cfbd.Configuration(
    access_token = key
)

with cfbd.ApiClient(configuration) as api_client:
    api_instance = cfbd.GamesApi(api_client)
    games = api_instance.get_games(year=2024)

print(games[1])