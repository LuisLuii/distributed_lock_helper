import asyncio

class Asyncer(object):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
