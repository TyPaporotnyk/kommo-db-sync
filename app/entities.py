from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class Lead:
    id: int
    name: str
    price: int
    responsible_user_id: int
    group_id: int
    status_id: int
    pipeline_id: int
    loss_reason_id: Optional[int]
    created_by: int
    updated_by: int
    created_at: int
    updated_at: int
    closed_at: Optional[int]
    closest_task_at: Optional[int]
    is_deleted: bool
    score: Optional[float]
    account_id: int
    labor_cost: Optional[float]
    source: Optional[str]
    payment_type: Optional[str]
    readiness_to_buy: Optional[str]
    object_type: Optional[str]
    purchase_purpose: Optional[str]
    meeting_format: Optional[str]
    meeting_scheduled_datetime: Optional[int]
    zoom_link: Optional[str]
    deposit_date: Optional[int]
    meeting_conducted_date: Optional[int]
    deal_date: Optional[int]
    payment_method: Optional[str]
    down_payment_percent: Optional[float]
    apartment_number: Optional[str]
    apartment_cost: Optional[float]
    apartment_status: Optional[str]
    comment: Optional[str]
    referrer: Optional[str]
    tag_name: Optional[str]
    tag_id: Optional[int]
    company_id: Optional[int]
    contact_id: Optional[int]


@dataclass
class Contact:
    id: int
    name: str
    first_name: Optional[str]
    last_name: Optional[str]
    responsible_user_id: int
    group_id: int
    created_by: int
    updated_by: int
    created_at: int
    updated_at: int
    closest_task_at: Optional[int]
    is_deleted: bool
    is_unsorted: bool
    account_id: int
    phone: Optional[str]
    email: Optional[str]
    position: Optional[str]
    company_name: Optional[str]
    company_id: Optional[int]
    tag_id: Optional[int]
    tag_name: Optional[str]
    apartment: Optional[str]
    was_in_bali: Optional[str]
    geography: Optional[str]
    language: Optional[str]


@dataclass
class Company:
    id: int
    name: str
    responsible_user_id: int
    group_id: int
    created_by: int
    updated_by: int
    created_at: int
    updated_at: int
    account_id: int
    closest_task_at: Optional[int]
    is_deleted: bool
    tag_id: Optional[int]
    tag_name: Optional[str]
    phone: Optional[str]
    broker: Optional[str]


@dataclass
class Task:
    id: int
    created_by: int
    updated_by: int
    created_at: int
    updated_at: int
    responsible_user_id: int
    group_id: int
    entity_id: Optional[int]
    entity_type: Optional[str]
    duration: int
    is_completed: bool
    task_type_id: int
    text: str
    result: List[Any]
    complete_till: int
    account_id: int


@dataclass
class User:
    id: int
    name: str
    email: str
    lang: str


@dataclass
class Event:
    id: str
    type: str
    entity_id: int
    entity_type: str
    created_by: int
    created_at: int
    account_id: int
    value_after_field_id: Optional[int]
    value_after_field_type: Optional[int]
    value_after_enum_id: Optional[int]
    value_after_text: Optional[str]
    value_before_field_id: Optional[int]
    value_before_field_type: Optional[int]
    value_before_enum_id: Optional[int]
    value_before_text: Optional[str]


@dataclass
class Status:
    id: int
    name: str
    sort: int
    is_editable: bool
    pipeline_id: int
    color: str
    type: int
    account_id: int


@dataclass
class Pipeline:
    id: int
    name: str
    sort: int
    is_main: bool
    is_unsorted_on: bool
    is_archive: bool
    account_id: int
    statuses: List[Status]
