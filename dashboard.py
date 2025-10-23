import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Investimentos", page_icon="💰", layout="wide")

st.title("💰 Dashboard da Carteira de Investimentos")

# upload de arquivo
arquivo = st.file_uploader("📂 Envie seu arquivo CSV da carteira", type=["csv"])

if arquivo is not None:
    df = pd.read_csv(arquivo)

    # limpar valores
    df["Valor"] = (
        df["Valor"]
        .replace({"R\$": "", "\.": "", ",": "."}, regex=True)
        .astype(float)
    )

    total = df["Valor"].sum()
    df["%_da_carteira"] = df["Valor"] / total * 100

    st.metric("Valor total da carteira", f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # layout em colunas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Por Composição")
        fig1 = px.pie(df, names="Composição", values="Valor", hole=0.4,
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("📈 Por Tipo")
        fig2 = px.bar(df.groupby("Tipo", as_index=False)["Valor"].sum(),
                      x="Tipo", y="Valor", color="Tipo",
                      text_auto=".2s", color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart(fig2, use_container_width=True)

    # tabela detalhada
    st.subheader("📋 Detalhamento por Ativo")
    st.dataframe(
        df.sort_values("Valor", ascending=False).style.format({
            "Valor": "R$ {:.2f}",
            "%_da_carteira": "{:.2f}%"
        })
    )
else:
    st.info("Envie um arquivo CSV para visualizar o dashboard.")
