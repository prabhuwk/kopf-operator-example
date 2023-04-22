import os
import kopf
import debugpy
import logging
from src.user_info import process_record, delete_record


if os.environ.get("DEBUG", "False") == "True":
    debugpy.listen(("0.0.0.0", 5678))
    logging.debug("Waiting for debugger attach")
    debugpy.wait_for_client()
    debugpy.breakpoint()  # must have


def get_resource_name(**kwargs):
    namespace = kwargs["body"]["metadata"]["namespace"]
    name = kwargs["body"]["metadata"]["name"]
    return f"{namespace}_{name}"


@kopf.on.create("example.io", "v1alpha1", "updatedbs")
def create_fn(spec, **kwargs):
    resource_name = get_resource_name(**kwargs)
    logging.info(f"creating database entry for {resource_name}")
    process_record(resource_name, spec)
    return f"successfully added database entry for {resource_name}."


@kopf.on.delete("example.io", "v1alpha1", "updatedbs")
def delete_fn(**kwargs):
    resource_name = get_resource_name(**kwargs)
    logging.warn(f"deleting database entry of {resource_name}")
    delete_record(resource_name)
    return f"successfully deleted database entry for {resource_name}."
