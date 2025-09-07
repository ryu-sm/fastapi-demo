import json


def parse_msg(code: str) -> str:
    with open("./messages.json", encoding="utf8", mode="r") as msg:
        msg_data = json.load(msg)
        return msg_data.get(code, code)
