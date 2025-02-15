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

from typing import Optional, TYPE_CHECKING

from .abcs import Messageable
from .enums import PredictionEnum

if TYPE_CHECKING:
    from .channel import Channel
    from .user import User
    from .websocket import WSConnection


__all__ = ("PartialChatter", "Chatter")


class PartialChatter(Messageable):

    __messageable_channel__ = False

    def __init__(self, websocket, **kwargs):
        self._name = kwargs.get("name")
        self._ws = websocket
        self._channel = kwargs.get("channel", self._name)

    def __repr__(self):
        return f"<PartialChatter name: {self._name}, channel: {self._channel}>"

    def __eq__(self, other):
        return other.name == self.name and other.channel.name == other.channel.name

    def __hash__(self):
        return hash(self.name + self.channel.name)

    async def user(self) -> "User":
        """|coro|
        Fetches a :class:`twitchio.User` object based off the chatters channel name

        Returns
        --------
            :class:`twitchio.User`
        """
        return (await self._ws._client.fetch_users(names=[self.name]))[0]

    @property
    def name(self):
        """The users name"""
        return self._name

    @property
    def channel(self):
        """The channel associated with the user."""
        return self._channel

    def _fetch_channel(self):
        return self  # Abstract method

    def _fetch_websocket(self):
        return self._ws  # Abstract method

    def _bot_is_mod(self):
        return False


class Chatter(PartialChatter):

    __slots__ = (
        "_name",
        "_channel",
        "_tags",
        "_badges",
        "_ws",
        "id",
        "_turbo",
        "_sub",
        "_mod",
        "_display_name",
        "_colour",
    )

    __messageable_channel__ = False

    def __init__(self, websocket: "WSConnection", **kwargs):
        super(Chatter, self).__init__(websocket, **kwargs)
        self._tags = kwargs.get("tags", None)
        self._badges = kwargs.get("badges", {})
        self._ws = websocket

        if not self._tags:
            self.id = None
            self._turbo = None
            self._sub = None
            self._mod = None
            self._display_name = None
            self._colour = None
            return

        self.id = self._tags.get("user-id")
        self._turbo = self._tags.get("turbo")
        self._sub = self._tags["subscriber"]
        self._mod = int(self._tags["mod"])
        self._display_name = self._tags["display-name"]
        self._colour = self._tags["color"]

    def _bot_is_mod(self):
        cache = self._ws._cache[self._channel.name]  # noqa
        for user in cache:
            if user.name == self._ws.nick:
                try:
                    mod = user.is_mod
                except AttributeError:
                    return False

                return mod

    @property
    def name(self) -> str:
        """The users name. This may be formatted differently than display name."""
        return self._name or (self.display_name and self.display_name.lower())

    @property
    def display_name(self) -> str:
        """The users display name."""
        return self._display_name

    @property
    def colour(self) -> str:
        """The users colour. Alias to color."""
        return self._colour

    @property
    def color(self) -> str:
        """The users color."""
        return self.colour

    @property
    def is_mod(self) -> bool:
        """A boolean indicating whether the User is a moderator of the current channel."""
        if self._mod == 1:
            return True
        if self.channel.name == self.display_name.lower():
            return True
        else:
            return False

    @property
    def is_turbo(self) -> Optional[bool]:
        """A boolean indicating whether the User is Turbo.

        Could be None if no Tags were received.
        """
        return self._turbo

    @property
    def is_subscriber(self) -> Optional[bool]:
        """A boolean indicating whether the User is a subscriber of the current channel.

        Could be None if no Tags were received.
        """
        return self._sub

    @property
    def prediction(self) -> Optional[PredictionEnum]:
        """
        The users current prediction, if one exists.

        Returns
        --------
        Optional[:class:`twitchio.enums.PredictionEnum`]
        """
        if "blue-1" in self._badges:
            return PredictionEnum("blue-1")

        elif "pink-2" in self._badges:
            return PredictionEnum("pink-2")

        return None


class WhisperChatter(PartialChatter):

    __messageable_channel__ = False

    def __init__(self, websocket: "WSConnection", **kwargs):
        super().__init__(websocket, **kwargs)

    def __repr__(self):
        return f"<WhisperChatter name: {self._name}>"

    @property
    def channel(self):
        return None

    def _fetch_channel(self):
        return self  # Abstract method

    def _fetch_websocket(self):
        return self._ws  # Abstract method

    def _bot_is_mod(self):
        return False
