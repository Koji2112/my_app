import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import base64
import streamlit.components.v1 as components

# CSS pour personnalisation simple

CSS = """
<style>

header {
    text-align: center;
    margin-bottom: 30px;
    color: #4CAF50;
}
h1 {
    font-size: 3rem;
    font-weight: bold;
    letter-spacing: 1px;
}
.stButton > button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 12px 25px;
    font-size: 1.2rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s;
}
.stButton > button:hover {
    background-color: #45a049;
}


.stSelectbox label {
    font-size: 1.2rem;
    font-weight: bold;
    color: #4CAF50;
}


.stSelectbox div[data-baseweb="select"] {
    background-color: #f9f9f9;
    border: 2px solid #4CAF50;
    border-radius: 8px;
    padding: 5px;
    font-size: 1rem;
    color: #333;
}







</style>
"""

# Insérer le CSS dans l'application
st.markdown(CSS, unsafe_allow_html=True)

# Titre de l'application
st.markdown("<header><h1>Application de WebScraping</h1></header>", unsafe_allow_html=True)


# Choisir la méthode de scraping
scraping_method = st.sidebar.selectbox(
    "Choisissez la méthode de scraping",
    ("BeautifulSoup", "WebScraper")
)

# Choisir le nombre de pages a scraper
num_pages = st.sidebar.selectbox(
    "Choisissez le nombre de pages",
    options=list(range(1, 120)), 
    index=2 
)
form_choices = ["Sélectionnez un formulaire", "Kobotoolbox", "Google Forms"]

# Affichage du sélecteur
form_selection = st.sidebar.selectbox("Choisissez un formulaire", form_choices)

# Afficher le formulaire sélectionné
if form_selection == "Kobotoolbox":
    st.info("Formulaire Kobotoolbox sélectionné.")
    components.html("""
    <iframe src="https://ee.kobotoolbox.org/i/ya9GbL2S" width="1000%" height="800"></iframe>
    """,height=800,width=600)
  
elif form_selection == "Google Forms":
    st.info("Formulaire Google Forms sélectionné.")
    google_forms_url = "https://forms.gle/X9vAp5GvaiunnUCi8"  # Remplacez par votre lien
    st.components.v1.html(
        f"""
        <iframe src="{google_forms_url}" width="100%" height="600" style="border:none;"></iframe>
        """,
        height=600,
    )


st.markdown("""
Cet application permets le webscraping de donnée a partir de site sur plusieurs pages mais
il est egalement possible des données(non nettoyées) directement. Vous pourrez enfin telecharger
données.
* **Python libraries:** base64, pandas, streamlit, requests, bs4
* **Data source:** [Les Villas](https://sn.coinafrique.com/categorie/villas?) -- [Les terrains](https://sn.coinafrique.com/categorie/terrains?).
""")


# BeautifulSoup pour terrains 
def scrape_terrains_beautifulsoup(pages):

    data_terrains = {
        "superficie": [],
        "prix": [],
        "adresse": [],
        "image lien": []
    }
    for i in range(1, pages + 1):
        url = f'https://sn.coinafrique.com/categorie/terrains?page={i}'
        try:
            res = get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            containers = soup.find_all('div', class_="col s6 m4 l3")
            for container in containers:
                img_link = container.find('img', class_="ad__card-img")['src']
                try:
                    inner_link = container.find('a', class_="card-image ad__card-image waves-block waves-light")["href"]
                    if inner_link:
                        url_enfant = 'https://sn.coinafrique.com' + inner_link
                except:
                    continue

                if url_enfant:
                    try:
                        res1 = get(url_enfant)
                        soup1 = BeautifulSoup(res1.text, 'html.parser')
                        container_1 = soup1.find('div', class_="card round slide proffer z-depth-0 remove-background-white")
                        if container_1:
                            superficie = container_1.find('span', class_='qt').text.replace('m2', '').replace(' ', '')
                            prix = int(container_1.find('p', class_='price').text.replace('CFA', '').replace(' ', '').strip())
                            adresse = container_1.find_all('span', class_='valign-wrapper')[1].text
                            data_terrains["superficie"].append(superficie)
                            data_terrains["prix"].append(prix)
                            data_terrains["adresse"].append(adresse)
                            data_terrains["image lien"].append(img_link)
                    except:
                        continue
        except:
            continue
    return pd.DataFrame(data_terrains)

