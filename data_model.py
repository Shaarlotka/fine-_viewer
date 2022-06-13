import pandas as pd
from car_model import car

class conf:
    def __init__(self):
        self.data = self.set_data()
        self.car_list = self.set_list()

    def set_data(self):
        gsheetkey = "1gqWc2QKkUDG6i88axFP2NC_Xi3rPubsAas9KbY8Jb50"
        table_url = f'https://docs.google.com/spreadsheet/ccc?key={gsheetkey}&output=xlsx'
        sheet_name = 'Лист1'
        return pd.read_excel(table_url, sheet_name)

    def set_list(self):
        car_list = list()
        for index, row in self.data.iterrows():
            num = row.T.T.ТС
            num = [num[index : index + 6] for index in range(0, len(num), 6)]
            certificate = row.T.T.СТС
            certificate = str(certificate).replace(".0","")
            organization = row.T.T.Организация
            new_car = car(num[0], num[1], certificate, organization)
            car_list.append(new_car)
        return car_list