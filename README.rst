Bookbot
=======

Setup
-----

You need to prepare:

1. a Discord bot
2. a Github Personal Access Token
3. a CSV containing a mapping between the Github handles and the Discord Snowflakes

.. code-block:: csv

   Firstname,Lastname,Github,DiscordID
   ...

Installation
------------

.. code-block:: console

   $ pip install git+https://github.com/greut/bookbot#egg=bookbot
   # the bot token
   $ export DISCORD=...
   # the personal access token
   $ export GITHUB=...
   # the CSV file
   $ export PEOPLE=people.csv
   $ bookbot