# WebScraperpour terrains 
def scrape_terrains_webscraper(pages):
    # Charger les données pré-existantes dans terrains_df
    try:
        terrains_df = pd.read_csv("terrain.csv")  
        return terrains_df
    except FileNotFoundError:
        st.error("Le fichier 'terrain.csv' n'a pas été trouvé. Veuillez vous assurer qu'il est téléchargé.")
        return pd.DataFrame()  # Return an empty DataFrame in case the file is missing

# BeautifulSoup pour villas 
def scrape_villas_beautifulsoup(pages):
    data_villas = {
        "type annonce": [],
        "nombre pieces": [],
        "prix": [],
        "adresse": [],
        "image lien": []
    }
    for i in range(1, pages + 1):
        url = f'https://sn.coinafrique.com/categorie/villas?page={i}'
        try:
            res = get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            containers = soup.find_all('div', class_="col s6 m4 l3")
            for container in containers:
                img_link = container.find('img', class_="ad__card-img")['src']
                try:
                    inner_link = container.find('a', class_="card-image ad__card-image waves-block waves-light")["href"]
                    if inner_link:
                        url_enfant = 'https://sn.coinafrique.com' + inner_link
                except:
                    continue

                if url_enfant:
                    try:
                        res1 = get(url_enfant)
                        soup1 = BeautifulSoup(res1.text, 'html.parser')
                        container_1 = soup1.find('div', class_="card round slide proffer z-depth-0 remove-background-white")
                        if container_1:
                            type_annonce = container_1.find('h1', class_='title title-ad hide-on-large-and-down').text.split()[0]
                            nombre_pieces = int(container_1.find('span', class_='qt').text)
                            prix = int(container_1.find('p', class_='price').text.replace('CFA', '').replace(' ', '').strip())
                            adresse = container_1.find_all('span', class_='valign-wrapper')[1].text
                            data_villas["type annonce"].append(type_annonce)
                            data_villas["nombre pieces"].append(nombre_pieces)
                            data_villas["prix"].append(prix)
                            data_villas["adresse"].append(adresse)
                            data_villas["image lien"].append(img_link)
                    except:
                        continue
        except:
            continue
    return pd.DataFrame(data_villas)

# Fonction de scraping pour villas (WebScraper)
def scrape_villas_webscraper(pages):
    # Charger les données pré-existantes dans villas_df
    try:
        villas_df = pd.read_csv("villa.csv")  
        return villas_df
    except FileNotFoundError:
        st.error("Le fichier 'villa.csv' n'a pas été trouvé. Veuillez vous assurer qu'il est téléchargé.")
        return pd.DataFrame() 

# Affichage et scraping des données
if scraping_method == "BeautifulSoup":
    if st.sidebar.button("Scraper Terrains"):
        st.info("Scraping des terrains en cours avec BeautifulSoup...")
        df_terrains = scrape_terrains_beautifulsoup(pages=num_pages)
        st.success("Scraping des terrains terminé !")
        st.write(df_terrains)
        st.session_state['data_terrains'] = df_terrains  

    if st.sidebar.button("Scraper Villas"):
        st.info("Scraping des villas en cours avec BeautifulSoup...")
        df_villas = scrape_villas_beautifulsoup(pages=num_pages)
        st.success("Scraping des villas terminé !")
        st.write(df_villas)
        st.session_state['data_villas'] = df_villas  

elif scraping_method == "WebScraper":
    if st.sidebar.button("Charger les données de terrains via WebScraper"):
        st.info("Chargement des terrains avec WebScraper...")
        df_terrains = scrape_terrains_webscraper(pages=num_pages)
        st.success("Chargement des terrains terminé !")
        st.write(df_terrains)
        st.session_state['data_terrains'] = df_terrains  

    if st.sidebar.button("Charger les données de villas via WebScraper"):
        st.info("Chargement des villas avec WebScraper...")
        df_villas = scrape_villas_webscraper(pages=num_pages)
        st.success("Chargement des villas terminé !")
        st.write(df_villas)
        st.session_state['data_villas'] = df_villas  

# Téléchargement des données
if st.sidebar.button("Télécharger les données (CSV)"):
    if 'data_terrains' in st.session_state:
        df_terrains = st.session_state['data_terrains']
        csv_terrains = df_terrains.to_csv(index=False).encode('utf-8')
        st.download_button(label="Télécharger les Terrains", data=csv_terrains, file_name="annonces_terrains.csv", mime='text/csv')
    
    if 'data_villas' in st.session_state:
        df_villas = st.session_state['data_villas']
        csv_villas = df_villas.to_csv(index=False).encode('utf-8')
        st.download_button(label="Télécharger les Villas", data=csv_villas, file_name="annonces_villas.csv", mime='text/csv')
