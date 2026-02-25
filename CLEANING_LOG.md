# Data Cleaning Log - Survey Response Cleaner

Detailed record of all data quality issues identified and decisions made during the cleaning process.

---

## Session Information

- **Date**: 2026-02-25
- **Dataset**: survey_data_messy.csv
- **Rows**: 50
- **Tool**: Python 3.12, pandas

---

## Summary of Issues Found

| Column | Issue Type | Count | Resolution |
|--------|------------|-------|------------|
| gender | Case inconsistency, abbreviations, whitespace | 12 variations → 2 | Mapping dictionary |
| employment_status | Case inconsistency, format variations | 12 variations → 4 | Mapping dictionary |
| department | Abbreviations, typos, suffixes | 30 variations → 5 | Mapping dictionary |
| satisfaction | Case inconsistency | 8 variations → 5 | Mapping dictionary |
| recommend | Case inconsistency, abbreviations, NaN | 10 variations → 3 | Mapping dictionary |
| respondent_name | Titles (Dr., Mr., etc.), case issues | Mixed formats | Remove titles + Title Case |
| feedback | Whitespace, meaningless values | 3 issues | Strip + replace "No comment" with NaN |

---

## Phase 1: Gender Column

### Issues Found

```python
df['gender'].unique()
# Output: ['Male' 'female' 'MALE' 'Female' 'M' 'f' 'male' ' Male' 'F' ' male' 'FEMALE' 'm' ' Male']
```

| Issue Type | Examples |
|------------|----------|
| Case inconsistency | 'male', 'MALE', 'Male' |
| Abbreviations | 'M', 'F', 'm', 'f' |
| Leading whitespace | ' Male', ' male' |

### Decision

- **Standard values**: Male, Female
- **Rationale**: Full words are more readable in reports and dashboards than abbreviations

### Resolution

```python
# Step 1: Strip whitespace
df['gender'] = df['gender'].str.strip()

# Step 2: Apply mapping
gender_mapping = {
    'MALE': 'Male',
    'M': 'Male',
    'male': 'Male',
    'm': 'Male',
    'female': 'Female',
    'f': 'Female',
    'F': 'Female',
    'FEMALE': 'Female'
}
df['gender'] = df['gender'].replace(gender_mapping)
```

### Verified

```python
df['gender'].unique()
# Output: ['Male' 'Female']
```

---

## Phase 2: Employment Status Column

### Issues Found

```python
df['employment_status'].unique()
# Output: ['Full-time' 'full-time' 'Full Time' 'Part-time' 'Fulltime' 'Contract' 
#          'full time' 'Part time' 'Contractor' 'Intern' 'Freelance' 'intern']
```

| Issue Type | Examples |
|------------|----------|
| Case inconsistency | 'full-time', 'Full-time' |
| Format variations | 'Full Time', 'Fulltime', 'Full-time', 'full time' |
| Alternative terms | 'Contractor', 'Freelance' |

### Decision

- **Standard values**: Full-time, Part-time, Contract, Intern
- **Key decision**: Group 'Contractor' and 'Freelance' under 'Contract'
- **Rationale**: Both represent non-permanent workers paid for specific work

### Resolution

```python
# Step 1: Strip whitespace
df['employment_status'] = df['employment_status'].str.strip()

# Step 2: Apply mapping
employ_status_mapping = {
    'full-time': 'Full-time',
    'Full Time': 'Full-time',
    'Fulltime': 'Full-time',
    'full time': 'Full-time',
    'Part time': 'Part-time',
    'Contractor': 'Contract',
    'Freelance': 'Contract',
    'intern': 'Intern'
}
df['employment_status'] = df['employment_status'].replace(employ_status_mapping)
```

### Verified

```python
df['employment_status'].unique()
# Output: ['Full-time' 'Part-time' 'Contract' 'Intern']
```

---

## Phase 3: Department Column

### Issues Found

```python
df['department'].unique()
# Output: 30 unique values!
```

