import configparser
from irc.client import SimpleIRCClient
from quote_handler import QuoteHandler  # import quote handler module

class IRCBot(SimpleIRCClient):
    def __init__(self, config_file):
        super().__init__()
        self.config = self.load_config(config_file)
        self.quote_handler = QuoteHandler()  # initialize quotehandler

    def load_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config['IRC']

    def on_welcome(self, connection, event):
        connection.join(self.config['channel'])

    def on_pubmsg(self, connection, event):
        message = event.arguments[0]
        if message.startswith("!quote add"):
            self.quote_handler.handle_quote_add(connection, event)
        elif message.startswith("!quote "):
            self.quote_handler.handle_quote_retrieve(connection, event)
        elif message.startswith("!quote remove "):
            self.quote_handler.handle_quote_remove(connection, event)

    def run(self):
        server = self.config['server']
        port = int(self.config.get('port', 6667))
        nickname = self.config['nickname']

        self.connect(server, port, nickname)
        self.start()

    def on_ready(self, connection, event):
        connection.execute_at("JOIN", self.config['channel'])

if __name__ == "__main__":
    config_file = "bot_config.ini"
    bot = IRCBot(config_file)
    try:
        bot.run()
    except KeyboardInterrupt:
        bot.connection.quit("Bot is shutting down")
