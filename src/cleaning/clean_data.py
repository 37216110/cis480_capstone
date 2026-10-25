"""Clean the AI4I 2020 dataset"""
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_CSV = PROJECT_ROOT / 'data' / 'raw' / 'ai4i2020.csv'
OUTPUT_DIR = PROJECT_ROOT / 'data' / 'cleaned'
CLEAN_CSV = OUTPUT_DIR / 'ai4i2020_cleaned.csv'
MODEL_CSV = OUTPUT_DIR / 'ai4i2020_modeling.csv'
NO_INCONSISTENT_CSV = OUTPUT_DIR / 'ai4i2020_no_inconsistent.csv'
MODEL_AND_NO_INCONSISTENT_CSV = OUTPUT_DIR / \
    'ai4i2020_modeling_no_inconsistent.csv'

FAILURE_COLS = ['TWF', 'HDF', 'PWF', 'OSF', 'RNF']
BINARY_COLS = ['Machine failure', *FAILURE_COLS]
NUMERIC_COLS = [
    'Air temperature [K]', 'Process temperature [K]',
    'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]'
]
PREDICTORS = ['Type', *NUMERIC_COLS]
TARGET = 'Machine failure'
REQUIRED_COLS = ['UDI', 'Product ID', *PREDICTORS, TARGET, *FAILURE_COLS]


def clean_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    missing_cols = set(REQUIRED_COLS) - set(df_raw.columns)
    if missing_cols:
        raise ValueError(f'Missing required columns: {sorted(missing_cols)}')

    df = df_raw.copy()
    if df[REQUIRED_COLS].isna().any().any():
        raise ValueError(
            'Raw dataset has missing values; investigate before proceeding.')
    if df.duplicated().any():
        raise ValueError(
            'Raw dataset has duplicate rows; investigate before proceeding.')
    for col in BINARY_COLS:
        if not df[col].isin([0, 1]).all():
            raise ValueError(f'{col} must contain only 0 or 1.')

    if not df['Type'].isin(['L', 'M', 'H']).all():
        raise ValueError('Unexpected product Type.')
    for col in ['UDI', 'Product ID']:
        if not df[col].is_unique:
            raise ValueError(f'{col} must be unique.')
    for col in ['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]']:
        if not (df[col] > 0).all():
            raise ValueError(f'{col} must be positive.')
    for col in ['Torque [Nm]', 'Tool wear [min]']:
        if not (df[col] >= 0).all():
            raise ValueError(f'{col} cannot be negative.')

    assert not df.isna().any().any()
    assert not df.duplicated().any()
    print(f'Cleaned rows: {len(df):,}; columns: {df.shape[1]}')
    print('Failure distribution:')
    print(df[TARGET].value_counts().sort_index().to_string())
    return df


def remove_inconsistent_rows(df: pd.DataFrame) -> pd.DataFrame:
    inconsistent = df[TARGET].ne(df[FAILURE_COLS].max(axis=1))

    df_no_inconsistent = df.loc[~inconsistent].copy().reset_index(drop=True)

    assert df_no_inconsistent[TARGET].eq(
        df_no_inconsistent[FAILURE_COLS].max(axis=1)).all()

    print(f'Inconsistent failure labels removed: {inconsistent.sum():,}')
    return df_no_inconsistent


def main():
    df_raw = pd.read_csv(INPUT_CSV)
    df_clean = clean_data(df_raw)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(CLEAN_CSV, index=False)
    df_clean[[*PREDICTORS, TARGET]].to_csv(MODEL_CSV, index=False)
    print(f'Cleaned dataset saved to: {CLEAN_CSV}')
    print(f'Modeling dataset saved to: {MODEL_CSV}')

    df_inconsistent_removed = remove_inconsistent_rows(df_clean)
    df_inconsistent_removed.to_csv(NO_INCONSISTENT_CSV, index=False)

    df_inconsistent_removed[[*PREDICTORS, TARGET]
                            ].to_csv(MODEL_AND_NO_INCONSISTENT_CSV, index=False)
    print(
        f'Cleaned dataset with no inconsistent labels saved to: {NO_INCONSISTENT_CSV}')
    print(
        f'Modeling dataset with no inconsistent labels saved to: {MODEL_AND_NO_INCONSISTENT_CSV}')


if __name__ == '__main__':
    main()
