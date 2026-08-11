"""
Schema aliases.

This module contains known aliases used for automatic
schema detection.

Each logical column type maps to a collection of
possible column names encountered in real datasets.

These aliases are consumed by SchemaDetector and
InferenceEngine.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from typing import Final

# ==================================================
# Column Aliases
# ==================================================

ALIASES: Final[dict[str, frozenset[str]]] = {

    # --------------------------------------------------
    # Identifier
    # --------------------------------------------------

    "id": frozenset({

        "id",
        "customer_id",
        "consumer_id",
        "record_id",
        "user_id",
        "member_id",

    }),

    # --------------------------------------------------
    # Name
    # --------------------------------------------------

    "name": frozenset({

        "name",
        "full_name",
        "fullname",
        "customer_name",
        "consumer_name",

    }),

    "first_name": frozenset({

        "first_name",
        "firstname",
        "given_name",

    }),

    "last_name": frozenset({

        "last_name",
        "lastname",
        "surname",
        "family_name",

    }),

    # --------------------------------------------------
    # Email
    # --------------------------------------------------

    "email": frozenset({

        "email",

        "email_address",

        "emailaddress",

        "e_mail",

        "e-mail",

        "primary_email",

        "work_email",

        "business_email",

        "contact_email",

    }),

    # --------------------------------------------------
    # Phone
    # --------------------------------------------------

    "phone": frozenset({

        "phone",

        "phone_number",

        "telephone",

        "mobile",

        "cell",

        "contact_phone",

        "business_phone",

        "work_phone",

    }),

    # --------------------------------------------------
    # Website
    # --------------------------------------------------

    "website": frozenset({

        "website",

        "url",

        "web",

        "domain",

        "homepage",

        "company_website",

    }),

    # --------------------------------------------------
    # Address
    # --------------------------------------------------

    "address": frozenset({

        "address",

        "street",

        "street_address",

        "address_line_1",

        "address1",

    }),

    # --------------------------------------------------
    # City
    # --------------------------------------------------

    "city": frozenset({

        "city",

        "town",

        "municipality",

    }),

    # --------------------------------------------------
    # State
    # --------------------------------------------------

    "state": frozenset({

        "state",

        "province",

        "region",

    }),

    # --------------------------------------------------
    # Country
    # --------------------------------------------------

    "country": frozenset({

        "country",

        "country_code",

        "nation",

    }),

    # --------------------------------------------------
    # ZIP
    # --------------------------------------------------

    "zip_code": frozenset({

        "zip",

        "zipcode",

        "zip_code",

        "postal",

        "postal_code",

    }),

    # --------------------------------------------------
    # Date
    # --------------------------------------------------

    "date": frozenset({

        "date",

        "created",

        "updated",

        "created_at",

        "updated_at",

        "birth_date",

        "dob",

        "joined",

        "registration_date",

    }),

}