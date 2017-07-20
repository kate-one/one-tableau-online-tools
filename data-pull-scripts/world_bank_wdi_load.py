import pandas as pd


WDI_PATH = '../../WorldBank-Dev_Indicators-1Jul17/WDI_csv/WDIData.csv'


def tidy_wdi_data(file = WDI_PATH):
    full_wb_data = pd.read_csv(file, encoding='utf-8')

    #Drop the extra blank column at the end
    full_wb_data.drop('Unnamed: 61', axis=1, inplace=True)

    full_wb_data_long = pd.melt(full_wb_data,
                                  id_vars=['Country Name','Country Code','Indicator Name','Indicator Code'],
                                  value_name = 'Value',
                                  var_name = 'Year')

    # Convert the Year field to be numeric (instead of a string)
    full_wb_data_long['Year'] = full_wb_data_long['Year'].astype('int')

    # Drop null values
    full_wb_data_long = full_wb_data_long.dropna()

    # Keep only last 5 years of data
    full_wb_data_long = full_wb_data_long[full_wb_data_long['Year'] >= 2012]

    full_wb_data_long.to_csv('../../WorldBank-Dev_Indicators-1Jul17/WDIData20170720.csv', index=False, encoding='utf-8')

    return full_wb_data_long

def run():
    tidy_wdi_data()


if __name__ == "__main__":
    run()