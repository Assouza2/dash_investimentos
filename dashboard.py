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
