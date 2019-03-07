from ExternalHelper.ExternalHelper import ExternalHelperMethods

if __name__ == '__main__':
    external_helper = ExternalHelperMethods()
    data = external_helper.get_my_sql_data()
    print(data)