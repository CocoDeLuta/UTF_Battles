import json
from pathlib import Path

USERS = Path("data/users.json")

class User:

    def __init__(self, name, id):
        self.name = name
        self.id = id
        register(self.name, self.id)

    def __str__(self):
        return self.name + " " + self.id


def register(nick, id):

    new_user = {"name": nick, "id": id, "academics": []}
    # salve o nome e id do usuário em um arquivo json
    with open(USERS, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except:
            data = {"users": []}

    # verifica se o usuario ja esta registrado
    for user in data["users"]:
        if user["id"] == id:
            return

    data["users"].append(new_user)

    with open(USERS, "w", encoding="utf-8") as f:
        try:
            json.dump(data, f)
        except:
            pass