| Standard | Variations Found |
|----------|------------------|
| Sales | 'Sales', 'sales', 'Sales Team', 'sales department' |
| Marketing | 'Marketing', 'marketing', 'Mktg', 'Mkt', 'mktg', 'Mrkting', 'Marketng', 'marketing department' |
| IT | 'IT', 'I.T.', 'Tech', 'Information Technology', 'IT Department', 'information technology' |
| HR | 'HR', 'hr', 'Human Resources', 'Human Resource', 'HR Dept' |
| R&D | 'R&D', 'R and D', 'R & D', 'Research & Development', 'Research and Development', 'Research' |

| Issue Type | Examples |
|------------|----------|
| Case inconsistency | 'sales', 'Sales', 'SALES' |
| Abbreviations | 'Mktg', 'Mkt', 'HR', 'I.T.' |
| Typos | 'Mrkting', 'Marketng' |
| Suffixes | 'IT Department', 'Sales Team', 'marketing department' |
| Full names | 'Information Technology', 'Human Resources' |
| Leading whitespace | '  Marketing' |

### Decision

- **Standard values**: Sales, Marketing, IT, HR, R&D
- **Rationale**: Short, consistent, commonly used department names

### Resolution

```python
# Step 1: Strip whitespace
df['department'] = df['department'].str.strip()

# Step 2: Apply comprehensive mapping
department_mapping = {
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
df['department'] = df['department'].replace(department_mapping)
```

### Verified

```python
df['department'].unique()
# Output: ['Sales' 'Marketing' 'HR' 'IT' 'R&D']
```

---

## Phase 4: Satisfaction Column

### Issues Found

```python
df['satisfaction'].unique()
# Output: ['Very Satisfied' 'very satisfied' 'Satisfied' 'Neutral' 'satisfied' 
#          'Dissatisfied' 'Very Dissatisfied' 'SATISFIED']
```

| Issue Type | Examples |
|------------|----------|
| Case inconsistency | 'satisfied', 'Satisfied', 'SATISFIED' |

### Decision

- **Standard values**: Very Satisfied, Satisfied, Neutral, Dissatisfied, Very Dissatisfied
- **Rationale**: Standard Likert scale format with Title Case

### Resolution

```python
# Step 1: Strip whitespace
df['satisfaction'] = df['satisfaction'].str.strip()

# Step 2: Apply mapping
satisfaction_mapping = {
    'very satisfied': 'Very Satisfied',
    'satisfied': 'Satisfied',
    'SATISFIED': 'Satisfied'
}
df['satisfaction'] = df['satisfaction'].replace(satisfaction_mapping)
```

### Verified

```python
df['satisfaction'].unique()
# Output: ['Very Satisfied' 'Satisfied' 'Neutral' 'Dissatisfied' 'Very Dissatisfied']
```

---

## Phase 5: Recommend Column

### Issues Found

```python
df['recommend'].unique()
# Output: ['Yes' 'yes' 'Maybe' 'No' 'YES' 'maybe' 'Y' 'N' nan 'no']
```

| Issue Type | Examples |
|------------|----------|
| Case inconsistency | 'yes', 'Yes', 'YES' |
| Abbreviations | 'Y', 'N' |
| Missing values | nan (1 row) |

### Decision

- **Standard values**: Yes, No, Maybe
- **Missing values**: Leave as NaN (represents non-response)
- **Rationale**: Full words are clearer; NaN honestly represents missing data

### Resolution

```python
# Step 1: Strip whitespace
df['recommend'] = df['recommend'].str.strip()

# Step 2: Apply mapping
recommend_mapping = {
    'yes': 'Yes',
    'YES': 'Yes',
    'Y': 'Yes',
    'maybe': 'Maybe',
    'N': 'No',
    'no': 'No'
}
df['recommend'] = df['recommend'].replace(recommend_mapping)
```

### Verified

```python
df['recommend'].unique()
# Output: ['Yes' 'Maybe' 'No' nan]
```

---

## Phase 6: Respondent Name Column

### Issues Found

```python
df['respondent_name'].head(20)
# Examples: 'Dr. Robert Brown', 'sarah connor', 'MIKE JOHNSON', 'Mr. David Lee', 'Prof. Lisa Anderson'
```

| Issue Type | Examples |
|------------|----------|
| Titles/Prefixes | 'Dr. ', 'Mr. ', 'Ms. ', 'Mrs. ', 'Prof. ' |
| Case inconsistency | 'sarah connor', 'MIKE JOHNSON' |

