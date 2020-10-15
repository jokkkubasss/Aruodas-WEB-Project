import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn import ensemble


class Model:
    def __init__(self):
        df3 = pd.read_csv('df3_latest.csv')
        latest = pd.read_csv('latest.csv')
        self.y = df3['price']
        self.X = df3[
               ['room_n', 'area', 'floor_n', 'floor_total', 'age', 'b_Blokinis', 'b_Karkasinis', 'b_Kita', 'b_Medinis',
                'b_Monolitinis',
                'b_Mūrinis', 'b_Rąstinis', 'h_aeroterminis',
                'h_centrinis', 'h_centrinis kolektorinis', 'h_dujinis', 'h_elektra',
                'h_geoterminis', 'h_kietu kuru', 'h_kita', 'lon_scaled', 'lat_scaled']]

        self.gbr2 = ensemble.GradientBoostingRegressor(subsample=0.5, n_estimators=1500, max_depth=5, loss='ls',
                                                       learning_rate=0.025)
        self.ss = StandardScaler()
        self.ss.fit(df3[['longitude', 'latitude']])

        self.enc_b = OneHotEncoder(handle_unknown='ignore')
        self.enc_b.fit(latest[['building_type']])

        self.enc_h = OneHotEncoder(handle_unknown='ignore')
        self.enc_h.fit(latest[['heating_type']])

    def train_model(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2)
        self.gbr2.fit(X_train, y_train)
        return print(self.gbr2.score(X_test, y_test))

    def predict(self, form_data):
        return self.gbr2.predict(self.parse_data_for_model(form_data))

    def scale_coords(self, lon, lat):
        array = np.array([lon, lat])
        return self.ss.transform(array.reshape(1, -1))

    def encode_building(self, building_type):
        return self.enc_b.transform([[building_type]]).toarray()

    def get_age(self, year):
        return 2020 - int(year)

    def encode_heating(self, heating_type):
        types = {'aeroterminis': 0, 'centrinis': 0, 'centrinis kolektorinis': 0, 'dujinis': 0, 'elektra': 0,
                 'geoterminis': 0, 'kietu kuru': 0, 'kita': 0}
        types[heating_type] = 1

        return np.array(list(types.values())).reshape(1, -1).astype(float)

    def parse_data_for_model(self, form_data):
        tmp_array = np.array([form_data['room_n'], form_data['area'], form_data['floor_n'], form_data['floor_total'],
                              self.get_age(form_data['year'])]).reshape(1, -1).astype(float)

        array_data = np.concatenate((tmp_array,
                                     self.encode_building(form_data['building_type']),
                                     self.encode_heating(form_data['heating_type']),
                                     self.scale_coords(form_data['lon'], form_data['lat'])
                                     ), axis=1)
        return array_data
