import logging
from datetime import datetime
from contextlib import contextmanager
from httpx import Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.kommo.auth import TokenManager
from app.kommo.leads import LeadManager
from app.kommo.contacts import ContactManager
from app.kommo.companies import CompanyManager
from app.kommo.users import UserManager
from app.kommo.tasks import TaskManager
from app.kommo.events import EventManager
from app.kommo.pipelines import PipelineManager
from app.config import settings
from app.entities import Lead as LeadEntity

from app.db.repositories import (
    UserRepository,
    PipelineRepository,
    StatusRepository,
    LeadRepository,
    ContactRepository,
    CompanyRepository,
    TaskRepository,
    EventRepository,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


def process_in_batches(items, batch_size=100):
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]


def export_users(user_manager: UserManager):
    users = list(user_manager.get_all_users())
    logger.info(f"Got {len(users)} users from CRM")

    for batch in process_in_batches(users):
        with get_session() as session:
            user_repo = UserRepository(session)
            user_repo.save_or_update_all(batch)

    logger.info(f"Exported {len(users)} users")
    return users


def export_pipelines(pipeline_manager: PipelineManager):
    pipelines = list(pipeline_manager.get_all_pipelines())
    logger.info(f"Got {len(pipelines)} pipelines from CRM")

    all_statuses = []
    for pipeline in pipelines:
        all_statuses.extend(pipeline.statuses)

    for batch in process_in_batches(pipelines):
        with get_session() as session:
            pipeline_repo = PipelineRepository(session)
            pipeline_repo.save_or_update_all(batch)

    for batch in process_in_batches(all_statuses):
        with get_session() as session:
            status_repo = StatusRepository(session)
            status_repo.save_or_update_all(batch)

    logger.info(f"Exported {len(pipelines)} pipelines and {len(all_statuses)} statuses")
    return pipelines


def export_companies(company_manager: CompanyManager):
    companies = list(company_manager.get_all_companies())
    logger.info(f"Got {len(companies)} companies from CRM")

    for batch in process_in_batches(companies):
        with get_session() as session:
            company_repo = CompanyRepository(session)
            company_repo.save_or_update_all(batch)

    logger.info(f"Exported {len(companies)} companies")
    return companies


def export_contacts(contact_manager: ContactManager):
    contacts = list(contact_manager.get_all_contacts())
    logger.info(f"Got {len(contacts)} contacts from CRM")

    for batch in process_in_batches(contacts):
        with get_session() as session:
            contact_repo = ContactRepository(session)
            contact_repo.save_or_update_all(batch)

    logger.info(f"Exported {len(contacts)} contacts")
    return contacts


def export_leads(lead_manager: LeadManager):
    leads = list(lead_manager.get_all_leads())
    logger.info(f"Got {len(leads)} leads from CRM")

    for batch in process_in_batches(leads):
        with get_session() as session:
            lead_repo = LeadRepository(session)
            lead_repo.save_or_update_all(batch)

    logger.info(f"Exported {len(leads)} leads")
    return leads


def export_tasks(task_manager: TaskManager, leads: list[LeadEntity]):
    tasks = list(task_manager.get_all_tasks())
    logger.info(f"Got {len(tasks)} tasks from CRM")

    # Создаем множество ID лидов для быстрой проверки
    lead_ids = {lead.id for lead in leads}

    # Фильтруем и корректируем задачи
    filtered_tasks = []
    for task in tasks:
        # Если задача привязана к лиду, проверяем его наличие
        if task.entity_type == 'leads' and task.entity_id not in lead_ids:
            # Если лида нет в списке, обнуляем entity_id
            task.entity_id = None
        
        filtered_tasks.append(task)

    for batch in process_in_batches(filtered_tasks):
        with get_session() as session:
            task_repo = TaskRepository(session)
            task_repo.save_or_update_all(batch)

    logger.info(f"Exported {len(filtered_tasks)} tasks")
    return filtered_tasks


def export_events(event_manager: EventManager, leads: list[LeadEntity]):
    all_events = []
    
    # Создаем множество ID лидов для быстрой проверки
    lead_ids = {lead.id for lead in leads}

    for lead in leads:
        events = list(event_manager.get_all_lead_events(lead_id=lead.id))
        
        # Фильтруем и корректируем события
        filtered_events = []
        for event in events:
            # Если событие привязано к лиду, проверяем его наличие
            if event.entity_type == 'leads' and event.entity_id not in lead_ids:
                # Если лида нет в списке, обнуляем entity_id
                event.entity_id = None
            
            filtered_events.append(event)

        all_events.extend(filtered_events)

        for batch in process_in_batches(filtered_events, batch_size=50):
            with get_session() as session:
                event_repo = EventRepository(session)
                event_repo.save_or_update_all(batch)

        logger.info(f"Exported {len(filtered_events)} events for lead {lead.id}")

    logger.info(f"Exported total {len(all_events)} events")
    return all_events


def export_data():
    start_time = datetime.now()
    logger.info(f"Starting data export at {start_time}")

    http_client = Client(base_url=f"https://{settings.KOMMO_URL_BASE}.kommo.com/")
    token_manager = TokenManager(http_client)

    try:
        users = export_users(UserManager(token_manager, http_client))
        pipelines = export_pipelines(PipelineManager(token_manager, http_client))
        companies = export_companies(CompanyManager(token_manager, http_client))
        contacts = export_contacts(ContactManager(token_manager, http_client))
        leads = export_leads(LeadManager(token_manager, http_client))
        tasks = export_tasks(TaskManager(token_manager, http_client), leads)
        events = export_events(EventManager(token_manager, http_client), leads)

        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"Export completed at {end_time}. Duration: {duration}")

    except Exception as e:
        logger.error(f"Error during export: {str(e)}")
        raise
    finally:
        http_client.close()


if __name__ == "__main__":
    export_data()
