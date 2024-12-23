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

# def test_double_column_pivot():
#     df = pd.DataFrame({
#         'A': ['foo', 'foo', 'bar', 'bar'],
#         'B': ['one', 'two', 'one', 'two'],
#         'C': ['x', 'y', 'x', 'y'],
#         'Values': [1, 2, 3, 4]
#     })

#     # 関数の実行
#     result = pivot(df, 'Values', 'B', 'C')

#     # 期待される結果
#     expected = pd.DataFrame({
#         'one_x': [3, None],
#         'one_y': [None, None],
#         'two_x': [None, None],
#         'two_y': [4, 2]
#     }, index=['bar', 'foo'])

#     pd.testing.assert_frame_equal(result, expected)

# def test_replacement_in_columns():
#     df = pd.DataFrame({
#         'A': ['foo', 'foo'],
#         'B': ['one_x', 'two_x'],
#         'Values': [1, 2]
#     })

#     # 関数の実行
#     result = pivot(df, 'Values', 'B', replace_str='_x')

#     # 期待される結果
#     expected = pd.DataFrame({
#         'one': [1],
#         'two': [2]
#     }, index=['foo'])

#     pd.testing.assert_frame_equal(result, expected)

# def test_missing_column_error():
#     df = pd.DataFrame({
#         'A': ['foo', 'bar'],
#         'Values': [1, 2]
#     })

#     # 必要なカラムがない場合にエラーが発生するかのテスト
#     with pytest.raises(KeyError):
#         pivot(df, 'Values', 'B')