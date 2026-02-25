"""
Survey Data Cleaning Utilities
Reusable functions for cleaning text and categorical data.
"""

import pandas as pd
import numpy as np


# =============================================================================
# VALID VALUES (Membership Constraints)
# =============================================================================

VALID_GENDERS = ['Male', 'Female', 'Other']
VALID_EMPLOYMENT = ['Full-time', 'Part-time', 'Contract', 'Intern']
VALID_DEPARTMENTS = ['Sales', 'Marketing', 'IT', 'HR', 'R&D']
VALID_SATISFACTION = ['Very Satisfied', 'Satisfied', 'Neutral', 'Dissatisfied', 'Very Dissatisfied']
VALID_RECOMMEND = ['Yes', 'No', 'Maybe']


# =============================================================================
# MAPPING DICTIONARIES
# =============================================================================

GENDER_MAPPING = {
    'MALE': 'Male',
    'M': 'Male',
    'male': 'Male',
    'm': 'Male',
    'female': 'Female',
    'f': 'Female',
    'F': 'Female',
    'FEMALE': 'Female'
}

EMPLOYMENT_MAPPING = {
    'full-time': 'Full-time',
    'Full Time': 'Full-time',
    'Fulltime': 'Full-time',
    'full time': 'Full-time',
    'Part time': 'Part-time',
    'Contractor': 'Contract',
    'Freelance': 'Contract',
    'intern': 'Intern'
}

DEPARTMENT_MAPPING = {
    # Sales variations
    'sales': 'Sales',
    'Sales Team': 'Sales',
    'sales department': 'Sales',
    
    # Marketing variations
    'marketing': 'Marketing',
    'Mktg': 'Marketing',
    'Mkt': 'Marketing',
    'mktg': 'Marketing',
    'Mrkting': 'Marketing',
    'Marketng': 'Marketing',
    'marketing department': 'Marketing',
    
    # IT variations
    'I.T.': 'IT',
    'Tech': 'IT',
    'Information Technology': 'IT',
    'IT Department': 'IT',
    'information technology': 'IT',
    
    # HR variations
    'hr': 'HR',
    'Human Resources': 'HR',
    'Human Resource': 'HR',
    'HR Dept': 'HR',
    
    # R&D variations
    'R and D': 'R&D',
    'R & D': 'R&D',
    'Research & Development': 'R&D',
    'Research and Development': 'R&D',
    'Research': 'R&D'
}

SATISFACTION_MAPPING = {
    'very satisfied': 'Very Satisfied',
    'satisfied': 'Satisfied',
    'SATISFIED': 'Satisfied'
}

RECOMMEND_MAPPING = {
    'yes': 'Yes',
    'YES': 'Yes',
    'Y': 'Yes',
    'maybe': 'Maybe',
    'N': 'No',
    'no': 'No'
}


# =============================================================================
# CLEANING FUNCTIONS
# =============================================================================

def standardize_column(df: pd.DataFrame, column: str, mapping: dict) -> pd.DataFrame:
    """
    Strip whitespace and apply mapping to standardize a categorical column.
    
    Parameters:
        df: DataFrame to modify
        column: Column name to standardize
        mapping: Dictionary mapping old values to new values
    
    Returns:
        DataFrame with standardized column
    """
    df = df.copy()
    df[column] = df[column].str.strip()
    df[column] = df[column].replace(mapping)
    return df


def remove_titles(df: pd.DataFrame, column: str, titles: list = None) -> pd.DataFrame:
    """
    Remove titles/prefixes from a name column and standardize to Title Case.
    
    Parameters:
        df: DataFrame to modify
        column: Column name containing names
        titles: List of titles to remove (default: Dr., Mr., Ms., Mrs., Prof.)
    
    Returns:
        DataFrame with cleaned name column
    """
    if titles is None:
        titles = ['Dr. ', 'Mr. ', 'Ms. ', 'Mrs. ', 'Prof. ']
    
    df = df.copy()
    for title in titles:
        df[column] = df[column].str.replace(title, '', regex=False)
    df[column] = df[column].str.title()
    return df


def clean_feedback(df: pd.DataFrame, column: str, meaningless: list = None) -> pd.DataFrame:
    """
    Clean feedback column by stripping whitespace and converting meaningless values to NaN.
    
    Parameters:
        df: DataFrame to modify
        column: Column name containing feedback
        meaningless: List of values to treat as missing (default: ['No comment'])
    
    Returns:
        DataFrame with cleaned feedback column
    """
    if meaningless is None:
        meaningless = ['No comment', 'N/A', 'n/a', 'None', '-', '']
    
    df = df.copy()
    df[column] = df[column].str.strip()
    df[column] = df[column].replace(meaningless, np.nan)
    return df


