import csv
import os
from collections import defaultdict, deque
import time

class CsvData:
    def __init__(self, parent, path, frequence=20):
        self.parent = parent
        self.freq = frequence
        self.path = path
        self.headers = []
        self.data_rows = []
        self.allData = deque(maxlen=5000)
        self.opened = False
        self.column_set = set()
        self.data_dict = defaultdict(lambda: [''] * len(self.headers))
        self.current_row_by_source = {}  # Track the current row for each source
        self.verifyPath()
        
    def verifyPath(self):
        if not os.path.exists(self.path):
            return True
        else:
            name = self.path.split('.')[0]
            cnt=0
            while os.path.exists(self.path):
                cnt+=1
                self.path = name + str(cnt) + ".csv"
            return True
    
    def addMeasurement(self, measurement):
        source = measurement.source
        timestamp = measurement.timestamp
        value = measurement.value
        self.allData.append([source, timestamp, value])

    def openFile(self):
        """Initialize the file with the basic header."""
        with open(self.path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
        self.opened = True

    def saveData(self):
        """Save all accumulated data to the CSV file."""
        for data in self.allData:
            self.add_data(data[0], data[1], data[2])
        self.write_data_to_csv()
        self.allData.clear()

    def update_header(self, column_title):
        """Update the CSV header if a new column title is added."""
        timestamp_col = f"{column_title} Timestamp"
        
        if column_title not in self.column_set:
            # Add timestamp and data columns for the new source
            if timestamp_col not in self.headers:
                self.headers.append(timestamp_col)
            if column_title not in self.headers:
                self.headers.append(column_title)
            
            self.column_set.add(column_title)
            self.column_set.add(timestamp_col)

            # Ensure existing rows in the data_dict match the updated headers
            for key in self.data_dict:
                self.data_dict[key].extend([''] * (len(self.headers) - len(self.data_dict[key])))

    def add_data(self, column_title, timestamp, value):
        """Add data to the CSV file."""
        if column_title not in self.column_set:
            self.update_header(column_title)

        # Determine the correct row index for this source
        row_index = self.current_row_by_source.get(column_title, len(self.data_rows))

        # Ensure the row exists in data_rows
        while row_index >= len(self.data_rows):
            self.data_rows.append([''] * len(self.headers))
        
        # Update the row with the new data
        row = self.data_rows[row_index]
        timestamp_col = f"{column_title} Timestamp"
        row[self.headers.index(timestamp_col)] = timestamp
        row[self.headers.index(column_title)] = value

        # Update the current row index for the source
        self.current_row_by_source[column_title] = row_index + 1

    def write_data_to_csv(self):
        """Write all accumulated data to the CSV file."""
        with open(self.path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.headers)
            writer.writerows(self.data_rows)

    def run(self):
        try:
            while True:
                if self.parent.configSettings.saveData:
                    if not self.opened:
                        self.openFile()
                    self.saveData()
                time.sleep(1 / self.freq)
        except KeyboardInterrupt:
            print('Interrupted!')
