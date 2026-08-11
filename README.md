Data Quality Audit Platform

A Python-based data quality and audit platform for validating customer data,generating a non-destructive flag preview, collecting audit evidence,and reconciling the execution before producing a success manifest.

Current Status

76 tests passed, 2 warnings — TEST SUITE GREEN

Current source dataset:

10,000 rows

33 source columns

10 validation rules

Audit Flow

customers.csv
10,000 rows / 33 columns
          |
          v
  Validation Engine
     10 rules
          |
     +----+----+
     |         |
     v         v
Flag Preview  Evidence
     |         |
     +----+----+
          |
          v
   Reconciliation
          |
          v
   SUCCESS MANIFEST

Validation Rules

The platform currently executes 10 validation rules across the33-column source dataset:

Email validation

Phone validation

Website validation

ZIP validation

Name validation

Date validation

Duplicate validation

Schema validation

Invariant validation

PII validation

Source Dataset

The current real-source test uses:

File: sample_data/customers.csv

Rows: 10,000

Columns: 33

The source schema is:

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

What Is Completed

Real-source end-to-end audit execution

10 validation rules loaded and executed

Non-destructive Flag Preview generation

Source row-count preservation

Source/schema reconciliation

DDL change detection

Production-change detection

Source-write detection

Audit evidence generation

Success manifest generation

Automated validation and audit tests

76 tests passing

Project Structure

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

Requirements

Python 3.13+

Install the project dependencies if a requirements file is provided:

python -m pip install -r requirements.txt

Run the Test Suite

Run all tests from the project root:

python -m pytest -vv -s

Expected result:

76 passed, 2 warnings

Run the Real-Source Audit Test

python -m pytest tests/test_e2e_audit_execution.py::test_e2e_audit_run_real_source -vv -s

Expected:

PASSED

Run the Real-Artifact Audit Test

python -m pytest tests/test_e2e_audit_artifact.py -vv -s

Expected:

PASSED

Non-Destructive Audit

The audit process does not modify the original source data.

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

The reconciliation verifies:

Row count remains unchanged.

Source schema / DDL remains unchanged.

Production data remains unchanged.

No write is performed against the source.

Evidence is produced for the audit run.

A success manifest is generated when all checks pass.

Test Result

Latest full test execution:

76 passed, 2 warnings

The warnings are deprecation warnings related todatetime.utcnow() and do not currently cause test failures.

Next Steps

Replace deprecated datetime.utcnow() with timezone-aware UTC timestamps.

Add GitHub Actions CI.

Strengthen versioned rule contracts.

Expand audit and reporting capabilities.

Improve operational documentation.

Strengthen evidence and monitoring.

