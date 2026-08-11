from pathlib import Path

from audit.source_evidence import SourceEvidenceReader


SOURCE_FILE = Path(
    r"C:\Users\LENOVO Pro\Desktop\tips"
    r"\sample_data\customers.csv"
)


def test_real_source_evidence():
    evidence = SourceEvidenceReader.read_csv(
        SOURCE_FILE
    )

    assert evidence.source_file == SOURCE_FILE

    assert evidence.row_count == 10_000

    assert evidence.column_count == 33

    assert evidence.columns == (
        "id",
        "email_address",
        "first_name",
        "last_name",
        "address",
        "city",
        "county_name",
        "state",
        "zip",
        "website_source",
        "phone_number",
        "gender",
        "dob",
        "registration_date",
        "valid",
        "extra",
        "email_id",
        "ethnicity",
        "ownrent",
        "domain",
        "main_interest",
        "sub_interest",
        "latitude",
        "longitude",
        "uploaded",
        "country",
        "websource_id",
        "interest_ids",
        "DNC",
        "source",
        "first_name_norm",
        "last_name_norm",
        "zip_norm",
    )