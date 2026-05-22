import argparse
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError

class KafkaTopicManager:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

    def list_topics(self):
        topics = self.admin.list_topics()
        return topics