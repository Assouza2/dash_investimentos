import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Investimentos", page_icon="💰", layout="wide")

st.title("💰 Dashboard da Carteira de Investimentos")

# upload de arquivo
arquivo = st.file_uploader("📂 Envie seu arquivo CSV da carteira", type=["csv"])

if arquivo is not None:
    df = pd.read_csv(arquivo)

    # Normalizar nomes de colunas (remover espaços e deixar minúsculas)
    df.columns = df.columns.str.strip().str.lower()

    # Verificar se coluna 'valor' existe
    if "valor" not in df.columns:
        st.error("❌ A coluna 'Valor' não foi encontrada no arquivo CSV. Certifique-se de que existe uma coluna chamada 'Valor'.")
        st.stop()

    # limpar valores
    df["valor"] = (
        df["valor"]
        .replace({"R\$": "", "\.": "", ",": "."}, regex=True)
        .astype(float)
    )

    total = df["valor"].sum()
    df["%_da_carteira"] = df["valor"] / total * 100

    st.metric("Valor total da carteira", f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Por Composição")
        fig1 = px.pie(df, names="composição", values="valor", hole=0.4,
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("📈 Por Tipo")
        fig2 = px.bar(df.groupby("tipo", as_index=False)["valor"].sum(),
                      x="tipo", y="valor", color="tipo",
                      text_auto=".2s", color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📋 Detalhamento por Ativo")
    st.dataframe(
        df.sort_values("valor", ascending=False).style.format({
            "valor": "R$ {:.2f}",
            "%_da_carteira": "{:.2f}%"
        })
    )
else:
    st.info("Envie um arquivo CSV para visualizar o dashboard.")
