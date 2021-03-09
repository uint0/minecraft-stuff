import re
import re_util
import typing
import dataclasses

@dataclasses.dataclass
class BaseMessage:
    """ Represents a generic uncategorized message """
    message: str
    
    @staticmethod
    def from_match(message: str):
        return BaseMessage(message)

@dataclasses.dataclass
class LagMessage(BaseMessage):
    """
    Represents the server reporting it is running behind
    Match: Can't keep up! Is the server overloaded? Running <lag_ms>ms or <!lag_ticks> ticks behind
    """
    lag_ms: int

    @staticmethod
    def from_match(message: str):
        match = re.match(
            r"^Can't keep up! Is the server overloaded\? Running (?P<lag_ms>\d+)ms or (?:\d+) ticks behind$",
            message
        )

        return LagMessage(
            message=message,
            lag_ms=int(match.group('lag_ms'))
        ) if match else None


@dataclasses.dataclass
class ConnectionMessage(BaseMessage):
    """
    Represents the server reporting a new player has connected
    Match: <player>[<local|>][/<netloc>] logged in with entity id <entity_id> at (<coordinates>)
    """
    player: str
    local_player: bool
    netloc: str
    entity_id: int
    coordinates: typing.Tuple[float, float, float]

    @staticmethod
    def from_match(message: str):
        match = re.match(
            r"^(?P<player>" + re_util.RE_PLAYER + r")" +\
            r"(?P<local_player>\[local\])?" +\
            r"\[\/(?P<netloc>" + re_util.RE_IPv4_PORT + r")] logged in with " +\
            r"entity id (?P<entity_id>\d+) at \(" +\
            r"(?P<coord_x>" + re_util.RE_FLOAT + r"), " +\
            r"(?P<coord_y>" + re_util.RE_FLOAT + r"), " +\
            r"(?P<coord_z>" + re_util.RE_FLOAT + r")\)$",
            message
        )

        return ConnectionMessage(
            message=message,
            player=match.group('player'),
            local_player=match.group('local_player') is not None,
            netloc=match.group('netloc'),
            entity_id=int(match.group('entity_id')),
            coordinates=(
                float(match.group('coord_x')),
                float(match.group('coord_y')),
                float(match.group('coord_z'))
            )
        ) if match else None

@dataclasses.dataclass
class DisconnectionMessage(BaseMessage):
    """
    Represents the server reporting a player has left
    Match: <player> lost connection: <reason>
    """
    player: str
    reason: str

    @staticmethod
    def from_match(message: str):
        match = re.match(
            r"^(?P<player>[A-Za-z0-9_]{3,16}) lost connection: (?P<reason>.+)$",
            message
        )

        return DisconnectionMessage(
            message=message,
            player=match.group('player'),
            reason=match.group('reason')
        ) if match else None