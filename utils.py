import pandas as pd

def create_tencif_column(df, account_branch_col, customer_number_col):
    if "TENCIF" not in df.columns:
        df[account_branch_col] = df[account_branch_col].astype(str).str.zfill(7)
        df[customer_number_col] = df[customer_number_col].astype(str).str.zfill(7)
        
        df["TENCIF"] = df[account_branch_col] + df[customer_number_col]
    else:
        df["TENCIF"] = df["TENCIF"].astype(str).str.zfill(14)
    
    df.drop(columns=[account_branch_col, customer_number_col], inplace = True, errors = "ignore")

    return df

def pivot(df, value_column, col1_for_pivot, col2_for_pivot=None, replace_str=""):
    index_columns = df.columns.tolist()
    
    index_columns.remove(value_column)
    index_columns.remove(col1_for_pivot)
    
    if col2_for_pivot:
        index_columns.remove(col1_for_pivot)
        df[col1_for_pivot] = df[col1_for_pivot] + "_" +df[col2_for_pivot]
        
    pivot_df = pd.pivot_table(df, index= index_columns, values = value_column, columns=col1_for_pivot).reset_index()
        
    pivot_df.columns.name = None
    
    pivot_df.columns = [str(col).replace(replace_str, "") for col in pivot_df.columns]
    
    pivot_df.drop(columns = [col2_for_pivot], inplace = True)
    
    return pivot_df