### Decision

- **Remove titles**: Names should be clean without honorifics
- **Standardize to Title Case**: Consistent, professional appearance
- **Rationale**: For analysis, we need clean names; titles can be stored separately if needed

### Resolution

```python
# Step 1: Remove titles
titles = ['Dr. ', 'Mr. ', 'Ms. ', 'Mrs. ', 'Prof. ']
for title in titles:
    df['respondent_name'] = df['respondent_name'].str.replace(title, '', regex=False)

# Step 2: Standardize capitalization
df['respondent_name'] = df['respondent_name'].str.title()
```

### Note on regex=False

Used `regex=False` because the dot (.) has special meaning in regular expressions. Using `regex=False` ensures we match the literal text 'Dr. ' rather than treating '.' as "any character".

### Verified

```python
df['respondent_name'].head(10)
# Output: Clean names like 'John Smith', 'Sarah Connor', 'Mike Johnson'
```

---

## Phase 7: Feedback Column

### Issues Found

```python
df['feedback'].value_counts(dropna=False)
# Found:
# - NaN: 2 rows
# - '  It's okay I guess' (leading whitespace)
# - 'No comment' (meaningless feedback)
```

| Issue Type | Count | Examples |
|------------|-------|----------|
| Missing values | 2 | NaN |
| Leading/trailing whitespace | 1 | '  It's okay I guess' |
| Meaningless feedback | 1 | 'No comment' |

### Decision

- **Strip whitespace**: Standard text cleaning
- **Replace "No comment" with NaN**: Not usable feedback
- **Rationale**: "No comment" is functionally the same as not providing feedback — both give us no analyzable content

### Alternative Considered

Could have created a flag column `has_feedback` to distinguish between:
- Forgot to answer (original NaN)
- Chose not to answer ("No comment")
- Provided feedback

For this project, treating both as NaN was sufficient. In a real business context, the distinction might matter.

### Resolution

```python
# Step 1: Strip whitespace
df['feedback'] = df['feedback'].str.strip()

# Step 2: Replace meaningless values with NaN
df['feedback'] = df['feedback'].replace('No comment', np.nan)
```

### Verified

```python
df['feedback'].isna().sum()
# Output: 3 (2 original + 1 "No comment")
```

---

## Final Validation

```python
print(df['gender'].unique())           # ['Male' 'Female']
print(df['employment_status'].unique()) # ['Full-time' 'Part-time' 'Contract' 'Intern']
print(df['department'].unique())        # ['Sales' 'Marketing' 'HR' 'IT' 'R&D']
print(df['satisfaction'].unique())      # ['Very Satisfied' 'Satisfied' 'Neutral' 'Dissatisfied' 'Very Dissatisfied']
print(df['recommend'].unique())         # ['Yes' 'Maybe' 'No' nan]
```

### Missing Values Summary

| Column | Missing Count | Reason |
|--------|---------------|--------|
| recommend | 1 | Original non-response |
| feedback | 3 | 2 original + 1 "No comment" |

These are legitimate missing values representing non-responses.

---

## Key Learnings

1. **Always strip whitespace first** — ' Male' and 'Male' are different strings to Python

2. **Use `.unique()` and `.value_counts()`** — Essential for discovering all variations

3. **Mapping dictionaries are powerful** — Clean way to handle many variations

4. **Document your decisions** — Why did you group Freelance with Contract? Future you needs to know

5. **regex=False for literal matching** — Safer when your text contains special characters like '.'

6. **Context matters for missing values** — "No comment" vs NaN might mean different things in different analyses

---

## Techniques Used

| Task | Method |
|------|--------|
| Strip whitespace | `df['col'].str.strip()` |
| Check unique values | `df['col'].unique()` |
| Count values | `df['col'].value_counts(dropna=False)` |
| Remap categories | `df['col'].replace(mapping_dict)` |
| Remove text patterns | `df['col'].str.replace('pattern', '', regex=False)` |
| Standardize case | `df['col'].str.title()` |
| Check membership | `df[~df['col'].isin(valid_list)]` |
