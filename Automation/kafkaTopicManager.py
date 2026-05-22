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
    def get_topic_details(self, name):
        try:
            metadata = self.admin.describe_topics([name])
            return metadata
        except:
            return None
    if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kafka Topic Manager')
    parser.add_argument('--bootstrap', default='localhost:9092')
    parser.add_argument('--action', choices=['list', 'create', 'delete', 'describe'], required=True)
    parser.add_argument('--topic', help='Topic name')
    parser.add_argument('--partitions', type=int, default=1)
    parser.add_argument('--replication', type=int, default=1)
    args = parser.parse_args()

    manager = KafkaTopicManager(args.bootstrap)
    if args.action == 'list':
        topics = manager.list_topics()
        for t in topics:
            print(t)
    elif args.action == 'create':
        manager.create_topic(args.topic, args.partitions, args.replication)
    elif args.action == 'delete':
        manager.delete_topic(args.topic)
    else:
        details = manager.get_topic_details(args.topic)
        print(details)
