from datetime import datetime
from typing import List, TypeVar, Generic, Type

from sqlalchemy.orm import Session

from app.db.models import User, Pipeline, Status, Lead, Contact, Company, Task, Event
from app.entities import User as UserEntity
from app.entities import Pipeline as PipelineEntity
from app.entities import Status as StatusEntity
from app.entities import Lead as LeadEntity
from app.entities import Contact as ContactEntity
from app.entities import Company as CompanyEntity
from app.entities import Task as TaskEntity
from app.entities import Event as EventEntity

T = TypeVar("T")
E = TypeVar("E")


class BaseRepository(Generic[T, E]):
    def __init__(self, session: Session, model: Type[T]):
        self._session = session
        self._model = model

    def save_or_update(self, entity: E) -> T:
        db_entity = self._convert_to_db_model(entity)
        merged = self._session.merge(db_entity)
        self._session.commit()
        return merged

    def save_or_update_all(self, entities: List[E]) -> List[T]:
        db_entities = [self._convert_to_db_model(entity) for entity in entities]
        merged = [self._session.merge(entity) for entity in db_entities]
        self._session.commit()
        return merged

    def get_by_id(self, id: int) -> T | None:
        return self._session.get(self._model, id)

    def _convert_to_db_model(self, entity: E) -> T:
        raise NotImplementedError


