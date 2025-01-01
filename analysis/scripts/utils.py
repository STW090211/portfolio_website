def load_table(table_name, db_path="../../data/portfolio.db"):
    """
    Loads an entire table from the SQLite db into a Pandas DataFrame
    """
    import pandas as pd
    from sqlalchemy import create_engine

    engine = create_engine(f"sqlite:///{db_path}")
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    engine.dispose()
    return df

