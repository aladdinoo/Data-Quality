# Data Quality Audit Platform

Python-based data quality and audit platform for validating customer data,
generating a non-destructive flag preview, collecting audit evidence,
and reconciling the execution before producing a success manifest.

## Current Status

**76 tests passed, 2 warnings — TEST SUITE GREEN**

```text
                    customers.csv
                 10,000 rows / 33 cols
                         |
                         v
                +-------------------+
                | Validation Engine |
                |    10 rules       |
                +---------+---------+
                          |
                 +--------+--------+
                 v                 v
          +-------------+   +----------------+
          | Flag Preview|   | Audit Evidence|
          | Source +    |   | Hashes / files|
          | quality flags|  |                |
          +------+------+   +-------+--------+
                 |                  |
                 +--------+---------+
                          v
                 +-------------------+
                 |  Reconciliation   |
                 | row count / DDL   |
                 | source unchanged  |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | SUCCESS MANIFEST  |
                 +-------------------+
```

## Completed

- 10 validation rules loaded and executed.
- End-to-end audit against the real source.
- Source remains read-only.
- Row-count preservation verified.
- Schema / DDL preservation verified.
- Production changes are detected.
- Source writes are detected.
- Non-destructive Flag Preview generated.
- Audit evidence and success manifest generated.
- Reconciliation checks implemented.
- Automated tests cover validation, flags, evidence, audit execution,
  and reconciliation.
- **76 tests passing.**

## Validation Rules

1. Email validation
2. Phone validation
3. Website validation
4. ZIP validation
5. Name validation
6. Date validation
7. Duplicate validation
8. Schema validation
9. Invariant validation
10. PII validation

## Source Contract

The current real-source test uses:

- **10,000 rows**
- **33 source columns**

```text
id
email_address
first_name
last_name
address
city
county_name
state
zip
website_source
phone_number
gender
dob
registration_date
valid
extra
email_id
ethnicity
ownrent
domain
main_interest
sub_interest
latitude
longitude
uploaded
country
websource_id
interest_ids
DNC
source
first_name_norm
last_name_norm
zip_norm
```

The Flag Preview preserves the source columns and adds the required
quality/audit flag columns.

## Project Structure

```text
app/             Application configuration
audit/           Audit execution, evidence and reconciliation
auditing/        Auditing components
cleaning/        Cleaning components
core/            Core pipeline components
evidence/        Evidence artifacts
extract/         Data extraction
flag_preview/    Non-destructive quality flags
profiling/       Data profiling
reporting/       Reporting
rules/           Validation rules
runner/          Pipeline runners
sample_data/     Test/source data
schema/          Schema handling
storage/         Storage layer
tests/           Automated tests
validation/      Validation engine
validators/      Validation utilities
```

## Running Tests

From the project root:

```powershell
python -m pytest -vv -s
```

Expected:

```text
76 passed, 2 warnings
```

### Real-source audit

```powershell
python -m pytest tests/test_e2e_audit_execution.py::test_e2e_audit_run_real_source -vv -s
```

### Real-artifact test

```powershell
python -m pytest tests/test_e2e_audit_artifact.py -vv -s
```

## Non-Destructive Audit Model

```text
RAW SOURCE
    |
    +-- Validation
    +-- Flag Preview
    +-- Evidence Collection
             |
             v
       Reconciliation
             |
             v
      Success Manifest
```

The audit verifies that rows are preserved, the source schema remains
unchanged, the source is not written to, production data is not modified,
and execution evidence is produced.

## Next Steps

- Replace deprecated `datetime.utcnow()` usage with timezone-aware UTC.
- Expand audit and reporting capabilities.
- Strengthen versioned rule contracts.
- Add GitHub Actions CI.
- Expand operational documentation.
- Strengthen evidence and monitoring.

## Repository

https://github.com/aladdinoo/Data-Quality
