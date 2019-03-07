from enum import Enum

import pandas as pd
import pymysql

from Configuration.GlobalConstants import GlobalConstants

_connection_local_host = None


class DBNames(Enum):
    LOCALHOST = 1


class ExternalHelperMethods(object):
    const = GlobalConstants()

    def _run_mysql_query(self, query, functional_db_name_enum):
        try:
            if functional_db_name_enum is DBNames.LOCALHOST:
                global _connection_local_host
                if _connection_local_host is None:
                    _connection_local_host = pymysql.connect(host=self.const.MYSQL_END_POINT,
                                                             port=self.const.MYSQL_PORT,
                                                             user=self.const.MYSQL_USER_NAME,
                                                             passwd=self.const.MYSQL_PASSWORD,
                                                             db=self.const.MYSQL_SCHEMA)
                    mysql_result = pd.read_sql(query, _connection_local_host)
                    return mysql_result
                elif _connection_local_host is not None:
                    mysql_result = pd.read_sql(query, _connection_local_host)
                    return mysql_result

        except Exception as e:
            print(e)
            return pd.DataFrame()

    def get_my_sql_data(self):
        query = "select * from flights"
        flights_data = self._run_mysql_query(query, DBNames.LOCALHOST)
        return flights_data

    def _insert_query(self, data_row, functional_db_name_enum):
        try:
            if functional_db_name_enum is DBNames.LOCALHOST:
                global _connection_local_host
                if _connection_local_host is None:
                    _connection_local_host = pymysql.connect(host=self.const.MYSQL_END_POINT,
                                                             port=self.const.MYSQL_PORT,
                                                             user=self.const.MYSQL_USER_NAME,
                                                             passwd=self.const.MYSQL_PASSWORD,
                                                             db=self.const.MYSQL_SCHEMA)
                    data_row.to_sql('flights', con=_connection_local_host, if_exists='append')
                elif _connection_local_host is not None:
                    data_row.to_sql('flights', con=_connection_local_host, if_exists='append')
        except Exception as e:
            print(e)
            return pd.DataFrame()

    def insert_data_into_db(self, data_row):
        try:
            global _connection_local_host
            if _connection_local_host is None:
                _connection_local_host = pymysql.connect(host=self.const.MYSQL_END_POINT,
                                                         port=self.const.MYSQL_PORT,
                                                         user=self.const.MYSQL_USER_NAME,
                                                         passwd=self.const.MYSQL_PASSWORD,
                                                         db=self.const.MYSQL_SCHEMA)
        except Exception as e:
            print(e)
        data_row = data_row.squeeze()
        MSN = data_row['MSN']
        HarnessLength = data_row['HarnessLength'] if 'HarnessLength' in data_row else None
        FlightProgram = data_row['FlightProgram']
        GrossWeight = data_row['GrossWeight'] if 'GrossWeight' in data_row else None
        AtmPressure = data_row['AtmPressure'] if 'AtmPressure' in data_row else None
        RoomTemp = data_row['RoomTemp'] if 'RoomTemp' in data_row else None
        Airport = data_row['Airport'] if 'Airport' in data_row else None
        FuelCapacityLeft = data_row['FuelCapacityLeft'] if 'FuelCapacityLeft' in data_row else None
        FuelCapacityRight = data_row['FuelCapacityRight'] if 'FuelCapacityRight' in data_row else None
        FuelQuantityRight = data_row['FuelQuantityRight'] if 'FuelQuantityRight' in data_row else None
        FuelQuantityLeft = data_row['FuelQuantityLeft'] if 'FuelQuantityLeft' in data_row else None
        MaxAltitude = data_row['MaxAltitude'] if 'MaxAltitude' in data_row else None
        FlightNo = data_row['FlightNo'] if 'FlightNo' in data_row else None
        if int(FuelCapacityLeft) < int(FuelQuantityLeft):
            print('left')
            return False
        if int(FuelCapacityRight) < int(FuelQuantityRight):
            print('right')
            return False
        query = "INSERT INTO flights VALUES (" + str(MSN) + ',' + str(HarnessLength) + ',' + '"' +str(
            FlightProgram)+ '"' + ',' + str(GrossWeight) + ',' + str(AtmPressure) + ',' + str(RoomTemp) + ',' + '"'+ str(
            Airport) + '"'+ ',' + str(FuelCapacityLeft) + ',' + str(FuelCapacityRight)  + ',' + str(
            FuelQuantityRight) + ',' + str(FuelQuantityLeft) + ',' + str(
            MaxAltitude) + ',' + '"'+ str(FlightNo) + '"'+ ')'
        print(query)
        try:
            with _connection_local_host.cursor() as cursor:
                cursor.execute(query)
                _connection_local_host.commit()
                return True
        except Exception as e:
            print(e)
            return False
