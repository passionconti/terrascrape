from terrascrape.core.builder import Builder
from terrascrape.db.models.builder import Builder as DB_Builder
from terrascrape.db.services.component import ComponentService


class BuilderService(ComponentService):
    def __init__(self):
        super().__init__(DB_Builder)

    def _map_component_to_db_model(self, builder: Builder) -> DB_Builder:
        return DB_Builder(
            name=builder.name,
            package_name=builder.package_name,
            class_name=builder.class_name,
            description=builder.description,
            contents_schema=builder.contents_model.schema(),
        )
