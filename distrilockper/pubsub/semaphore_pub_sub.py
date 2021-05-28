from distrilockper.pubsub.publish_subscribe import PublishSubscribe


class SemaphorePubSub(PublishSubscribe):
    def __init__(self, service):
        super().__init__(service)
