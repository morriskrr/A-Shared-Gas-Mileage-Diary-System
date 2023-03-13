import pytest
import uuid
import sys
from PyQt5.QtWidgets import QApplication




class TestPackageImports(object):

	def test_shared_diary(self):
		from shared_diary.client.SharedGasMileageDiary import UI

		BOOTSTRAP_SERVER = "localhost:9092"
		KAFKA_TOPIC = "mileage_diary_entries"
		GROUP_ID = str(uuid.uuid1().hex)
		print(GROUP_ID)

		app = QApplication(sys.argv)
		ui = UI(BOOTSTRAP_SERVER, KAFKA_TOPIC, GROUP_ID)
		ui.show()

		assert True == True


