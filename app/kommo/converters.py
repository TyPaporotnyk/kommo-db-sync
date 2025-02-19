from app.entities import Company, Contact, Event, Lead, Pipeline, Status, Task, User


def convert_lead_json_to_entity(json_data: dict) -> Lead:
    custom_fields = {}
    if json_data.get("custom_fields_values"):
        for field in json_data["custom_fields_values"]:
            field_name = field["field_name"]
            if field["values"]:
                value = field["values"][0].get("value")
                if isinstance(value, dict):
                    continue
                custom_fields[field_name] = value

    tag = None
    tag_id = None
    if json_data.get("_embedded", {}).get("tags"):
        first_tag = (
            json_data["_embedded"]["tags"][0]
            if json_data["_embedded"]["tags"]
            else None
        )
        if first_tag:
            tag = first_tag.get("name")
            tag_id = first_tag.get("id")

    company_id = None
    if json_data.get("_embedded", {}).get("companies"):
        first_company = (
            json_data["_embedded"]["companies"][0]
            if json_data["_embedded"]["companies"]
            else None
        )
        if first_company:
            company_id = first_company.get("id")

    contact_id = None
    if json_data.get("_embedded", {}).get("contacts"):
        first_contact = (
            json_data["_embedded"]["contacts"][0]
            if json_data["_embedded"]["contacts"]
            else None
        )
        if first_contact and first_contact.get("is_main"):
            contact_id = first_contact.get("id")

    return Lead(
        id=json_data["id"],
        name=json_data["name"],
        price=json_data["price"],
        responsible_user_id=json_data["responsible_user_id"],
        group_id=json_data["group_id"],
        status_id=json_data["status_id"],
        pipeline_id=json_data["pipeline_id"],
        loss_reason_id=json_data["loss_reason_id"],
        created_by=json_data["created_by"],
        updated_by=json_data["updated_by"],
        created_at=json_data["created_at"],
        updated_at=json_data["updated_at"],
        closed_at=json_data["closed_at"],
        closest_task_at=json_data["closest_task_at"],
        is_deleted=json_data["is_deleted"],
        score=json_data["score"],
        account_id=json_data["account_id"],
        labor_cost=json_data["labor_cost"],
        source=custom_fields.get("Источник"),
        payment_type=custom_fields.get("Оплата"),
        readiness_to_buy=custom_fields.get("Готовность купить"),
        object_type=custom_fields.get("Тип объекта"),
        purchase_purpose=custom_fields.get("Цель покупки"),
        meeting_format=custom_fields.get("Формат встречи"),
        meeting_scheduled_datetime=custom_fields.get(
            "Дата и время запланированной встречи"
        ),
        zoom_link=custom_fields.get("Ссылка на зум встречу"),
        deposit_date=custom_fields.get("Дата задатка"),
        meeting_conducted_date=custom_fields.get("Дата проведённой встречи"),
        deal_date=custom_fields.get("Дата сделки"),
        payment_method=custom_fields.get("Способ оплаты"),
        down_payment_percent=(
            float(custom_fields.get("Размер ПВ, %"))
            if custom_fields.get("Размер ПВ, %")
            else None
        ),
        apartment_number=custom_fields.get("Апартамент"),
        apartment_cost=(
            float(custom_fields.get("Стоимость апартамента"))
            if custom_fields.get("Стоимость апартамента")
            else None
        ),
        apartment_status=custom_fields.get("Статус апартамента"),
        comment=custom_fields.get("Комментарий"),
        referrer=custom_fields.get("referrer"),
        tag_name=tag,
        tag_id=tag_id,
        company_id=company_id,
        contact_id=contact_id,  # Добавляем новое поле
    )


def convert_contact_json_to_entity(json_data: dict) -> Contact:
    custom_fields = {}
    custom_fields_values = json_data.get("custom_fields_values")

    if custom_fields_values:
        for field in custom_fields_values:
            field_name = field["field_name"]
            if field["values"]:
                value = field["values"][0].get("value")
                if isinstance(value, dict):
                    continue
                custom_fields[field_name] = value

            if field["field_code"] == "PHONE":
                custom_fields["phone"] = (
                    field["values"][0]["value"] if field["values"] else None
                )
            elif field["field_code"] == "EMAIL":
                custom_fields["email"] = (
                    field["values"][0]["value"] if field["values"] else None
                )

    embedded = json_data.get("_embedded", {})
    tags = embedded.get("tags", [])
    companies = embedded.get("companies", [])

    tag = tags[0] if tags else None
    company = companies[0] if companies else None

    return Contact(
        id=json_data["id"],
        name=json_data["name"],
        first_name=json_data.get("first_name"),
        last_name=json_data.get("last_name"),
        responsible_user_id=json_data["responsible_user_id"],
        group_id=json_data["group_id"],
        created_by=json_data["created_by"],
        updated_by=json_data["updated_by"],
        created_at=json_data["created_at"],
        updated_at=json_data["updated_at"],
        closest_task_at=json_data.get("closest_task_at"),
        is_deleted=json_data["is_deleted"],
        is_unsorted=json_data["is_unsorted"],
        account_id=json_data["account_id"],
        phone=custom_fields.get("phone"),
        email=custom_fields.get("email"),
        position=custom_fields.get("Position"),
        company_name=company.get("name") if company else None,
        company_id=company.get("id") if company else None,
        tag_id=tag.get("id") if tag else None,
        tag_name=tag.get("name") if tag else None,
        apartment=custom_fields.get("Апартамент"),
        was_in_bali=custom_fields.get("Был на Бали"),
        geography=custom_fields.get("География"),
        language=custom_fields.get("Язык"),
    )


