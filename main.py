# -----------------------------------------------------------------------------------
# Importações
# -----------------------------------------------------------------------------------
import discord
from discord import app_commands
import os
from discord.ext import commands
import json
import random
import sys
import classes.users as users
from pathlib import Path

# ------------------------------------------------------------------------------------
# Configurações iniciais
# ------------------------------------------------------------------------------------

# token do bot
TOKEN = "MTIxMTQyMTc1MjQ0MjIyNDc1MA.GOC_LH.Z3Sffiu_-wumfGl0NwR-rRCEZWKNnTaKCfbHaM"
PREFIX = "/"

# id do servidor e do canal
SERVER_ID = 1211431587603026012
CHAANNEL_ID = 1211431588366258308

# path dos arquivos
HELP = Path("data/help.txt")
CHAMPIONS = Path("data/champions.txt")
BUILDS = Path("data/items.txt")
RULES = Path("data/rules.txt")
USERS = Path("data/users.json")
ACADEMICS = Path("data/academics.json")

# intenções do bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# inicialização do bot
client = discord.Client(command_prefix=PREFIX, intents=intents)
tree = app_commands.CommandTree(client)

# ----------------------------------------------------------------------------------
# Ações do bot
# ----------------------------------------------------------------------------------


# quando o bot estiver pronto, ele vai enviar uma mensagem no servidor
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=SERVER_ID))
    # identificar o id do canal que o bot vai enviar a mensagem
    channel = client.get_channel(CHAANNEL_ID)
    # enviar a mensagem
    await channel.send("Olá, eu sou o bot agiota de rinha, e já estou de pé")
    await channel.send("Utilize **/help** para ver os comandos disponíveis")


@tree.command(
    name="salve",
    description="Responde com uma saudação",
    guild=discord.Object(id=SERVER_ID),
)
async def salve(interaction):
    user_nickname = interaction.user.display_name
    await interaction.response.send_message("Salve, " + user_nickname + "!")


@tree.command(
    name="boneco",
    description="Escolhe um boneco aleatório pra proxima partida do lol",
    guild=discord.Object(id=SERVER_ID),
)
async def boneco(interaction):
    with open(CHAMPIONS, "r", encoding="utf-8") as f:
        champions = f.readlines()
        champion = random.choice(champions)
        await interaction.response.send_message("Quero que jogue com: " + champion)


@tree.command(
    name="build",
    description="Escolhe uma build aleatória pra proxima partida do lol",
    guild=discord.Object(id=SERVER_ID),
)
async def build(interaction):
    # escolhe 5 itens aleatórios
    with open(BUILDS, "r", encoding="utf-8") as f:
        items = f.readlines()
        build = random.sample(items, 5)
        await interaction.response.send_message("".join(build))


@tree.command(
    name="help",
    description="Exibe ajudas e tutoriais",
    guild=discord.Object(id=SERVER_ID),
)
async def help(interaction):
    # envia o que esta no arquivo help.txt
    with open(HELP, "r", encoding="utf-8") as f:
        help = f.read()
        # Envolva o conteúdo em um bloco de código para evitar a formatação do Markdown
        await interaction.response.send_message(help)


@tree.command(
    name="register",
    description="Registra um usuário no torenio de batalha",
    guild=discord.Object(id=SERVER_ID),
)
async def register(interaction):
    # cria um novo usuário
    nome = interaction.user.display_name
    id = interaction.user.id
    # o bot manda uma mensagem para teste com o nome e id do usuário
    await interaction.response.send_message("Nome: " + nome + " ID: " + str(id))
    user = users.User(nome, id)


@tree.command(
    name="catch",
    description="Caso esteja registrado, captura um acadêmico",
    guild=discord.Object(id=SERVER_ID),
)
async def catch(interaction):
    # verifica se o usuário esta registrado
    id = interaction.user.id
    try:
        with open(USERS, "r", encoding="utf-8") as f:
            data = json.load(f)
            for user in data["users"]:
                # verifica se o usuario ja esta registrado
                if user["id"] == id:
                    # se estiver registrado, recolhe as informa coes dos monstros disponiveis
                    with open(ACADEMICS, "r", encoding="utf-8") as f:
                        academics = json.load(f)
                        for academic in academics["academics"]:
                            # sortear um monstro baseado na chance de captura de cada um
                            chance = random.randint(0, 100)
                            await interaction.response.send_message(
                                " Você encontrou um " + academic["name"] + "!"
                            )

                            # verifica se o usuario ja tem o monstro
                            if academic not in user["academics"]:

                                if chance <= academic["chance"]:
                                    await interaction.response.send_message(
                                        "Você capturou um " + academic["name"] + "!"
                                    )
                                    user["academics"].append(academic)
                                    with open("users.json", "w") as f:
                                        json.dump(data, f)
                                    return
                            else:
                                await interaction.response.send_message(
                                    "Ah não! Você encontrou um "
                                    + academic["name"]
                                    + " mas já o possui!"
                                )
                                return
                        await interaction.response.send_message(
                            "Você não encontrou nenhum monstro!"
                        )
                    return
            await interaction.response.send_message(
                "Você ainda não está registrado, utilize /register para se registrar"
            )

    except:
        await interaction.response.send_message(
            "Parece que ocorreu um erro, tente novamente mais tarde ou contate o suporte!"
        )


# rodar o bot
client.run(TOKEN)
