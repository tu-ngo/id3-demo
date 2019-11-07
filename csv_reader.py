import csv


class CsvRows:
    def __init__(self, path_to_csv_file):
        input_file = csv.DictReader(open(path_to_csv_file))
        rows = []
        for row in input_file:
            rows.append(row)

        self.rows = rows

    def get_records(self):
        return self.rows

    def get_length(self):
        return self.rows.__len__()

    def get_row(self, position):
        return self.rows[position]