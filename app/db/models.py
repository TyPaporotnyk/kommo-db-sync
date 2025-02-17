from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, and_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer)
    responsible_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(Integer)
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"))
    pipeline_id: Mapped[int] = mapped_column(ForeignKey("pipelines.id"))
    loss_reason_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_by: Mapped[int] = mapped_column(Integer)
    updated_by: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    closest_task_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    account_id: Mapped[int] = mapped_column(Integer)
    labor_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    payment_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    readiness_to_buy: Mapped[str | None] = mapped_column(String(255), nullable=True)
    object_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    purchase_purpose: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meeting_format: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meeting_scheduled_datetime: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    zoom_link: Mapped[str | None] = mapped_column(String(255), nullable=True)
    deposit_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    meeting_conducted_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    deal_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    payment_method: Mapped[str | None] = mapped_column(String(255), nullable=True)
    down_payment_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    apartment_number: Mapped[str | None] = mapped_column(String(255), nullable=True)
    apartment_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    apartment_status: Mapped[str | None] = mapped_column(String(255), nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    referrer: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tag_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tag_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), nullable=True)

    # Relationships
    responsible_user: Mapped["User"] = relationship(back_populates="leads")
    status: Mapped["Status"] = relationship(back_populates="leads")
    pipeline: Mapped["Pipeline"] = relationship(back_populates="leads")
    company: Mapped["Company"] = relationship(back_populates="leads")
    
    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        primaryjoin="and_(Task.entity_type=='leads', foreign(Task.entity_id)==Lead.id)",
        viewonly=True
    )
    
    events: Mapped[List["Event"]] = relationship(
        "Event",
        primaryjoin="and_(Event.entity_type=='leads', foreign(Event.entity_id)==Lead.id)",
        viewonly=True
    )


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    responsible_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(Integer)
    created_by: Mapped[int] = mapped_column(Integer)
    updated_by: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    closest_task_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean)
    is_unsorted: Mapped[bool] = mapped_column(Boolean)
    account_id: Mapped[int] = mapped_column(Integer)
    phone: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    position: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), nullable=True)
    tag_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tag_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    apartment: Mapped[str | None] = mapped_column(String(255), nullable=True)
    was_in_bali: Mapped[str | None] = mapped_column(String(255), nullable=True)
    geography: Mapped[str | None] = mapped_column(String(255), nullable=True)
    language: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    responsible_user: Mapped["User"] = relationship(back_populates="contacts")
    company: Mapped["Company"] = relationship(back_populates="contacts")
    
    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        primaryjoin="and_(Task.entity_type=='contacts', foreign(Task.entity_id)==Contact.id)",
        viewonly=True
    )
    
    events: Mapped[List["Event"]] = relationship(
        "Event",
        primaryjoin="and_(Event.entity_type=='contacts', foreign(Event.entity_id)==Contact.id)",
        viewonly=True
    )


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    responsible_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(Integer)
    created_by: Mapped[int] = mapped_column(Integer)
    updated_by: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    account_id: Mapped[int] = mapped_column(Integer)
    closest_task_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean)
    tag_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tag_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(255), nullable=True)
    broker: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    responsible_user: Mapped["User"] = relationship(back_populates="companies")
    contacts: Mapped[List["Contact"]] = relationship(back_populates="company")
    leads: Mapped[List["Lead"]] = relationship(back_populates="company")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_by: Mapped[int] = mapped_column(Integer)
    updated_by: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    responsible_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(Integer)
    entity_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    entity_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    duration: Mapped[int] = mapped_column(Integer)
    is_completed: Mapped[bool] = mapped_column(Boolean)
    task_type_id: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    complete_till: Mapped[datetime] = mapped_column(DateTime)
    account_id: Mapped[int] = mapped_column(Integer)

    # Relationships
    responsible_user: Mapped["User"] = relationship(back_populates="tasks")
    lead: Mapped[Optional["Lead"]] = relationship(
        "Lead",
        primaryjoin="and_(Task.entity_type=='leads', foreign(Task.entity_id)==Lead.id)",
        viewonly=True
    )
    contact: Mapped[Optional["Contact"]] = relationship(
        "Contact",
        primaryjoin="and_(Task.entity_type=='contacts', foreign(Task.entity_id)==Contact.id)",
        viewonly=True
    )


class Event(Base):
    __tablename__ = "events"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    type: Mapped[str] = mapped_column(String(255))
    entity_id: Mapped[int] = mapped_column(Integer, nullable=True)
    entity_type: Mapped[str] = mapped_column(String(50))
    created_by: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    account_id: Mapped[int] = mapped_column(Integer)
    value_after_field_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    value_after_field_type: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    value_after_enum_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    value_after_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    value_before_field_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    value_before_field_type: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    value_before_enum_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    value_before_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    lead: Mapped[Optional["Lead"]] = relationship(
        "Lead",
        primaryjoin="and_(Event.entity_type=='leads', foreign(Event.entity_id)==Lead.id)",
        viewonly=True
    )
    
    contact: Mapped[Optional["Contact"]] = relationship(
        "Contact",
        primaryjoin="and_(Event.entity_type=='contacts', foreign(Event.entity_id)==Contact.id)",
        viewonly=True
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    lang: Mapped[str] = mapped_column(String(10))

    # Relationships
    contacts: Mapped[List["Contact"]] = relationship(back_populates="responsible_user")
    companies: Mapped[List["Company"]] = relationship(back_populates="responsible_user")
    leads: Mapped[List["Lead"]] = relationship(back_populates="responsible_user")
    tasks: Mapped[List["Task"]] = relationship(back_populates="responsible_user")


class Pipeline(Base):
    __tablename__ = "pipelines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    sort: Mapped[int] = mapped_column(Integer)
    is_main: Mapped[bool] = mapped_column(Boolean)
    is_unsorted_on: Mapped[bool] = mapped_column(Boolean)
    is_archive: Mapped[bool] = mapped_column(Boolean)
    account_id: Mapped[int] = mapped_column(Integer)

    # Relationships
    statuses: Mapped[List["Status"]] = relationship(
        back_populates="pipeline", cascade="all, delete-orphan"
    )
    leads: Mapped[List["Lead"]] = relationship(back_populates="pipeline")


class Status(Base):
    __tablename__ = "statuses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    sort: Mapped[int] = mapped_column(Integer)
    is_editable: Mapped[bool] = mapped_column(Boolean)
    pipeline_id: Mapped[int] = mapped_column(ForeignKey("pipelines.id"))
    color: Mapped[str] = mapped_column(String(50))
    type: Mapped[int] = mapped_column(Integer)
    account_id: Mapped[int] = mapped_column(Integer)

    # Relationships
    pipeline: Mapped["Pipeline"] = relationship(back_populates="statuses")
    leads: Mapped[List["Lead"]] = relationship(back_populates="status")