import streamlit as st
import pandas as pd
import plotly.express as px
import unidecode
import io

st.set_page_config(page_title="Dashboard Inteligente de Investimentos", page_icon="💰", layout="wide")

st.title("💰 Dashboard Inteligente da Carteira de Investimentos")

# Upload do arquivo
arquivo = st.file_uploader("📂 Envie seu arquivo CSV da carteira", type=["csv"])

if arquivo is not None:
    # Detectar automaticamente o separador
    conteudo = arquivo.getvalue().decode("utf-8")
    sep = ";" if conteudo.count(";") > conteudo.count(",") else ","

    # Ler o CSV com separador detectado
    df = pd.read_csv(io.StringIO(conteudo), sep=sep)

    # Normalizar nomes de colunas
    df.columns = [unidecode.unidecode(c).strip() for c in df.columns]

    st.success(f"✅ Arquivo carregado com sucesso! Separador detectado: '{sep}'")
    st.write("**Colunas detectadas:**", list(df.columns))

    # Permitir que o usuário escolha quais colunas usar
    col_valor = st.selectbox("💵 Selecione a coluna de valores:", df.columns, index=min(2, len(df.columns)-1))
    col_tipo = st.selectbox("🏷️ Selecione a coluna de categorias (tipo):", df.columns, index=min(1, len(df.columns)-1))
    col_nome = st.selectbox("📊 Selecione a coluna de composição/ativo:", df.columns, index=0)

    # Limpar e converter a coluna de valor
    df[col_valor] = (
        df[col_valor]
        .astype(str)
        .replace({"R\$": "", "\.": "", ",": "."}, regex=True)
        .astype(float)
    )

    # Calcular percentuais
    total = df[col_valor].sum()
    df["%_da_carteira"] = df[col_valor] / total * 100

    # Mostrar valor total
    st.metric("Valor total da carteira", f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # Layout dos gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Distribuição por Ativo")
        fig1 = px.pie(
            df,
            names=col_nome,
            values=col_valor,
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("📈 Distribuição por Categoria")
        fig2 = px.bar(
            df.groupby(col_tipo, as_index=False)[col_valor].sum(),
            x=col_tipo,
            y=col_valor,
            color=col_tipo,
            text_auto=".2s",
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Tabela detalhada
    st.subheader("📋 Detalhamento por Ativo")
    st.dataframe(
        df.sort_values(col_valor, ascending=False).style.format({
            col_valor: "R$ {:.2f}",
            "%_da_carteira": "{:.2f}%"
        })
    )

else:
    st.info("📥 Envie um arquivo CSV para visualizar o dashboard.")
