from typing import List
from extras.graph_api.data import graphdataclass


@graphdataclass
class User:
    id: str = None
    business_phones: List[str] = None
    display_name: str = None
    given_name: str = None
    job_title: str = None
    mail: str = None
    mobile_phone: str = None
    office_location: str = None
    preferred_language: str = None
    surname: str = None
    user_principal_name: str = None
