import logging
from src.models import (
    create_database_engine,
    get_record_by_resource_name,
    add_database_record,
    delete_database_record,
)


engine = create_database_engine()


def process_record(resource_name, spec):

    record = {"resource_name": resource_name}
    for key, value in spec.items():
        record[key] = value

    record_exists = get_record_by_resource_name(
        engine=engine, resource_name=resource_name
    )
    if record_exists:
        logging.info(f"database entry already exists for {resource_name}")

    add_database_record(engine, record)


def delete_record(resource_name):
    delete_database_record(engine, resource_name)
