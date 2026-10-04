from src.data_type_mapper import DataTypeMapper


class SchemaGenerator:
    """
    Generates SQL database schema dynamically from
    extracted entities, attributes, foreign keys,
    and many-to-many relationships.
    """

    def __init__(self):
        self.data_type_mapper = DataTypeMapper()

    # ---------------------------------------------------------
    # TABLE NAME
    # ---------------------------------------------------------

    def table_name(self, entity):
        """
        Convert an entity name into a table name.
        """

        entity = entity.lower().strip()

        if entity.endswith("y"):
            return entity[:-1] + "ies"

        if entity.endswith("s"):
            return entity

        return entity + "s"

    # ---------------------------------------------------------
    # COLUMN NAME
    # ---------------------------------------------------------

    def column_name(self, attribute):
        """
        Convert an attribute into a SQL-friendly column name.
        """

        return (
            attribute.lower()
            .strip()
            .replace(" ", "_")
        )

    # ---------------------------------------------------------
    # GENERATE ENTITY TABLE
    # ---------------------------------------------------------

    def generate_entity_table(
        self,
        entity,
        attributes,
        foreign_keys
    ):
        """
        Generate CREATE TABLE statement for an entity.
        """

        table = self.table_name(entity)

        columns = []

        # Primary key
        columns.append(
            "id INTEGER PRIMARY KEY"
        )

        # Extracted attributes
        for attribute in attributes:

            column = self.column_name(attribute)

            data_type = self.data_type_mapper.suggest_type(
                attribute
            )

            # Avoid duplicate ID column
            if column == "id":
                continue

            columns.append(
                f"{column} {data_type}"
            )

        # Foreign keys belonging to this table
        table_foreign_keys = []

        for foreign_key in foreign_keys:

            if foreign_key["table"] == table:

                column = foreign_key["column"]
                references = foreign_key["references"]

                # Avoid duplicate FK columns
                if not any(
                    column == existing.split()[0]
                    for existing in columns
                ):
                    columns.append(
                        f"{column} INTEGER"
                    )

                table_foreign_keys.append(
                    f"FOREIGN KEY ({column}) "
                    f"REFERENCES {references}"
                )

        columns.extend(table_foreign_keys)

        sql = (
            f"CREATE TABLE IF NOT EXISTS {table} (\n"
        )

        sql += ",\n".join(
            f"    {column}"
            for column in columns
        )

        sql += "\n);"

        return sql

    # ---------------------------------------------------------
    # GENERATE MANY-TO-MANY TABLE
    # ---------------------------------------------------------

    def generate_many_to_many_table(
        self,
        junction
    ):
        """
        Generate a junction table for a many-to-many
        relationship.
        """

        table = junction["table"]

        entity1 = self.table_name(
            junction["entity1"]
        )

        entity2 = self.table_name(
            junction["entity2"]
        )

        # Special handling for order_items
        if table == "order_items":

            sql = """
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER,
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    UNIQUE (order_id, product_id)
);"""

            return sql.strip()

        # Generic junction table
        entity1_column = (
            entity1.rstrip("s") + "_id"
        )

        entity2_column = (
            entity2.rstrip("s") + "_id"
        )

        sql = f"""
CREATE TABLE IF NOT EXISTS {table} (
    id INTEGER PRIMARY KEY,
    {entity1_column} INTEGER NOT NULL,
    {entity2_column} INTEGER NOT NULL,
    FOREIGN KEY ({entity1_column})
        REFERENCES {entity1}(id),
    FOREIGN KEY ({entity2_column})
        REFERENCES {entity2}(id),
    UNIQUE ({entity1_column}, {entity2_column})
);"""

        return sql.strip()

    # ---------------------------------------------------------
    # COMPLETE SCHEMA GENERATION
    # ---------------------------------------------------------

    def generate_schema(
        self,
        entities,
        attributes_by_entity,
        foreign_keys,
        many_to_many_tables
    ):
        """
        Generate the complete SQL database schema.
        """

        statements = []

        # -----------------------------------------------------
        # Entity tables
        # -----------------------------------------------------

        for entity in entities:

            attributes = attributes_by_entity.get(
                entity,
                []
            )

            table_sql = self.generate_entity_table(
                entity,
                attributes,
                foreign_keys
            )

            statements.append(table_sql)

        # -----------------------------------------------------
        # Many-to-many tables
        # -----------------------------------------------------

        for junction in many_to_many_tables:

            junction_sql = self.generate_many_to_many_table(
                junction
            )

            statements.append(junction_sql)

        return "\n\n".join(statements)


# -------------------------------------------------------------
# TEST
# -------------------------------------------------------------

if __name__ == "__main__":

    entities = [
        "customer",
        "product",
        "category",
        "order",
        "payment"
    ]

    attributes_by_entity = {

        "customer": [
            "name",
            "email",
            "phone",
            "address"
        ],

        "product": [
            "name",
            "description",
            "price",
            "quantity"
        ],

        "category": [
            "name"
        ],

        "order": [
            "order_date",
            "total_amount",
            "status"
        ],

        "payment": [
            "payment_date",
            "amount"
        ]
    }

    foreign_keys = [

        {
            "table": "orders",
            "column": "customer_id",
            "references": "customers(id)"
        },

        {
            "table": "products",
            "column": "category_id",
            "references": "categories(id)"
        },

        {
            "table": "payments",
            "column": "order_id",
            "references": "orders(id)"
        }
    ]

    many_to_many_tables = [

        {
            "table": "order_items",
            "entity1": "orders",
            "entity2": "products"
        }
    ]

    generator = SchemaGenerator()

    schema = generator.generate_schema(
        entities=entities,
        attributes_by_entity=attributes_by_entity,
        foreign_keys=foreign_keys,
        many_to_many_tables=many_to_many_tables
    )

    print("=" * 70)
    print("GENERATED DATABASE SCHEMA")
    print("=" * 70)

    print(schema)