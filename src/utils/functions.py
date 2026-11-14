
def generate_metadata(df, ids, targets, orderby = 'PCT_NULOS'):
    import pandas as pd
    """
    Esta função retorna uma tabela com informações descritivas sobre um DataFrame.

    Parâmetros:
    - df: DataFrame que você quer descrever.
    - ids: Lista de colunas que são identificadores.
    - targets: Lista de colunas que são variáveis alvo.

    Retorna:
    Um DataFrame com informações sobre o df original.
    """

    metadata = pd.DataFrame({
        'USO_FEATURE': ['ID' if col in ids else 'Target' if col in targets else 'Explicativa' for col in df.columns],
        'QT_NULOS': df.isnull().sum(),
        'PCT_NULOS': round((df.isnull().sum() / len(df))* 100,2),
        'CARDINALIDADE': df.nunique(),
        'TIPO_FEATURE': df.dtypes
    })

    metadata = metadata.sort_values(by=orderby, ascending=False)
    metadata = metadata.reset_index()
    # Renomeando a coluna 'index' para 'FEATURES'
    metadata = metadata.rename(columns={'index': 'FEATURE'})
    return metadata


def custom_fillna(df):
    import pandas as pd
    import numpy as np

    # Substituindo -1 por nulos
    # Esta função serve para este modelo ou caso específico, porque pode ser que em outras situações o missing não venha marcado com -1

    df.replace(-1, np.nan, inplace=True)
    numerical_cols = df.select_dtypes(include=['float64', 'float32', 'int64', 'int32']).columns
    means = {}

    for col in numerical_cols:
        means[col] = df[col].mean()
        df[col].fillna(means[col], inplace=True)

    categorical_cols = df.select_dtypes(include=['object']).columns
    df[categorical_cols] = df[categorical_cols].fillna('VERIFICAR')

    return df, means


def custom_fillna_prod(df, means):
    import numpy as np
    import pandas as pd

    df.replace(-1, np.nan, inplace=True)
    for col, mean_value in means.items():
      df[col].fillna(mean_value, inplace=True)

    categorical_cols = df.select_dtypes(include=['object']).columns
    df[categorical_cols] = df[categorical_cols].fillna('VERIFICAR')

    return df