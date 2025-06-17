import streamlit as st
import pandas as pd
import plotly.express as px

# Načítanie dát zo záložky a úprava názvov stĺpcov
@st.cache_data
def load_data():
    df = pd.read_excel("AllHands20250509_V1.xlsx", sheet_name="aktivity_pracovny")
    df = df.rename(columns={"odddelenie": "oddelenie"})  # oprava preklepu
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = load_data()

st.title("📊 Analýza aktivít podľa oddelení")

# Zobrazenie stĺpcov pre kontrolu (voliteľné)
# st.write("Dostupné stĺpce:", df.columns.tolist())

# Možnosť zobraziť celé dáta
if st.checkbox("Zobraziť zdrojové dáta"):
    st.dataframe(df)

# Filtrovanie údajov
oddelenia = st.multiselect("Vyber oddelenie", options=df["oddelenie"].unique(), default=df["oddelenie"].unique())
df_filtered = df[df["oddelenie"].isin(oddelenia)]

if len(oddelenia) == 1:
    oddelenie_name = oddelenia[0]
    df_odd = df_filtered[df_filtered["oddelenie"] == oddelenie_name]
    
    # Počet aktivít podľa kategórie
    kat_summary = df_odd.groupby("kategória_činností").size().reset_index(name="pocet")
    kat_summary["percento"] = round(100 * kat_summary["pocet"] / kat_summary["pocet"].sum(), 2)

    # Graf: koláč podľa kategórií
    fig2 = px.pie(
        kat_summary,
        names="kategória_činností",
        values="pocet",
        title=f"Podiel kategórií činností v oddelení: {oddelenie_name}"
    )
    st.plotly_chart(fig2)

kategorie = st.multiselect("Vyber kategóriu činností", options=df_filtered["kategória_činností"].unique(), default=df_filtered["kategória_činností"].unique())
df_filtered = df_filtered[df_filtered["kategória_činností"].isin(kategorie)]

# Ak je vybraná práve jedna kategória činností, zobraz podiel aktivít podľa podkategórií
if len(kategorie) == 1:
    kategoria_name = kategorie[0]
    df_kat = df_filtered[df_filtered["kategória_činností"] == kategoria_name]

    pod_summary = df_kat.groupby("podkategória_činností").size().reset_index(name="pocet")
    pod_summary["percento"] = round(100 * pod_summary["pocet"] / pod_summary["pocet"].sum(), 2)

    # Graf: koláč podľa podkategórií
    fig3 = px.pie(
        pod_summary,
        names="podkategória_činností",
        values="pocet",
        title=f"Podiel podkategórií v kategórii: {kategoria_name}"
    )
    st.plotly_chart(fig3)

podkategorie = st.multiselect("Vyber podkategóriu činností", options=df_filtered["podkategória_činností"].unique(), default=df_filtered["podkategória_činností"].unique())
df_filtered = df_filtered[df_filtered["podkategória_činností"].isin(podkategorie)]

aktivity = st.multiselect("Vyber aktivitu", options=df_filtered["aktivita"].unique(), default=df_filtered["aktivita"].unique())
df_filtered = df_filtered[df_filtered["aktivita"].isin(aktivity)]

# Výpočet počtu a percentuálneho podielu aktivít
summary = df_filtered.groupby(["oddelenie", "kategória_činností", "podkategória_činností", "aktivita"]).size().reset_index(name="pocet")
summary["percento"] = round(100 * summary["pocet"] / summary["pocet"].sum(), 2)

# Výpis tabuľky
st.subheader("📋 Súhrn aktivít (počty a podiely)")
st.dataframe(summary)

# Graf: podiel podľa oddelení
if not summary.empty:
    fig = px.pie(summary, names="oddelenie", values="pocet", title="Podiel aktivít podľa oddelení")
    st.plotly_chart(fig)
else:
    st.warning("⚠️ Žiadne dáta pre zvolenú kombináciu filtrov.")

# Bar chart: počet aktivít podľa kategórií a oddelení
if not df_filtered.empty:
    bar_summary = df_filtered.groupby(["kategória_činností", "oddelenie"]).size().reset_index(name="pocet")

    fig4 = px.bar(
        bar_summary,
        x="kategória_činností",
        y="pocet",
        color="oddelenie",
        barmode="group",
        title="Počet aktivít podľa kategórií a oddelení"
    )
    st.plotly_chart(fig4)

# Debug:
