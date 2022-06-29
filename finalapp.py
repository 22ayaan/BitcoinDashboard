from datetime import datetime
import streamlit as st
import pandas as pd

from hashrateindex import API
from resolvers import RESOLVERS

definedFunctions = {
    # Contains Bitcoin network data overview stats.
    'Bitcoin Overview': {
        'value' : 'get_bitcoin_overview',
        'resolver' : 'resolve_get_bitcoin_overview',
        'params': {},
        },

    # """
    #     Returns Bitcoin hashprice for a given interval

    #     Parameters
    #     ---------
    #     inputInterval : str
    #         intervals to generate the timeseries, options are: `_1_DAY`, `_7_DAYS`, `_1_MONTH`, `_3_MONTHS`, `_1_YEAR` and `ALL`
    #     currency : str
    #         currency for ASIC price, options are: `USD`, `BTC`
    # """
    'Hashprice' : {
        'value' : 'get_hashprice',
        'resolver' : 'resolve_get_hashprice',
        'params': {
            'inputInterval': {
                '1 Day': '_1_DAY',
                '7 Days': '_7_DAYS',
                '1 Month': '_1_MONTH',
                '3 Months': '_3_MONTHS',
                '1 Year': '_1_YEAR',
                'All': 'ALL',
            },
            'currency': {
                'USD': 'USD',
                'BTC': 'BTC',
            },
        },
    },

    # """
    #     Returns the network hashrate for a given interval

    #     Parameters
    #     ---------
    #     inputInterval : str
    #         intervals to generate the timeseries, options are: `_1_DAY`, `_7_DAYS`, `_1_MONTH`, `_3_MONTHS`, `_1_YEAR` and `ALL`
    # """
    'Network Hashrate' : {
        'value' : 'get_network_hashrate',
        'resolver' : 'resolve_get_network_hashrate',
        'params': {
            'inputInterval': {
                '1 Day': '_1_DAY',
                '7 Days': '_7_DAYS',
                '1 Month': '_1_MONTH',
                '3 Months': '_3_MONTHS',
                '1 Year': '_1_YEAR',
                'All': 'ALL',
            },
        },
    },

    # """
    #     Returns the network difficulty

    #     Parameters
    #     ---------
    #     inputInterval : str
    #         intervals to generate the timeseries, options are: `_3_MONTHS`, `_6_MONTHS`, `_1_YEAR`, `_3_YEAR` and `ALL`
    # """
    'Network Difficulty' : {
        'value' : 'get_network_difficulty',
        'resolver' : 'resolve_get_network_difficulty',
        'params': {
            'inputInterval': {
                '3 Months': '_3_MONTHS',
                '6 Months': '_6_MONTHS',
                '1 Year': '_1_YEAR',
                '3 Years': '_3_YEAR',
                'All': 'ALL',
            },
        },
    },

    # """
    #     Returns the Bitcoin OLHC prices at a specified interval

    #     Parameters
    #     ---------
    #     inputInterval : str
    #         intervals to generate the timeseries, options are: `_1_DAY`, `_7_DAYS`, `_1_MONTH`, `_3_MONTHS`, `_1_YEAR` and `ALL`
    # """
    'OLHC Prices' : {
        'value' : 'get_ohlc_prices',
        'resolver' : 'resolve_get_ohlc_prices',
        'params': {
            'inputInterval': {
                '1 Day': '_1_DAY',
                '7 Days': '_7_DAYS',
                '1 Month': '_1_MONTH',
                '3 Months': '_3_MONTHS',
                '1 Year': '_1_YEAR',
                'All': 'ALL',
            },
        },
    },

    # """
    #     Returns the ASIC price index in USD for a given time interval

    #     Parameters
    #     ---------
    #     inputInterval : str
    #         intervals to generate the timeseries, options are: `_3_MONTHS`, `_6_MONTHS`, `_1_YEAR` and `ALL`
    #     currency : str
    #         currency for ASIC price, options are: `USD`, `BTC`
    # """
    'ASIC Price Index' : {
        'value' : 'get_asic_price_index',
        'resolver' : 'resolve_get_asic_price_index',
        'params': {
            'inputInterval': {
                '3 Months': '_3_MONTHS',
                '6 Months': '_6_MONTHS',
                '1 Year': '_1_YEAR',
                'All': 'ALL',
            },
            'currency': {
                'USD': 'USD',
                'BTC': 'BTC',
            },
        },
    },
}

st.header("Bitcoin Data Dashboard")
st.markdown("**This is a Streamlit app that displays the Hashrate Index of the network.**")
st.markdown("*The Hashrate Index is a measure of the difficulty of the network. It is calculated by taking the average of the difficulty of the last 10 blocks.*")

st.sidebar.header("**Filters**")

# Function Options
selectedFunc = st.sidebar.selectbox('Choose Function', list(definedFunctions.keys()))
selectedFuncParam = definedFunctions[selectedFunc]['params']

# Time Interval Options (if any)
duration = None
if (list(selectedFuncParam.keys()).__contains__('inputInterval')):
    selectedDuration = st.sidebar.select_slider("Choose Time Interval", list(selectedFuncParam['inputInterval'].keys()))
    duration = selectedFuncParam['inputInterval'][selectedDuration]

# Currency Options (if any)
finalCurrency = None
if (list(selectedFuncParam.keys()).__contains__('currency')):
    selectedCurrency = st.sidebar.selectbox("Choose Currency", list(selectedFuncParam['currency'].keys()))
    finalCurrency = selectedFuncParam['currency'][selectedCurrency]

inputKey = st.sidebar.text_input("Enter API key")

if st.sidebar.button('Show Data'):
    API = API(host = 'https://api.hashrateindex.com/graphql', method = 'POST', key = inputKey)
    RESOLVERS = RESOLVERS(df = False)

    finalFunc = getattr(API, definedFunctions[selectedFunc]['value'])

    if duration == None and finalCurrency == None:
        resp = finalFunc()
    elif duration != None and finalCurrency == None:
        resp = finalFunc(duration)
    elif duration != None and finalCurrency != None:
        resp = finalFunc(duration, finalCurrency)
    
    resolved = getattr(RESOLVERS, definedFunctions[selectedFunc]['resolver'])
    resolved = resolved(resp)

    # Data frame
    dictTable = {}
    for key in resolved[0]:
        dictTable.update({key: []})
    
    for idx in range (len(resolved)):
        for key, value in resolved[idx].items():
            dictTable[key].append(value)

    column = list(dictTable.keys())
    df = pd.DataFrame(dictTable, columns=column).set_index(column[0])
    df.index = pd.to_datetime(df.index)

    # Displaying accumulated data
    if selectedFunc != 'Bitcoin Overview':
        with st.expander('Line Chart'):
            st.line_chart(df)
        with st.expander('Area Chart'):
            st.area_chart(df)
        with st.expander('Bar Chart'):
            st.bar_chart(df)
        with st.expander('Table of Statistics'):
            st.dataframe(df.describe())
    
    else:
        st.subheader("**Overview**")
        for col in df.columns:
            if isinstance(df[col][0], datetime):
                df[col][0] = pd.to_datetime(df[col][0])
                st.metric(col, df[col][0])
            st.metric(col, df[col][0])
    
    with st.expander('Raw Data'):
        st.dataframe(df)