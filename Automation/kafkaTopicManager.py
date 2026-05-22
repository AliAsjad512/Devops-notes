import argparse
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError

class KafkaTopicManager:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

    def list_topics(self):
        topics = self.admin.list_topics()
        return topics
    def create_topic(self, name, partitions=1, replication_factor=1):
        topic = NewTopic(name=name, num_partitions=partitions, replication_factor=replication_factor)
        try:
            self.admin.create_topics([topic])
            print(f"✅ Topic '{name}' created")
        except TopicAlreadyExistsError:
            print(f"⚠️ Topic '{name}' already exists")
    def delete_topic(self, name):
        try:
            self.admin.delete_topics([name])
            print(f"🗑️ Topic '{name}' deleted")
        except UnknownTopicOrPartitionError:
            print(f"❌ Topic '{name}' not found")
