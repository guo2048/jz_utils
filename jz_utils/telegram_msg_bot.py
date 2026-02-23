import datetime
import os
import threading
import urllib
import urllib.request

from jz_utils.singleton import singleton


class TelegramBotPeriodically:
    def __init__(self, bot_id, chat_id, mark="", throttle=5):
        self.bot_id = bot_id
        self.chat_id = chat_id
        self.mark = mark
        self.url_prefix = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=" % (bot_id, chat_id)
        self.buffer = []
        self.send(throttle)
        self.push("bot start!")

    def send(self, throttle=5):
        if self.buffer:
            self.buffer, msg = [], self.buffer
            urllib.request.urlopen(self.__make_req_url("\n".join(msg)))
        threading.Timer(throttle, self.send).start()

    def push(self, msg):
        self.buffer.append(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {msg}")

    def __make_msg(self, msg):
        if self.mark:
            return urllib.parse.quote("[%s] %s" % (self.mark, msg))
        else:
            return urllib.parse.quote(msg)

    def __make_req_url(self, msg):
        return self.url_prefix + self.__make_msg(msg)


@singleton
class SimpleTelegramBot:
    def __init__(self, bot_id=None, chat_id=None, mark=None):
        self.bot_id = bot_id or os.environ.get("TELE_BOT_ID")
        self.chat_id = chat_id or os.environ.get("TELE_CHAT_ID")

        if not self.bot_id or not self.chat_id:
            # 为了向后兼容，如果还在特定项目里，用户可能希望报错更人性化
            raise ValueError(
                "bot_id and chat_id must be provided or set via environment variables (TELE_BOT_ID, TELE_CHAT_ID)"
            )

        self.mark = mark or os.environ.get("RUN_ENV")
        self.url_prefix = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=" % (self.bot_id, self.chat_id)

    def send(self, msg):
        urllib.request.urlopen(self.__make_req_url(msg))

    def __make_msg(self, msg):
        if self.mark:
            return urllib.parse.quote(f"[{self.mark}] {msg}")
        else:
            return urllib.parse.quote(msg)

    def __make_req_url(self, msg):
        return self.url_prefix + self.__make_msg(msg)


if __name__ == "__main__":
    # config = GlobalConfigs.get_tele_config()
    # bot = SimpleTelegramBot(config.bot_id, config.chat_id, mark='test')
    bot = SimpleTelegramBot()
    bot.send("hello world 中文测试")
