import streamlit as st
import pandas as pd
import numpy as np
import math
import urllib
from urllib.request import urlopen
import ssl
import warnings
warnings.filterwarnings("ignore")

# Configure app display
st.set_page_config(page_title="Tax Calculator", layout="wide",initial_sidebar_state='collapsed')
# SSL Verification
ssl._create_default_https_context = ssl._create_unverified_context

# Read Data Function
@st.cache()
def read_gsheet(sheetId,sheetName):
	url = f"https://docs.google.com/spreadsheets/d/{sheetId}/gviz/tq?tqx=out:csv&sheet={sheetName}"
	data = pd.read_csv(urllib.request.urlopen(url))
	return data

st.markdown("<h1 style='text-align: center; color: green;'>Bihar Government Land Tax Calculator</h1>", unsafe_allow_html=True)

#options
anchalDF = read_gsheet(st.secrets["sheetId"],"AnchalList")
anchalList = list(anchalDF['anchal'])
anchalList.sort()
anchalList.append("Select")
anchal = st.selectbox("Anchal",anchalList,len(anchalList)-1)
if anchal != "Select":
	selectedDf = read_gsheet(st.secrets["sheetId"],anchal)
	searchType = st.radio("Search By",["Mauza","Thana No."])
	if searchType == "Mauza":
		mauzaList = list(selectedDf["mauza"])
		mauza = st.selectbox("Mauza",mauzaList)
		thanaNo = selectedDf[selectedDf['mauza']==mauza]["thanaNo"].values[0]
		st.write(f"Thana No. = {thanaNo}")
		landType = st.selectbox("Land Type",["Commercial","Residencial","Irrigated","Developing"])
		ratePerDecimal = selectedDf[selectedDf['mauza']==mauza][landType].values[0]
	if searchType == "Thana No.":
		thanaList = list(selectedDf["thanaNo"])
		thanaNo = st.selectbox("Mauza",thanaList)
		mauza = selectedDf[selectedDf['thanaNo']==thanaNo]["mauza"].values[0]
		st.write(f"Mauza = {mauza}")
		landType = st.selectbox("Land Type",["Commercial","Residencial","Irrigated","Developing"])
		ratePerDecimal = selectedDf[selectedDf['thanaNo']==thanaNo][landType].values[0]

	areaIn = st.radio("Area in",["Decimal","Katha"])
	if areaIn == "Katha":
		katha = st.number_input("Total Area in Katha")
		decimal = float(katha) * 3.5
		st.write(f"{round(katha,2)} Katha = {round(decimal,2)} Decimal")
	elif areaIn == "Decimal":
		decimal = st.number_input("Total Area in Decimal")

	taxPercent = st.slider("@Rate",min_value=100, max_value=130, step=5)

	if st.button("Calculate"):
		totalRate = ratePerDecimal * decimal
		r = totalRate % 1000
		if r < 500:
			rf = .5
		else:
			rf = 1
		totalRateRound = totalRate//1000 + rf
		totalTax = int(math.ceil(totalRateRound*taxPercent))
		st.info(f"Total Tax = ₹ {totalTax}")
