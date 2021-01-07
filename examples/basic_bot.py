# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2017-2021 TwitchIO

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from twitchio.ext import commands

# api token can be passed as test if not needed.
# Channels is the initial channels to join, this could be a list, tuple or callable
bot = commands.Bot(
    irc_token='...',
    api_token='test',
    nick='mysterialpy',
    prefix='!',
    initial_channels=['mysterialpy']
)


# Register an event with the bot
@bot.event
async def event_ready():
    print(f'Ready | {bot.nick}')


@bot.event
async def event_message(message):
    print(message.content)

    # If you override event_message you will need to handle_commands for commands to work.
    await bot.handle_commands(message)


# Register a command with the bot
@bot.command(name='test', aliases=['t'])
async def test_command(ctx):
    await ctx.send(f'Hello {ctx.author.name}')

bot.run()