class UserRepository(BaseRepository[User, UserEntity]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def _convert_to_db_model(self, entity: UserEntity) -> User:
        return User(
            id=entity.id, name=entity.name, email=entity.email, lang=entity.lang
        )


class PipelineRepository(BaseRepository[Pipeline, PipelineEntity]):
    def __init__(self, session: Session):
        super().__init__(session, Pipeline)

    def _convert_to_db_model(self, entity: PipelineEntity) -> Pipeline:
        return Pipeline(
            id=entity.id,
            name=entity.name,
            sort=entity.sort,
            is_main=entity.is_main,
            is_unsorted_on=entity.is_unsorted_on,
            is_archive=entity.is_archive,
            account_id=entity.account_id,
        )


class StatusRepository(BaseRepository[Status, StatusEntity]):
    def __init__(self, session: Session):
        super().__init__(session, Status)

    def _convert_to_db_model(self, entity: StatusEntity) -> Status:
        return Status(
            id=entity.id,
            name=entity.name,
            sort=entity.sort,
            is_editable=entity.is_editable,
            pipeline_id=entity.pipeline_id,
            color=entity.color,
            type=entity.type,
            account_id=entity.account_id,
        )


class LeadRepository(BaseRepository[Lead, LeadEntity]):
    def __init__(self, session: Session):
        super().__init__(session, Lead)

    def _convert_to_db_model(self, entity: LeadEntity) -> Lead:
        return Lead(
            id=entity.id,
            name=entity.name,
            price=entity.price,
            responsible_user_id=entity.responsible_user_id,
            group_id=entity.group_id,
            status_id=entity.status_id,
            pipeline_id=entity.pipeline_id,
            loss_reason_id=entity.loss_reason_id,
            created_by=entity.created_by,
            updated_by=entity.updated_by,
            created_at=datetime.fromtimestamp(entity.created_at),
            updated_at=datetime.fromtimestamp(entity.updated_at),
            closed_at=(
                datetime.fromtimestamp(entity.closed_at) if entity.closed_at else None
            ),
            closest_task_at=(
                datetime.fromtimestamp(entity.closest_task_at)
                if entity.closest_task_at
                else None
            ),
            is_deleted=entity.is_deleted,
            score=entity.score,
            account_id=entity.account_id,
            labor_cost=entity.labor_cost,
            source=entity.source,
            payment_type=entity.payment_type,
            readiness_to_buy=entity.readiness_to_buy,
            object_type=entity.object_type,
            purchase_purpose=entity.purchase_purpose,
            meeting_format=entity.meeting_format,
            meeting_scheduled_datetime=(
                datetime.fromtimestamp(entity.meeting_scheduled_datetime)
                if entity.meeting_scheduled_datetime
                else None
            ),
            zoom_link=entity.zoom_link,
            deposit_date=(
                datetime.fromtimestamp(entity.deposit_date)
                if entity.deposit_date
                else None
            ),
            meeting_conducted_date=(
                datetime.fromtimestamp(entity.meeting_conducted_date)
                if entity.meeting_conducted_date
                else None
            ),
            deal_date=(
                datetime.fromtimestamp(entity.deal_date) if entity.deal_date else None
            ),
            payment_method=entity.payment_method,
            down_payment_percent=entity.down_payment_percent,
            apartment_number=entity.apartment_number,
            apartment_cost=entity.apartment_cost,
            apartment_status=entity.apartment_status,
            comment=entity.comment,
            referrer=entity.referrer,
            tag_name=entity.tag_name,
            tag_id=entity.tag_id,
            company_id=entity.company_id,
            contact_id=entity.contact_id,
        )


class ContactRepository(BaseRepository[Contact, ContactEntity]):
    def __init__(self, session: Session):
        super().__init__(session, Contact)

    def _convert_to_db_model(self, entity: ContactEntity) -> Contact:
        return Contact(
            id=entity.id,
            name=entity.name,
            first_name=entity.first_name,
            last_name=entity.last_name,
            responsible_user_id=entity.responsible_user_id,
            group_id=entity.group_id,
            created_by=entity.created_by,
            updated_by=entity.updated_by,
            created_at=datetime.fromtimestamp(entity.created_at),
            updated_at=datetime.fromtimestamp(entity.updated_at),
            closest_task_at=(
                datetime.fromtimestamp(entity.closest_task_at)
                if entity.closest_task_at
                else None
            ),
            is_deleted=entity.is_deleted,
            is_unsorted=entity.is_unsorted,
            account_id=entity.account_id,
            phone=entity.phone,
            email=entity.email,
            position=entity.position,
            company_name=entity.company_name,
            company_id=entity.company_id,
            tag_id=entity.tag_id,
            tag_name=entity.tag_name,
            apartment=entity.apartment,
            was_in_bali=entity.was_in_bali,
            geography=entity.geography,
            language=entity.language,
        )


class CompanyRepository(BaseRepository[Company, CompanyEntity]):
    def __init__(self, session: Session):
        super().__init__(session, Company)

    def _convert_to_db_model(self, entity: CompanyEntity) -> Company:
        return Company(
            id=entity.id,
            name=entity.name,
            responsible_user_id=entity.responsible_user_id,
            group_id=entity.group_id,
            created_by=entity.created_by,
            updated_by=entity.updated_by,
            created_at=datetime.fromtimestamp(entity.created_at),
            updated_at=datetime.fromtimestamp(entity.updated_at),
            account_id=entity.account_id,
            closest_task_at=(
                datetime.fromtimestamp(entity.closest_task_at)
                if entity.closest_task_at
                else None
            ),
            is_deleted=entity.is_deleted,
            tag_id=entity.tag_id,
            tag_name=entity.tag_name,
            phone=entity.phone,
            broker=entity.broker,
        )


class TaskRepository(BaseRepository[Task, TaskEntity]):
    def __init__(self, session: Session):
        super().__init__(session, Task)

    def _convert_to_db_model(self, entity: TaskEntity) -> Task:
        # Проверяем существование сущности, если entity_id указан
        entity_id = None
        if entity.entity_id:
            # Проверяем, существует ли сущность в базе данных
            if entity.entity_type == 'leads':
                existing_lead = self._session.get(Lead, entity.entity_id)
                entity_id = existing_lead.id if existing_lead else None
            elif entity.entity_type == 'contacts':
                existing_contact = self._session.get(Contact, entity.entity_id)
                entity_id = existing_contact.id if existing_contact else None

        return Task(
            id=entity.id,
            created_by=entity.created_by,
            updated_by=entity.updated_by,
            created_at=datetime.fromtimestamp(entity.created_at),
            updated_at=datetime.fromtimestamp(entity.updated_at),
            responsible_user_id=entity.responsible_user_id,
            group_id=entity.group_id,
            entity_id=entity_id,  # Используем проверенный entity_id
            entity_type=entity.entity_type,
            duration=entity.duration,
            is_completed=entity.is_completed,
            task_type_id=entity.task_type_id,
            text=entity.text,
            result=str(entity.result) if entity.result else None,
            complete_till=datetime.fromtimestamp(entity.complete_till),
            account_id=entity.account_id,
        )


class EventRepository(BaseRepository[Event, EventEntity]):
    def __init__(self, session: Session):
        super().__init__(session, Event)

    def _convert_to_db_model(self, entity: EventEntity) -> Event:
        return Event(
            id=entity.id,
            type=entity.type,
            entity_id=entity.entity_id,
            entity_type=entity.entity_type,
            created_by=entity.created_by,
            created_at=datetime.fromtimestamp(entity.created_at),
            account_id=entity.account_id,
            value_after_field_id=entity.value_after_field_id,
            value_after_field_type=entity.value_after_field_type,
            value_after_enum_id=entity.value_after_enum_id,
            value_after_text=entity.value_after_text,
            value_before_field_id=entity.value_before_field_id,
            value_before_field_type=entity.value_before_field_type,
            value_before_enum_id=entity.value_before_enum_id,
            value_before_text=entity.value_before_text,
        )
