"""Is my PR ready? bot."""
import csv
import json
import os

import aiohttp
from discord.client import log
from discord.ext.commands import Bot
from graphql.language.parser import parse
from graphql.language.printer import print_ast
from graphql.language.source import Source

# DEBUG
# import logging
# log.setLevel(logging.DEBUG)
# log.addHandler(logging.StreamHandler())


# Secrets....
DISCORD_TOKEN = os.environ["DISCORD"]
GITHUB_TOKEN = os.environ["GITHUB"]
PEOPLE_CSV = os.environ.get("PEOPLE", "people.csv")

URL = "https://api.github.com/graphql"

QUERY = """
{
  organization(login: "HE-Arc") {
    repository(name: "livre-python") {
      name
      pullRequests(last: 20, states: [OPEN]) {
        nodes {
          title
          url
          labels(first: 1) {
            nodes {
              name
            }
          }
          author {
            login
          }
          mergeable
        }
      }
    }
  }
}
"""

HEADERS = {
    "Authorization": f"bearer {GITHUB_TOKEN}",
    "Content-Type": "application/graphql; charset=utf-8"
}


with open(PEOPLE_CSV, "r", newline="") as f:
    reader = csv.reader(f)
    students = {discord: github for _, _, github, discord in reader}


async def execute(query, variables_values=None):
    """Run a GraphQL request on Github."""
    source = Source(query, 'GraphQL request')
    document = parse(source)

    with aiohttp.ClientSession() as session:
        async with session.post(URL,
                                headers=HEADERS,
                                data=json.dumps({
                                    'query': print_ast(document),
                                    'variables': variables_values or {}
                                })) as response:
            assert 200 == response.status, f"{URL}: {response.reason}"
            return await response.json()


async def last_prs(github):
    """Retrieve the last OPEN pull requests of a given user."""
    try:
        data = await execute(QUERY)
        repo = data['data']['organization']['repository']
        nodes = repo['pullRequests']['nodes']
        return [pr
                for pr in nodes
                if pr['author']['login'] == github]
    except KeyError:
        log.exception(data['errors'])
    return None


bot = Bot(command_prefix='?', description=__doc__)


@bot.event
async def on_ready():
    """React to the on ready event."""
    print(f"logging in as {bot.user.name}")


@bot.command(pass_context=True)
async def pr(ctx):
    """Respond to a Pull Request command."""
    github = students.get(ctx.message.author.id, None)
    if github is None:
        await bot.reply(":confused: Tu m'es inconnu.")
    else:
        prs = await last_prs(github)
        if not prs:
            await bot.reply(":hamster: pas de _pull request_.")
        else:
            pr = prs[0]
            label = f"{pr['title']}: <{pr['url']}>"
            if pr['mergeable'] != 'MERGEABLE':
                await bot.reply(f":boom: il y a des conflits!\n{label}")
            elif pr['labels']['nodes'][0]['name'] == 'need rebase':
                await bot.reply(f":broken_heart: rebase?\n{label}")
            else:
                await bot.reply(f":+1: Alles guët!\n{label}")


def main():
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
