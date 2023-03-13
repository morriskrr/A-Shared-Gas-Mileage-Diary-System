import pytest
from shared_diary.client.kafka_lib import MileageDiaryProducer



@pytest.fixture
def producer():
	yield MileageDiaryProducer



# TODO add more tests and add docker library to actually test messages
class TestMileageDiaryProducer(object):

	def test_producer_with_different_topics(self, producer):
		test_topics = [" ", "test", "12345", "\\"]
		server = "localhost:9092"

		for topic in test_topics:
			obj = producer
			instance = obj(server, topic)
			assert instance.kafka_topic == topic
