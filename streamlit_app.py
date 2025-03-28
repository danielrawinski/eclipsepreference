import streamlit as st
import pandas as pd
import geopandas as gpd
from plotnine import *

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

# IF GERMANY IS CHOSEN

if countryselector == 'Germany':
    regionselector = st.selectbox('Now, choose a district:', options=['Select']+regions_de)
    
    if regionselector != 'Select':
        st.write('Now, I will ask you to choose how much do you value the following when planning where to view solar eclipse.')
        st.write('There are three criteria. Set a value for each of them for 0 to 1.')
        st.write('IMPORTANT! Sum of those three values should equal to 1.')

        obs_pref = st.slider('Preference for how much sun is obscured', min_value = 0.0, max_value = 1.0, value = 0.0)
        clouds_pref = st.slider('Preference for how little clouds are there on the sky during eclipse', min_value = 0.0, max_value = 1.0, value = 0.0)
        dist_pref = st.slider('Preference for how far would you have to travel to see the eclipse', min_value = 0.0, max_value = 1.0, value = 0.0)
        
        if obs_pref + clouds_pref + dist_pref == 1:
            id_chosen = conditions_de.loc[conditions_de['krs_name'] == regionselector, 'krs_code'].iloc[0]
            distlist = distancematrix_de[str(id_chosen)].tolist()
            distlistnorm = []
            
            for i in range(len(distlist)):
                distlistnorm.append(1 - ((distlist[i] - min(distlist)) / (max(distlist) - min(distlist))))  # 1-norm distance because the smaller distance the better
            
            conditions_for_choice = conditions_de[['krs_code', 'krs_name_sh', 'obscuration', 'Clouds']]

            conditions_for_choice['distance in km'] = distlist
            conditions_for_choice['distance in km'] = conditions_for_choice['distance in km'] / 1000
            conditions_for_choice['distance_norm'] = distlistnorm #adding normalised slice of a distance matrix

            conditions_for_choice['obscuration_norm'] = (conditions_for_choice['obscuration'] - conditions_for_choice['obscuration'].min()) / (conditions_for_choice['obscuration'].max() - conditions_for_choice['obscuration'].min()) # normalizing obscuration
            conditions_for_choice['clouds_norm'] = 1 - ((conditions_for_choice['Clouds'] - conditions_for_choice['Clouds'].min()) / (conditions_for_choice['Clouds'].max() - conditions_for_choice['Clouds'].min())) #normalizing cloud cover, 1-norm because we want the least clouds possible

            conditions_for_choice['preference index'] = obs_pref * conditions_for_choice['obscuration_norm'] + clouds_pref * conditions_for_choice['clouds_norm'] + dist_pref * conditions_for_choice['distance_norm']
            
            display_df = conditions_for_choice[['krs_name_sh', 'obscuration', 'Clouds', 'distance in km', 'preference index']]
            display_df.rename(columns={'krs_name_sh': 'District name', 'obscuration': 'Percentage of Sun covered', 'Clouds': 'Cloud cover', 'distance in km': 'Distance in km', 'preference index': 'Preference index'}, inplace=True)
            
            print(display_df.sort_values(by=['Preference index'], axis=0, ascending=False).head().to_markdown(index=False))
            
            
            deutschland = gpd.read_file('georef-germany-kreis-millesime.shp')

            map_sp_df = deutschland.merge(conditions_for_choice, left_on='krs_code', right_on='krs_code')

            (
                ggplot(map_sp_df)
                + geom_map(aes(fill="preference index"))
                + scale_fill_continuous(
                    name="Preference index",
                    cmap_name="gnuplot",
                    breaks=[0, 0.25, 0.5, 0.75, 1],
                    labels=["0", "0.25", "0.5", "0.75", "1"],
                    limits=[0, 1],
                )
                + coord_fixed(expand=False)
                + theme_void()
                + theme(
                    figure_size=(12, 12),
                    plot_margin=0.1,
                    plot_background=element_rect(fill="white"),
                    panel_spacing=0.025,
                    # legend_frame=element_rect(color="black"),
                    # legend_ticks=element_line(color="black"),
                    strip_text=element_text(size=12),
                )
            )

# IF POLAND IS CHOSEN    
    
if countryselector == 'Poland':
    regionselector = st.selectbox('Now, choose a powiat:', options=['Select']+regions_pl)
    
    if regionselector != 'Select':
        st.write('Now, I will ask you to choose how much do you value the following when planning where to view solar eclipse.')
        st.write('There are three criteria. Set a value for each of them for 0 to 1.')
        st.write('IMPORTANT! Sum of those three values should equal to 1.')

        obs_pref = st.slider('Preference for how much sun is obscured', min_value = 0.0, max_value = 1.0, value = 0.0)
        clouds_pref = st.slider('Preference for how little clouds are there on the sky during eclipse', min_value = 0.0, max_value = 1.0, value = 0.0)
        dist_pref = st.slider('Preference for how far would you have to travel to see the eclipse', min_value = 0.0, max_value = 1.0, value = 0.0)
        
