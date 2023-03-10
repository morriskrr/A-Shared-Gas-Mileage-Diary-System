from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
from kafka_lib import *
import threading
import datetime
import uuid
import sys
import os

class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.consumer = MileageDiaryConsumer(BOOTSTRAP_SERVER, KAFKA_TOPIC, GROUP_ID)
        self.setFixedSize(800, 480)
        self.setWindowTitle("A Shared Gas Mileage Diary")


        # Create InputForm tab
        self.input_layout = QVBoxLayout()
        self.input_form = InputForm()
        self.input_layout.addWidget(self.input_form)

        # Create InputViewer tab
        self.output_layout = QVBoxLayout()
        self.input_viewer = InputViewer(self.consumer)
        self.output_layout.addWidget(self.input_viewer)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.output_layout)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.central_widget)

class InputForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.producer = MileageDiaryProducer(BOOTSTRAP_SERVER, KAFKA_TOPIC)

        # Create form elements
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.start_label = QLabel("Starting kilometers:")
        self.start_input = QLineEdit()
        self.end_label = QLabel("Ending kilometers:")
        self.end_input = QLineEdit()
        self.fill_label = QLabel("Filled fuel in euros:")
        self.fill_input = QLineEdit()
        self.fill_input.setText("0")

        self.submit_button = QPushButton("Submit")

        # Add form elements to layout
        self.layout = QFormLayout()
        self.layout.addRow(self.name_label, self.name_input)
        self.layout.addRow(self.start_label, self.start_input)
        self.layout.addRow(self.end_label, self.end_input)
        self.layout.addRow(self.fill_label, self.fill_input)
        self.layout.addWidget(self.submit_button)
        self.setLayout(self.layout)

        # Connect submit button to the send method
        self.submit_button.clicked.connect(self.send_to_kafka)
        self.submit_button.setEnabled(False)

        self.name_input.textChanged.connect(self.check_inputs)
        self.start_input.textChanged.connect(self.check_inputs)
        self.end_input.textChanged.connect(self.check_inputs)
        self.fill_input.textChanged.connect(self.check_inputs)

    def check_inputs(self):
        if self.name_input.text() and self.start_input.text() and self.end_input.text() and self.fill_input.text():
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)

    def send_to_kafka(self):
        # Get form data
        name = self.name_input.text()
        start = self.start_input.text()
        end = self.end_input.text()
        fill = self.fill_input.text()
        submission_time = datetime.datetime.now().timestamp()

        message = {
            "Name": name,
            "Starting_kilometers": start,
            "Ending_kilometers": end,
            "Filled_fuel_in_Euros": fill,
            "Submitted_at": submission_time
        }

        # Send data to Kafka topic
        thr = threading.Thread(target=self.producer.send_entry, args=(message,))
        thr.start()

        # Clear form
        self.name_input.clear()
        self.start_input.clear()
        self.end_input.clear()
        self.fill_input.setText("0")

class InputViewer(QWidget):
    def __init__(self, consumer, parent=None):
        super().__init__(parent)

        # Initialize kafka consumer
        self.consumer = consumer

        # Create text area to display inputs
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.label = QLabel("Diary entries")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_area)
        self.setLayout(self.layout)

        # Create message fetcher thread and connect its signal to the text area
        self.message_fetcher = MileageDiaryFetcher(BOOTSTRAP_SERVER, KAFKA_TOPIC, GROUP_ID, self.consumer)
        self.message_fetcher.message_received.connect(self.add_message)

        # Start message fetcher thread
        self.message_fetcher.start()

    def add_message(self, message: str):
        message_dict = json.loads(message)
        message_string = f'Drive entry by {message_dict["Name"]}, ' \
                        f'Started at {message_dict["Starting_kilometers"]} ' \
                        f'and ended at {message_dict["Ending_kilometers"]}, ' \
                        f'Filled {message_dict["Filled_fuel_in_Euros"]}€ of gas.'

        self.text_area.append(message_string)

class MileageDiaryFetcher(QThread):
    message_received = pyqtSignal(str)


    def __init__(self, bootstrap_servers, topic, group_id, consumer):
        super().__init__()
        self.consumer = consumer

    def run(self):
        for message in self.consumer.consume_messages():
            self.message_received.emit(message)

if __name__ == "__main__":
    BOOTSTRAP_SERVER = "localhost:9092"
    KAFKA_TOPIC = "mileage_diary_entries"
    GROUP_ID = str(uuid.uuid1().hex)
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())