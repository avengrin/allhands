import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_excel("AllHands20250509_V1.xlsx", sheet_name="aktivity_pracovny")
    df = df.rename(columns={"odddelenie": "oddelenie"})
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = load_data()

st.title("📊 Analýza aktivít")

# Výber oddelenia
oddelenie = st.selectbox("Vyber oddelenie", options=[""] + sorted(df["oddelenie"].dropna().unique().tolist()))

if oddelenie:
    df_filtered = df[df["oddelenie"] == oddelenie]

    # 📊 Graf: Podiel kategórií činností v tomto oddelení
    st.subheader(f"📈 Podiel kategórií činností v oddelení: {oddelenie}")
    kat_summary = df_filtered.groupby("kategória_činností").size().reset_index(name="pocet")
    kat_summary = kat_summary[kat_summary["pocet"] > 0]
    if not kat_summary.empty:
        fig_kat = px.pie(
            kat_summary,
            names="kategória_činností",
            values="pocet",
            title=f"Podiel kategórií činností v oddelení: {oddelenie}",
            width=500,
            height=500
        )
        st.plotly_chart(fig_kat)

    # Výber kategórie
    if "kategória_činností" in df_filtered.columns and not df_filtered.empty:
        kategorie = df_filtered["kategória_činností"].dropna().unique().tolist()
        kategoria = st.selectbox("Vyber kategóriu činností", options=[""] + sorted(kategorie))

        if kategoria:
            df_filtered = df_filtered[df_filtered["kategória_činností"] == kategoria]

            # 📊 Graf: Podiel podkategórií činností v tejto kategórii
            st.subheader(f"📈 Podiel podkategórií v kategórii: {kategoria}")
            pod_summary = df_filtered.groupby("podkategória_činností").size().reset_index(name="pocet")
            pod_summary = pod_summary[pod_summary["pocet"] > 0]
            if not pod_summary.empty:
                fig_pod = px.pie(
                    pod_summary,
                    names="podkategória_činností",
                    values="pocet",
                    title=f"Podiel podkategórií v kategórii: {kategoria}",
                    width=500,
                    height=500
                )
                st.plotly_chart(fig_pod)

            # Výber podkategórie
            if "podkategória_činností" in df_filtered.columns and not df_filtered.empty:
                podkategorie = df_filtered["podkategória_činností"].dropna().unique().tolist()
                podkategoria = st.selectbox("Vyber podkategóriu činností", options=[""] + sorted(podkategorie))

                if podkategoria:
                    df_filtered = df_filtered[df_filtered["podkategória_činností"] == podkategoria]

                    # Výber aktivity
                    if "aktivita" in df_filtered.columns and not df_filtered.empty:
                        aktivity = df_filtered["aktivita"].dropna().unique().tolist()
                        aktivita = st.selectbox("Vyber aktivitu", options=[""] + sorted(aktivity))

                        if aktivita:
                            df_filtered = df_filtered[df_filtered["aktivita"] == aktivita]
else:
    df_filtered = pd.DataFrame()

# Výpis finálnych dát
if not df_filtered.empty:
    st.subheader("📋 Výsledné filtrované dáta")
    st.dataframe(df_filtered)
else:
    st.info("Vyber oddelenie, aby sa zobrazili dáta a grafy.")
