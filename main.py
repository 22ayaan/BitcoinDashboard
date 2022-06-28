import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from traitlets import default


from hashrateindex import API
from resolvers import RESOLVERS



def display(resolved):
    for i in resolved:
        dct = i
        outstr = ""
        date = ""
        time = ""
        for key, value in dct.items():
            if key == 'timestamp' or key == "nextHalvingDate" or key == "time":
                value = dct[key]
                date = value[:value.index('T')]
                time = value[value.index('T') + 1 : value.index('+')]
                outstr = date + "     " + time + "     " + "  GMT"
                dct[key] = outstr
                value = outstr
    df = pd.DataFrame(resolved)
    st.subheader("Here's your DATA")
    st.dataframe(df)

def displayChart(resolved):
    for i in resolved:
        dct = i
        outstr = ""
        date = ""
        time = ""
        for key, value in dct.items():
            if key == 'timestamp' or key == "nextHalvingDate" or key == "time":
                value = dct[key]
                date = value[:value.index('T')]
                time = value[value.index('T') + 1 : value.index('+')]
                outstr = date + "     " + time + "     " + "  GMT"
                dct[key] = outstr
                value = outstr
    df = pd.DataFrame(resolved)
    # dfList = list(df.columns)
    # dfList.remove("timestamp")
    # for col_name in dfList:
    #     val = list(df[col_name].to_list())
    # chart_data = pd.DataFrame(val,columns=dfList)

    # st.line_chart(chart_data)
    if selectedFunction == "Network Difficulty" or selectedFunction == "ASIC Price Index":
        df = df.melt('time', var_name = "Columns", value_name = "Value")
        st.write(df)
        chart = alt.Chart(df).mark_line().encode(x = 'time', y = 'Value', color = 'Data')
    else:
        df = df.melt('timestamp', var_name = "Columns", value_name = "Value")
        st.write(df)
        chart = alt.Chart(df).mark_line().encode(x = 'timestamp:T', y = 'Value:Q', color = 'Data:N')
    st.altair_chart(chart, use_container_width=False)



# def switchFunc(choice):
#     match choice:
#         case 0: 
#             resp = API.get_bitcoin_overview()
#             resolved = RESOLVERS.resolve_get_bitcoin_overview(resp)
            
#         case 1:
#             duration  = input("Enter Duration of data required: ")
#             currency = input("Enter currency to display data in: ")
#             resp = API.get_hashprice(duration, currency)
#             resolved = RESOLVERS.resolve_get_hashprice(resp)
          
#         case 2:
#             duration  = input("Enter Duration of data required: ")
#             resp = API.get_network_hashrate(duration)
#             resolved = RESOLVERS.resolve_get_network_hashrate(resp)
        
#         case 3:
#             duration  = input("Enter Duration of data required: ")
#             resp = API.get_network_difficulty(duration)
#             resolved = RESOLVERS.resolve_get_network_difficulty(resp)
           
#         case 4:
#             duration  = input("Enter Duration of data required: ")
#             resp = API.get_ohlc_prices(duration)
#             resolved = RESOLVERS.resolve_get_ohlc_prices(resp)

#         case 5:
#             duration  = input("Enter Duration of data required: ")
#             currency = input("Enter currency to display data in: ")
#             resp = API.get_asic_price_index(duration,currency)
#             resolved = RESOLVERS.resolve_get_asic_price_index(resp)
#     display(resolved)

# print ("Choose Action: ")
# print ("0 - Bitcoin Overview")
# print ("1 - Hash Price")
# print ("2 - Network Hash Rate")
# print ("3 - Network Difficulty")
# print ("4 - OHLC Prices")
# print ("5 - ASIC Price Index")
# chooseFunc = int(input("Enter your choice: "))
# print(chooseFunc)
# switchFunc(chooseFunc)

def matchAction(selectedFunction):
    match selectedFunction:
        case "Bitcoin Overview": 
            resp = API.get_bitcoin_overview()
            resolved = RESOLVERS.resolve_get_bitcoin_overview(resp)
        case "Hash Price": 
            resp = API.get_hashprice(durationParam, currencyParam)
            resolved = RESOLVERS.resolve_get_hashprice(resp)
        case "Network Hash Rate":
            resp = API.get_network_hashrate(durationParam)
            resolved = RESOLVERS.resolve_get_network_hashrate(resp)
        case "Network Difficulty":
            resp = API.get_network_difficulty(durationParam)
            resolved = RESOLVERS.resolve_get_network_difficulty(resp)
        case "OHLC Prices":
            resp = API.get_ohlc_prices(durationParam)
            resolved = RESOLVERS.resolve_get_ohlc_prices(resp)
        case "ASIC Price Index":
            resp = API.get_asic_price_index(durationParam,currencyParam)
            resolved = RESOLVERS.resolve_get_asic_price_index(resp)
    #display(resolved)
    displayChart(resolved)



st.title("Bitcoin Mining Dashboard")
st.header("Filters")

inputKey = st.text_input("Enter API Key")
st.write("You entered: ", inputKey)

API = API(host = 'https://api.hashrateindex.com/graphql', method = 'POST', key = inputKey)
RESOLVERS = RESOLVERS(df = False)

selectedFunction = st.selectbox("Choose a Function",("Bitcoin Overview", "Hash Price", "Network Hash Rate", "Network Difficulty", "OHLC Prices", "ASIC Price Index"))

match selectedFunction:
    case "Bitcoin Overview": 
        durationCheck = False
        currencyCheck = False
    case "Hash Price": 
        durationCheck = True
        currencyCheck = True
    case "Network Hash Rate":
        durationCheck = True
        currencyCheck = False
    case "Network Difficulty":
        durationCheck = True
        currencyCheck = False
    case "OHLC Prices":
        durationCheck = True
        currencyCheck = False
    case "ASIC Price Index":
        durationCheck = True
        currencyCheck = True

if durationCheck:
    if selectedFunction == "Network Difficulty" or selectedFunction == "ASIC Price Index":
        st.write("Note: Data shown below is for the last 3 months")
        durationParam = "_3_MONTHS"
    else:
        duration = st.selectbox("Choose duration of data", ("1 day",  "1 month", "3 months"))
        match duration:
            case "1 day": durationParam = "_1_DAY"
            case "1 month": durationParam = "_1_MONTH"
            case "3 months": durationParam = "_3_MONTHS"

if currencyCheck:
    currencyParam = "BTC"

matchAction(selectedFunction)