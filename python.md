```python
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
```
---
```python
import pandas as pd
from utils import create_tencif_column
from pandas.testing import assert_frame_equal

def test_add_new_tencif_column():
    df = pd.DataFrame({
        'account_branch': ['123', '456'],
        'customer_number': ['7890', '1234']
    })
    expected = pd.DataFrame({
        'TENCIF': ['00001230007890', '00004560001234']
    })

    result = create_tencif_column(df, 'account_branch', 'customer_number')

    assert_frame_equal(result, expected, check_dtype=False)

def test_update_existing_tencif_column():
    df = pd.DataFrame({
        'TENCIF': ['123456789', '9876543210'],
        'account_branch': ['123', '456'],
        'customer_number': ['7890', '1234']
    })
    expected = pd.DataFrame({
        'TENCIF': ['00000123456789', '00009876543210']
    })

    result = create_tencif_column(df, 'account_branch', 'customer_number')

    assert_frame_equal(result, expected, check_dtype=False)
```
---
```python
import pandas as pd
from utils import pivot
from pandas.testing import assert_frame_equal

def test_basic_pivot():
    # テストデータの準備
    df = pd.DataFrame({
        'A': ['foo', 'foo', 'bar', 'bar'],
        'B': ['one', 'two', 'one', 'two'],
        'Values': [1, 2, 3, 4]
    })

    # 関数の実行
    result = pivot(df, 'Values', 'B')

    # 期待される結果
    expected = pd.DataFrame({
        'one': [3, 1],
        'two': [4, 2]
    }, index=['bar', 'foo'])

    assert_frame_equal(result, expected)

def test_double_column_pivot():
    df = pd.DataFrame({
        'A': ['foo', 'foo', 'bar', 'bar'],
        'B': ['one', 'two', 'one', 'two'],
        'C': ['x', 'y', 'x', 'y'],
        'Values': [1, 2, 3, 4]
    })

    # 関数の実行
    result = pivot(df, 'Values', 'B', 'C')

    # 期待される結果
    expected = pd.DataFrame({
        'one_x': [3, None],
        'one_y': [None, None],
        'two_x': [None, None],
        'two_y': [4, 2]
    }, index=['bar', 'foo'])

    pd.testing.assert_frame_equal(result, expected)

def test_replacement_in_columns():
    df = pd.DataFrame({
        'A': ['foo', 'foo'],
        'B': ['one_x', 'two_x'],
        'Values': [1, 2]
    })

    # 関数の実行
    result = pivot(df, 'Values', 'B', replace_str='_x')

    # 期待される結果
    expected = pd.DataFrame({
        'one': [1],
        'two': [2]
    }, index=['foo'])

    pd.testing.assert_frame_equal(result, expected)

def test_missing_column_error():
    df = pd.DataFrame({
        'A': ['foo', 'bar'],
        'Values': [1, 2]
    })

    # 必要なカラムがない場合にエラーが発生するかのテスト
    with pytest.raises(KeyError):
        pivot(df, 'Values', 'B')
```