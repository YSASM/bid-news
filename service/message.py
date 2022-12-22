import logging

import requests
from config.config import Config


class MessageService(object):
    baseUrl = "http://passat.smbrave.cn"
    ak = "75ee6b009af08597a4379f3146c66bb5"

    @classmethod
    def send_text(cls, message, receiver="jiangyong"):
        sender = Config.get_val("sender", "1000006")

        url = cls.baseUrl + "/message/weixin"
        headers = {"ak": cls.ak}
        data = {
            "sender": sender,
            "type": "text",
            "receiver": receiver,
            "content": message,
        }
        response = requests.post(url=url, headers=headers, data=data)
        logging.info(response.content)


if __name__ == "__main__":
    message = []
    message.append("abc")
    message.append("abc123")
    message.append("abc124")

    MessageService.send_text("\n".join(message))
