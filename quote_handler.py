class QuoteHandler:
    def __init__(self):
        self.quotes = {}

    def handle_quote_add(self, connection, event):
        message = event.arguments[0]
        parts = message.split(maxsplit=2)
        if len(parts) == 3:
            keyword, text = parts[2].split(maxsplit=1)
            self.quotes[keyword] = text
            connection.privmsg(event.target, f"Quote added: {keyword}")

    def handle_quote_retrieve(self, connection, event):
        message = event.arguments[0]
        parts = message.split(maxsplit=1)
        if len(parts) == 2:
            keyword = parts[1].strip()
            if keyword in self.quotes:
                connection.privmsg(event.target, f"Quote for {keyword}: {self.quotes[keyword]}")
            else:
                connection.privmsg(event.target, f"Quote not found for {keyword}")

    def handle_quote_remove(self, connection, event):
        message = event.arguments[0]
        parts = message.split(maxsplit=1)
        if len(parts) == 2:
            keyword = parts[1].strip()
            if keyword in self.quotes:
                del self.quotes[keyword]
                connection.privmsg(event.target, f"Quote removed for {keyword}")
            else:
                connection.privmsg(event.target, f"Quote not found for {keyword}")
