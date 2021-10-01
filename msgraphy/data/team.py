from datetime import date

from msgraphy.data import graphdataclass


@graphdataclass
class Team:
    display_name: str = None
    description: str = None
    classification: str = None
    specialization = None
    visibility = None
    fun_settings = None
    guest_settings = None
    internal_id: str = None
    is_archived: bool = None
    member_settings = None
    messaging_settings = None
    web_url: str = None
    created_date_time: date = None
