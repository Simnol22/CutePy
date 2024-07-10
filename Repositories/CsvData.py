import csv
import os
from collections import defaultdict

class CsvData:
    def __init__(self, path):
        self.path = path
        self.data = defaultdict(dict)
        self.header_written = False
        self.header = None  # Initialize header attribute

        # Load existing data if file exists
        if os.path.exists(self.path):
            self._load_existing_data()

    def _load_existing_data(self):
        with open(self.path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            self.header = reader.fieldnames  # Set header attribute
            for row in reader:
                timestamp = row['Timestamp']
                for key, value in row.items():
                    if key != 'Timestamp':
                        self.data[timestamp][key] = value

    def addMeasurement(self, measurement):
        source = measurement.source
        timestamp = measurement.timestamp
        value = measurement.value

        if not self.header_written:
            self._write_header([source])

        # Update the data dictionary
        if timestamp not in self.data:
            self.data[timestamp] = {}
        self.data[timestamp][source] = value

        # Update the CSV file
        self._update_rows()

    def _write_header(self, new_sources):
        self.header = ['Timestamp'] + new_sources  # Update header attribute
        with open(self.path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.header)
            self.header_written = True

    def _update_rows(self):
        with open(self.path, 'a', newline='') as file:
            writer = csv.writer(file)
            for timestamp, values in self.data.items():
                row = [timestamp] + [values.get(source, '') for source in self.header[1:]]
                writer.writerow(row)

    def read(self):
        with open(self.path, 'r') as file:
            return file.read()

    def write(self, data):
        with open(self.path, 'w') as file:
            file.write(data)

    def append(self, data):
        with open(self.path, 'a') as file:
            file.write(data)
