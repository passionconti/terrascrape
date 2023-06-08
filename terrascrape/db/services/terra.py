from terrascrape.core.terra import Terra
from terrascrape.db.models.terra import Terra as DB_Terra
from terrascrape.db.services.component import ComponentService


class TerraService(ComponentService):
    def __init__(self):
        super().__init__(DB_Terra)

    def _map_component_to_db_model(self, terra: Terra) -> DB_Terra:
        return DB_Terra(
            name=terra.name,
            package_name=terra.package_name,
            class_name=terra.class_name,
            parameters_schema=terra.parameters_model.schema(),
            description=terra.description,
        )
