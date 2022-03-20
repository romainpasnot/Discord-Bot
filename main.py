import json
import csv
import requests

# 1) Créer une application sur https://discord.com/developers/applications
# 2) Créér un bot avec les Intents et copier le Token
# 3) Url Generator avec avec scopes Bot + Administrator
# 4) Récuperer le guild ID

TOKEN = "Bot YOUR_TOKEN_HERE"
GUILD_ID = "YOUR_GUILD_ID_HERE"
URL_API = "https://discord.com/api/v9/guilds/"

def call_api(url):
    """
    call_api execute une requete GET vers url et retourne un JSON en dictionnaire

    :param url: adresse url de la requete GET
    :return: reponse JSON en dictionnaire
    """
    response = requests.get(url, headers={"Authorization": TOKEN})
    data = json.loads(response.text)
    return data


def roles_to_dict(data):
    """
    roles_to_dict recupere un reponse JSON pour y extraire les roles (ID + name)

    :param data: reponse JSON en dictionnaire avec les roles
    :return: dictionnaire avec les roles (ID + name)
    """
    data_roles = data["roles"]
    result = {}
    for role in data_roles:
        result[role["id"]] = {"role_name" : role["name"]}
    return result


def members_to_roles(data, dict_roles):
    """
    members_to_roles recupere un reponse JSON pour y extraire les members
    et les ajouters au dictionnaire existant avec les roles (ID + name + members)

    :param data: reponse JSON en dictionnaire avec les members
    :param dict_roles: dictionnaire avec les roles (ID + name)
    :return: dictionnaire avec les roles et members (ID + name + members)
    """
    for user in data:
        for role in user["roles"]:
            if "members" in dict_roles[role]:
                dict_roles[role]["members"].append(user["user"])
            else:
                dict_roles[role]["members"] = [user["user"]]
    return dict_roles


def write_csv(data):
    """
    write_csv ecris un fichier CSV avec le role, l'ID et le username

    :param data: dictionnaire avec en clefs les ID des roles et dedans les members
    """
    with open('result.csv', 'w+', encoding='UTF8') as file:
        header = ['role', 'id', 'username']
        writer = csv.writer(file)
        writer.writerow(header)

        for role in data:
            if "members" in data[role]:
                for member in data[role]["members"]:
                    writer.writerow([data[role]["role_name"], member["id"], member["username"]])


result_roles = roles_to_dict(call_api(URL_API + GUILD_ID))
result_roles = members_to_roles(call_api(URL_API + GUILD_ID + "/members?limit=1000"), result_roles)
write_csv(result_roles)