def convert_company_json_to_entity(json_data: dict) -> Company:
    custom_fields = {}
    custom_fields_values = json_data.get("custom_fields_values")

    if custom_fields_values:
        for field in custom_fields_values:
            field_name = field["field_name"]
            if field["values"]:
                value = field["values"][0].get("value")
                if isinstance(value, dict):
                    continue
                custom_fields[field_name] = value

            if field["field_code"] == "PHONE":
                custom_fields["phone"] = (
                    field["values"][0]["value"] if field["values"] else None
                )

    embedded = json_data.get("_embedded", {})
    tags = embedded.get("tags", [])
    tag = tags[0] if tags else None

    return Company(
        id=json_data["id"],
        name=json_data["name"],
        responsible_user_id=json_data["responsible_user_id"],
        group_id=json_data["group_id"],
        created_by=json_data["created_by"],
        updated_by=json_data["updated_by"],
        created_at=json_data["created_at"],
        updated_at=json_data["updated_at"],
        account_id=json_data["account_id"],
        closest_task_at=json_data.get("closest_task_at"),
        is_deleted=json_data["is_deleted"],
        tag_id=tag.get("id") if tag else None,
        tag_name=tag.get("name") if tag else None,
        phone=custom_fields.get("phone"),
        broker=custom_fields.get("Брокер"),
    )


def convert_task_json_to_entity(json_data: dict) -> Task:
    return Task(
        id=json_data["id"],
        created_by=json_data["created_by"],
        updated_by=json_data["updated_by"],
        created_at=json_data["created_at"],
        updated_at=json_data["updated_at"],
        responsible_user_id=json_data["responsible_user_id"],
        group_id=json_data["group_id"],
        entity_id=json_data.get("entity_id"),
        entity_type=json_data.get("entity_type"),
        duration=json_data["duration"],
        is_completed=json_data["is_completed"],
        task_type_id=json_data["task_type_id"],
        text=json_data["text"],
        result=json_data["result"],
        complete_till=json_data["complete_till"],
        account_id=json_data["account_id"],
    )


def convert_user_json_to_entity(json_data: dict) -> User:
    return User(
        id=json_data["id"],
        name=json_data["name"],
        email=json_data["email"],
        lang=json_data["lang"],
    )


def convert_event_json_to_entity(json_data: dict) -> Event:
    value_after = json_data.get("value_after", [])
    value_before = json_data.get("value_before", [])

    # Инициализируем default значения
    value_after_data = {}
    value_before_data = {}

    # Проверяем наличие данных и получаем custom_field_value безопасно
    if value_after and isinstance(value_after[0], dict):
        value_after_data = value_after[0].get("custom_field_value", {}) or {}
    if value_before and isinstance(value_before[0], dict):
        value_before_data = value_before[0].get("custom_field_value", {}) or {}

    return Event(
        id=json_data["id"],
        type=json_data["type"],
        entity_id=json_data["entity_id"],
        entity_type=json_data["entity_type"],
        created_by=json_data["created_by"],
        created_at=json_data["created_at"],
        account_id=json_data["account_id"],
        value_after_field_id=value_after_data.get("field_id"),
        value_after_field_type=value_after_data.get("field_type"),
        value_after_enum_id=value_after_data.get("enum_id"),
        value_after_text=value_after_data.get("text"),
        value_before_field_id=value_before_data.get("field_id"),
        value_before_field_type=value_before_data.get("field_type"),
        value_before_enum_id=value_before_data.get("enum_id"),
        value_before_text=value_before_data.get("text"),
    )


def convert_status_json_to_entity(json_data: dict) -> Status:
    return Status(
        id=json_data["id"],
        name=json_data["name"],
        sort=json_data["sort"],
        is_editable=json_data["is_editable"],
        pipeline_id=json_data["pipeline_id"],
        color=json_data["color"],
        type=json_data["type"],
        account_id=json_data["account_id"],
    )


def convert_pipeline_json_to_entity(json_data: dict) -> Pipeline:
    statuses = []
    if "_embedded" in json_data and "statuses" in json_data["_embedded"]:
        statuses = [
            convert_status_json_to_entity(status)
            for status in json_data["_embedded"]["statuses"]
        ]

    return Pipeline(
        id=json_data["id"],
        name=json_data["name"],
        sort=json_data["sort"],
        is_main=json_data["is_main"],
        is_unsorted_on=json_data["is_unsorted_on"],
        is_archive=json_data["is_archive"],
        account_id=json_data["account_id"],
        statuses=statuses,
    )
