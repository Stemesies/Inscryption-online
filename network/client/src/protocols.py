class Response:
    REQUEST_NICKNAME = "cast.request_nickname"
    SERVER_CLOSED = "broadcast.server_closed"
    OPPONENT_FOUND = "broadcast.opponent_found"
    OPPONENT_LEFT = "broadcast.opponent_left"
    START = "broadcast.start"
    START_TURN = "broadcast.start_turn"
    END_TURN = "broadcast.end_turn"
    CARD_SPAWN = "broadcast.card_spawn"
    CARD_UPDATE = "broadcast.update"
    CARD_DIE = "broadcast.die"


class Request:
    PROVIDE_NICKNAME = "protocol.provide_nickname"
    LEAVE = "protocol.leave"
    CARD_SPAWN = "protocol.card_spawn"
