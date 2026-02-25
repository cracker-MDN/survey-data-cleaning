# Survey Response Data Cleaning Project

A data cleaning project demonstrating systematic standardization of text and categorical data using Python and pandas.

## Project Overview

This project takes messy employee survey data (50 responses) and applies text cleaning and category standardization techniques to produce analysis-ready data. It demonstrates practical skills in handling real-world categorical data problems.

### The Challenge

The raw dataset contained multiple text and categorical data issues:
- Inconsistent capitalization (male, Male, MALE)
- Abbreviations mixed with full words (M vs Male, Mktg vs Marketing)
- Typos in category names (Marketng, Mrkting)
- Leading/trailing whitespace
- Titles mixed with names (Dr., Mr., Ms., Prof.)
- Meaningless feedback entries ("No comment")

### The Approach

Applied a systematic cleaning methodology for each categorical column:

1. **Explore**: Check unique values with `.unique()` and `.value_counts()`
2. **Strip**: Remove whitespace first (always!)
3. **Map**: Create dictionary mapping variations to standard values
4. **Verify**: Confirm only valid values remain

## Results Summary

| Column | Before | After |
|--------|--------|-------|
| gender | 12 variations | 2 (Male, Female) |
| employment_status | 12 variations | 4 (Full-time, Part-time, Contract, Intern) |
| department | 30 variations | 5 (Sales, Marketing, IT, HR, R&D) |
| satisfaction | 8 variations | 5 (Likert scale) |
| recommend | 10 variations | 3 (Yes, No, Maybe) |
| respondent_name | Titles + case issues | Clean Title Case |
| feedback | Whitespace + meaningless | Clean text |

## Issues Found & Solutions

### 1. Gender Column (12 → 2 values)

| Issue Type | Examples | Solution |
|------------|----------|----------|
| Case inconsistency | male, MALE, Male | Mapping dictionary |
| Abbreviations | M, F, m, f | Expand to full word |
| Whitespace | ' Male', ' male' | `.str.strip()` |

### 2. Department Column (30 → 5 values)

The messiest column with multiple issue types:

| Issue Type | Examples | Solution |
|------------|----------|----------|
| Abbreviations | Mktg, Mkt, HR, I.T. | Mapping dictionary |
| Typos | Marketng, Mrkting | Mapping dictionary |
| Suffixes | IT Department, Sales Team | Mapping dictionary |
| Full names | Information Technology | Mapping dictionary |

### 3. Respondent Names

| Issue | Solution |
|-------|----------|
| Titles (Dr., Mr., Ms., Prof., Mrs.) | Loop with `.str.replace()` |
| Case inconsistency | `.str.title()` |

### 4. Feedback Column

| Issue | Decision | Rationale |
|-------|----------|-----------|
| "No comment" | Convert to NaN | Not analyzable feedback |
| Whitespace | Strip | Standard cleaning |

## Project Structure

```
chapter2_survey_cleaner/
├── README.md                    # Project documentation
├── CLEANING_LOG.md              # Detailed cleaning decisions
├── requirements.txt             # Python dependencies
├── data/
│   ├── raw/
│   │   └── survey_data_messy.csv
│   └── processed/
│       └── survey_data_clean.csv
├── notebooks/
│   └── data_cleaning.ipynb
└── src/
    └── cleaning_utils.py
```

## Skills Demonstrated

- **Text Cleaning**: `.str.strip()`, `.str.title()`, `.str.replace()`
- **Category Standardization**: Mapping dictionaries with `.replace()`
- **Membership Constraints**: Validating against allowed values
- **Pattern Removal**: Removing titles from names
- **Missing Value Decisions**: Context-appropriate handling

## How to Run

1. Clone the repository:
```bash
git clone https://github.com/yourusername/survey-data-cleaning.git
cd survey-data-cleaning
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the notebook:
```bash
jupyter notebook notebooks/data_cleaning.ipynb
```

## Key Learnings

1. **Always strip whitespace first** — ' Male' and 'Male' are different strings

2. **Use `.unique()` liberally** — You can't fix what you don't know exists

3. **Mapping dictionaries scale well** — Handle dozens of variations cleanly

4. **Document your decisions** — Why group Freelance with Contract? Write it down

5. **Context matters** — "No comment" vs NaN might mean different things

## Techniques Reference

```python
# Strip whitespace
df['col'] = df['col'].str.strip()

# Check unique values
df['col'].unique()
df['col'].value_counts(dropna=False)

# Remap categories
mapping = {'old': 'new', 'old2': 'new'}
df['col'] = df['col'].replace(mapping)

# Remove text patterns
df['col'] = df['col'].str.replace('Dr. ', '', regex=False)

# Standardize case
df['col'] = df['col'].str.title()

# Check membership
valid = ['A', 'B', 'C']
invalid_rows = df[~df['col'].isin(valid)]
```

## Technologies Used

- Python 3.12
- pandas 2.0+
- NumPy
- Jupyter Notebook

## Dataset

Synthetic employee survey data created for learning purposes. Contains responses with fields:
- `response_id`: Unique identifier
- `respondent_name`: Employee name
- `age`: Employee age
- `gender`: Male/Female
- `department`: Sales, Marketing, IT, HR, R&D
- `employment_status`: Full-time, Part-time, Contract, Intern
- `salary_range`: Salary bracket
- `satisfaction`: Likert scale rating
- `recommend`: Yes/No/Maybe
- `feedback`: Open text feedback
- `survey_date`: Response date

## Author

[MD Noornabi]

## License

MIT License - feel free to use for learning!
