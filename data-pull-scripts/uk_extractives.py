import pandas as pd
import requests
import json
from pandas.io.json import json_normalize
import re


YEARS = [2015]

def get_fx_rates():
    path = 'http://api.fixer.io/latest?base=USD'
    #TODO maybe re-make this to pull in a data closer to the report date of each filing?
    fx_rates = requests.get(path).json()
    fx_rates_df = json_normalize(fx_rates['rates']).T.reset_index(level=0)
    # Rename fields
    fx_rates_df.rename(columns={'index': 'ccy',
                                0: 'rate_vs_USD'}, inplace=True)
    usd_row = pd.DataFrame([['USD', 1.000]], columns=['ccy', 'rate_vs_USD'])
    fx_rates_df = fx_rates_df.append(usd_row, ignore_index=True)
    fx_rates_df['fx_date'] = fx_rates['date']

    return fx_rates_df


# This function iterates through one set of filing data to extract one file of all individual project payments for a given year
def get_project_payments(data):
    uk_project_payments = pd.DataFrame([])
    for filing in data:
        payments = json_normalize(filing['projectPayments']['projectPayment'])
        payments['referenceNumber'] = filing['reportDetails']['referenceNumber']
        details = pd.DataFrame([filing['reportDetails']])
        combined = pd.merge(payments, details, how='left', on='referenceNumber')
        uk_project_payments = uk_project_payments.append(combined)

    return uk_project_payments

# This function iterates through multiple years to return a dataframe of project payments
def get_multiyear_project_payments(years):
    uk_project_payments_multiyear = pd.DataFrame([])
    for year in YEARS:
        path = 'https://extractives.companieshouse.gov.uk/api/year/{}/json'.format(year)
        uk_data = requests.get(path).json()
        uk_project_payments = get_project_payments(uk_data)
        uk_project_payments['queryYear'] = year
        uk_project_payments_multiyear = uk_project_payments_multiyear.append(uk_project_payments)
    uk_project_payments_multiyear = uk_project_payments_multiyear.replace({r'\n|\t|  |"': ''}, regex=True)
    return uk_project_payments_multiyear

# This function iterates through one set of filing data to extract one file of all individual government payments for a given year
def get_govt_payments(data):
    uk_govt_payments = pd.DataFrame([])
    for filing in data:
        payments = json_normalize(filing['governmentPayments']['payment'])
        payments['referenceNumber'] = filing['reportDetails']['referenceNumber']
        details = pd.DataFrame([filing['reportDetails']])
        combined = pd.merge(payments, details, how='left', on='referenceNumber')
        uk_govt_payments = uk_govt_payments.append(combined)

    return uk_govt_payments

# This function iterates through multiple years to return a dataframe of project payments
def get_multiyear_govt_payments(years):
    uk_govt_payments_multiyear = pd.DataFrame([])
    for year in YEARS:
        path = 'https://extractives.companieshouse.gov.uk/api/year/{}/json'.format(year)
        uk_data = requests.get(path).json()
        uk_govt_payments = get_govt_payments(uk_data)
        uk_govt_payments['queryYear'] = year
        uk_govt_payments_multiyear = uk_govt_payments_multiyear.append(uk_govt_payments)
    uk_govt_payments_multiyear = uk_govt_payments_multiyear.replace({r'\n|\t|  |"': ''}, regex=True)
    return uk_govt_payments_multiyear

def run():
    fx_rates = get_fx_rates()
    uk_project_payments = get_multiyear_project_payments(YEARS)
    uk_project_payments = pd.merge(uk_project_payments, fx_rates, how='left', left_on='currency', right_on='ccy')
    #uk_project_payments['amount_USD'] = uk_project_payments['rate_vs_USD'].apply(lambda x: uk_project_payments['amount'] / x if x else None)
    uk_project_payments.to_csv('../data/UK_Extractives/uk_project_payments.csv', index=False)

    uk_govt_payments = get_multiyear_govt_payments(YEARS)
    uk_govt_payments = pd.merge(uk_govt_payments, fx_rates, how='left', left_on='currency', right_on='ccy')
    uk_govt_payments.to_csv('../data/UK_Extractives/uk_govt_payments.csv', index=False)

if __name__ == "__main__":
    run()