def check_membership(df: pd.DataFrame, column: str, valid_values: list) -> pd.DataFrame:
    """
    Find rows where column values are not in the valid set.
    
    Parameters:
        df: DataFrame to check
        column: Column name to validate
        valid_values: List of allowed values
    
    Returns:
        DataFrame with invalid rows only
    """
    # Exclude NaN from invalid check (NaN is acceptable as missing)
    mask = ~df[column].isin(valid_values) & df[column].notna()
    return df[mask]


def validate_survey_data(df: pd.DataFrame) -> dict:
    """
    Validate that cleaned data meets all membership constraints.
    
    Returns:
        Dictionary with validation results
    """
    results = {
        'gender': check_membership(df, 'gender', VALID_GENDERS),
        'employment_status': check_membership(df, 'employment_status', VALID_EMPLOYMENT),
        'department': check_membership(df, 'department', VALID_DEPARTMENTS),
        'satisfaction': check_membership(df, 'satisfaction', VALID_SATISFACTION),
        'recommend': check_membership(df, 'recommend', VALID_RECOMMEND)
    }
    
    all_valid = all(len(v) == 0 for v in results.values())
    
    return {
        'all_valid': all_valid,
        'invalid_counts': {k: len(v) for k, v in results.items()},
        'invalid_rows': results
    }


def clean_survey_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Complete cleaning pipeline for survey data.
    
    Parameters:
        df: Raw DataFrame to clean
    
    Returns:
        Tuple of (cleaned DataFrame, cleaning report dictionary)
    """
    df_clean = df.copy()
    report = {
        'original_rows': len(df),
        'steps': []
    }
    
    # Step 1: Gender
    before = df_clean['gender'].nunique()
    df_clean = standardize_column(df_clean, 'gender', GENDER_MAPPING)
    after = df_clean['gender'].nunique()
    report['steps'].append(f"Gender: {before} → {after} unique values")
    
    # Step 2: Employment Status
    before = df_clean['employment_status'].nunique()
    df_clean = standardize_column(df_clean, 'employment_status', EMPLOYMENT_MAPPING)
    after = df_clean['employment_status'].nunique()
    report['steps'].append(f"Employment Status: {before} → {after} unique values")
    
    # Step 3: Department
    before = df_clean['department'].nunique()
    df_clean = standardize_column(df_clean, 'department', DEPARTMENT_MAPPING)
    after = df_clean['department'].nunique()
    report['steps'].append(f"Department: {before} → {after} unique values")
    
    # Step 4: Satisfaction
    before = df_clean['satisfaction'].nunique()
    df_clean = standardize_column(df_clean, 'satisfaction', SATISFACTION_MAPPING)
    after = df_clean['satisfaction'].nunique()
    report['steps'].append(f"Satisfaction: {before} → {after} unique values")
    
    # Step 5: Recommend
    before = df_clean['recommend'].nunique()
    df_clean = standardize_column(df_clean, 'recommend', RECOMMEND_MAPPING)
    after = df_clean['recommend'].nunique()
    report['steps'].append(f"Recommend: {before} → {after} unique values")
    
    # Step 6: Names
    df_clean = remove_titles(df_clean, 'respondent_name')
    report['steps'].append("Names: Removed titles, applied Title Case")
    
    # Step 7: Feedback
    before_na = df_clean['feedback'].isna().sum()
    df_clean = clean_feedback(df_clean, 'feedback')
    after_na = df_clean['feedback'].isna().sum()
    report['steps'].append(f"Feedback: {before_na} → {after_na} missing values")
    
    # Validate
    validation = validate_survey_data(df_clean)
    report['validation_passed'] = validation['all_valid']
    
    return df_clean, report


def print_cleaning_report(report: dict) -> None:
    """Print formatted cleaning report."""
    print("=" * 50)
    print("CLEANING REPORT")
    print("=" * 50)
    print(f"Original rows: {report['original_rows']}")
    print("\nSteps completed:")
    for step in report['steps']:
        print(f"  ✓ {step}")
    print("-" * 50)
    print(f"Validation: {'✓ PASSED' if report['validation_passed'] else '✗ FAILED'}")
    print("=" * 50)


# =============================================================================
# RUN IF EXECUTED DIRECTLY
# =============================================================================

if __name__ == "__main__":
    # Load data
    df = pd.read_csv('data/raw/survey_data_messy.csv')
    print(f"Loaded {len(df)} rows\n")
    
    # Clean data
    df_clean, report = clean_survey_data(df)
    print_cleaning_report(report)
    
    # Save
    df_clean.to_csv('data/processed/survey_data_clean.csv', index=False)
    print("\nCleaned data saved to data/processed/survey_data_clean.csv")
