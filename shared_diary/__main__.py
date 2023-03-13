""" __main__.py """

from shared_diary.client.SharedGasMileageDiary import *




if __name__ == '__main__':
    BOOTSTRAP_SERVER = "localhost:9092"
    KAFKA_TOPIC = "mileage_diary_entries"
    GROUP_ID = str(uuid.uuid1().hex)
    app = QApplication(sys.argv)
    ui = UI(BOOTSTRAP_SERVER, KAFKA_TOPIC, GROUP_ID)
    ui.show()
    sys.exit(app.exec_())