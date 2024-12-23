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
