import streamlit as st
import pandas as pd

# =============================================================================
# Importing files and defining variables
# =============================================================================

conditions_pl = pd.read_csv(r"poland_2025_eclipse_conditions_with_clouds.csv", sep = ";")
conditions_de = pd.read_csv(r"germany_2025_eclipse_conditions_with_clouds.csv", sep = ";")

distancematrix_pl = pd.read_csv(r"macierz_odleglosci_pl.csv", sep = ";").set_index('ID')
distancematrix_de = pd.read_csv(r"macierz_odleglosci_de.csv", sep = ";").set_index('ID')

regions_pl = sorted(conditions_pl['JPT_NAZWA_'].values.tolist())
regions_de = sorted(conditions_de['krs_name'].values.tolist())

# =============================================================================
# Page body
# =============================================================================

st.header('Solar eclipse viewing spot preference calculator - 2025.03 partial eclipse edition')

countryselector = st.selectbox('First, choose a country:', ['Select', 'Germany','Poland'])

if countryselector == 'Germany':
    regionselector = st.selectbox('Now, choose a district:', options=['Select']+regions_de)
    
    if regionselector != 'Select':
        st.write('Now, I will ask you to choose how much do you value the following when planning where to view solar eclipse.')
        st.write('There are three criteria. Set a value for each of them for 0 to 1.')
        st.write('IMPORTANT! Sum of those three values should equal to 1.')

        obs_pref = st.slider('Preference for how much sun is obscured', value=0.34)
        clouds_pref = st.slider('Preference for how little clouds are there on the sky during eclipse', value=0.33)
        dist_pref = st.slider('Preference for how far would you have to travel to see the eclipse', value=0.33)      
    
if countryselector == 'Poland':
    regionselector = st.selectbox('Now, choose a powiat:', options=['Select']+regions_pl)
    
    if regionselector != 'Select':
        st.write('Now, I will ask you to choose how much do you value the following when planning where to view solar eclipse.')
        st.write('There are three criteria. Set a value for each of them for 0 to 1.')
        st.write('IMPORTANT! Sum of those three values should equal to 1.')

        obs_pref = st.slider('Preference for how much sun is obscured', value=0.34)
        clouds_pref = st.slider('Preference for how little clouds are there on the sky during eclipse', value=0.33)
        dist_pref = st.slider('Preference for how far would you have to travel to see the eclipse', value=0.33)
