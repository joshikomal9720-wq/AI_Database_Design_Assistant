from src.nlp_processor import NLPProcessor
from src.entity_extractor import EntityExtractor
from src.attribute_extractor import AttributeExtractor
from src.relationship_extractor import RelationshipExtractor
from src.foreign_key_generator import ForeignKeyGenerator
from src.schema_generator import SchemaGenerator
from src.database_manager import DatabaseManager
from src.normalization_analyzer import NormalizationAnalyzer
from src.optimization_analyzer import OptimizationAnalyzer
from src.sqlalchemy_schema import SQLAlchemySchemaBuilder
from src.database_diagram import DatabaseDiagramGenerator


def print_section(title):
    """Print a formatted section heading."""

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():

    requirement = """
    We need an e-commerce system with customers, products,
    categories, orders, and payments.

    Each customer has a name, email, phone, and address.
    Each category has a name.
    Each product has a name, description, price, and quantity.
    Each order has an order date, total amount, and status.
    Each payment has a payment date and amount.

    Customers can place multiple orders.
    Each order contains products and has a payment.
    Products belong to categories.
    """

    print("=" * 70)
    print("AI DATABASE DESIGN ASSISTANT")
    print("=" * 70)

    # =========================================================
    # ORIGINAL REQUIREMENT
    # =========================================================

    print_section("ORIGINAL REQUIREMENT")
    print(requirement)

    # =========================================================
    # NLP PROCESSING
    # =========================================================

    processor = NLPProcessor()

    processed_tokens = processor.preprocess_text(
        requirement
    )

    print_section("PROCESSED TOKENS")
    print(processed_tokens)

    # =========================================================
    # ENTITY EXTRACTION
    # =========================================================

    entity_extractor = EntityExtractor()

    entities = entity_extractor.extract_entities(
        requirement
    )

    print_section("EXTRACTED ENTITIES")

    if entities:

        for entity in entities:
            print(f"- {entity}")

    else:

        print("- No entities detected.")

    # =========================================================
    # ATTRIBUTE EXTRACTION
    # =========================================================

    attribute_extractor = AttributeExtractor()

    attributes_by_entity = {}

    for entity in entities:

        attributes = (
            attribute_extractor.extract_attributes(
                requirement,
                entity
            )
        )

        attributes_by_entity[entity] = attributes

    print_section("EXTRACTED ATTRIBUTES")

    for entity, attributes in (
        attributes_by_entity.items()
    ):

        print(f"\n{entity}:")

        if attributes:

            for attribute in attributes:
                print(f"- {attribute}")

        else:

            print("- No attributes detected.")

    # =========================================================
    # RELATIONSHIP EXTRACTION
    # =========================================================

    relationship_extractor = (
        RelationshipExtractor()
    )

    relationships = (
        relationship_extractor.extract_relationships(
            requirement,
            entities
        )
    )

    print_section("EXTRACTED RELATIONSHIPS")

    if relationships:

        for relationship in relationships:

            print(
                f"- {relationship['from']} "
                f"→ {relationship['to']} "
                f"({relationship['type']})"
            )

    else:

        print("- No relationships detected.")

    # =========================================================
    # FOREIGN KEY GENERATION
    # =========================================================

    foreign_key_generator = (
        ForeignKeyGenerator()
    )

    foreign_keys = (
        foreign_key_generator.generate_foreign_keys(
            relationships
        )
    )

    print_section("GENERATED FOREIGN KEYS")

    if foreign_keys:

        for foreign_key in foreign_keys:

            print(
                f"- Table: "
                f"{foreign_key['table']} | "
                f"Column: "
                f"{foreign_key['column']} | "
                f"References: "
                f"{foreign_key['references']}"
            )

    else:

        print("- No foreign keys generated.")

    # =========================================================
    # MANY-TO-MANY TABLE GENERATION
    # =========================================================

    many_to_many_tables = []

    for relationship in relationships:

        if relationship["type"] == "Many-to-Many":

            entity1 = relationship["from"]
            entity2 = relationship["to"]

            entity1_name = entity1.rstrip("s")
            entity2_name = entity2.rstrip("s")

            junction_table = (
                f"{entity1_name}_{entity2_name}s"
            )

            if (
                entity1_name == "order"
                and entity2_name == "product"
            ):

                junction_table = "order_items"

            many_to_many_tables.append(
                {
                    "table": junction_table,
                    "entity1": entity1,
                    "entity2": entity2
                }
            )

    print_section("MANY-TO-MANY TABLES")

    if many_to_many_tables:

        for junction in many_to_many_tables:

            print(
                f"- {junction['table']} "
                f"(junction table)"
            )

            print(
                f"  Connects "
                f"{junction['entity1']} "
                f"and "
                f"{junction['entity2']}"
            )

            print(
                "  Includes quantity and price"
            )

    else:

        print("- No Many-to-Many tables detected.")

    # =========================================================
    # NORMALIZATION ANALYSIS
    # =========================================================

    normalization_analyzer = (
        NormalizationAnalyzer()
    )

    normalization_analysis = (
        normalization_analyzer.analyze(
            entities,
            attributes_by_entity,
            relationships
        )
    )

    normalization_analyzer.display_results(
        normalization_analysis
    )

    # =========================================================
    # OPTIMIZATION ANALYSIS
    # =========================================================

    optimization_analyzer = (
        OptimizationAnalyzer()
    )

    optimization_analysis = (
        optimization_analyzer.analyze(
            foreign_keys,
            many_to_many_tables
        )
    )

    optimization_analyzer.display_results(
        optimization_analysis
    )

    # =========================================================
    # SQL SCHEMA GENERATION
    # =========================================================

    schema_generator = SchemaGenerator()

    schema = schema_generator.generate_schema(
        entities=entities,
        attributes_by_entity=attributes_by_entity,
        foreign_keys=foreign_keys,
        many_to_many_tables=many_to_many_tables
    )

    print_section("GENERATED DATABASE SCHEMA")

    print(schema)

    # =========================================================
    # SQLALCHEMY SCHEMA REPRESENTATION
    # =========================================================

    sqlalchemy_builder = (
        SQLAlchemySchemaBuilder()
    )

    sqlalchemy_schema_definition = [

        # -----------------------------------------------------
        # CATEGORIES
        # -----------------------------------------------------

        {
            "table": "categories",

            "columns": [

                {
                    "name": "id",
                    "type": "INTEGER",
                    "primary_key": True,
                    "nullable": False
                },

                {
                    "name": "name",
                    "type": "VARCHAR(100)"
                }
            ]
        },

        # -----------------------------------------------------
        # CUSTOMERS
        # -----------------------------------------------------

        {
            "table": "customers",

            "columns": [

                {
                    "name": "id",
                    "type": "INTEGER",
                    "primary_key": True,
                    "nullable": False
                },

                {
                    "name": "name",
                    "type": "VARCHAR(100)"
                },

                {
                    "name": "email",
                    "type": "VARCHAR(255)"
                },

                {
                    "name": "phone",
                    "type": "VARCHAR(20)"
                },

                {
                    "name": "address",
                    "type": "VARCHAR(255)"
                }
            ]
        },

        # -----------------------------------------------------
        # PRODUCTS
        # -----------------------------------------------------

        {
            "table": "products",

            "columns": [

                {
                    "name": "id",
                    "type": "INTEGER",
                    "primary_key": True,
                    "nullable": False
                },

                {
                    "name": "name",
                    "type": "VARCHAR(100)"
                },

                {
                    "name": "description",
                    "type": "TEXT"
                },

                {
                    "name": "price",
                    "type": "DECIMAL(10,2)"
                },

                {
                    "name": "quantity",
                    "type": "INTEGER"
                },

                {
                    "name": "category_id",
                    "type": "INTEGER"
                }
            ],

            "foreign_keys": [

                {
                    "column": "category_id",
                    "references": "categories.id"
                }
            ]
        },

        # -----------------------------------------------------
        # ORDERS
        # -----------------------------------------------------

        {
            "table": "orders",

            "columns": [

                {
                    "name": "id",
                    "type": "INTEGER",
                    "primary_key": True,
                    "nullable": False
                },

                {
                    "name": "order_date",
                    "type": "DATE"
                },

                {
                    "name": "total_amount",
                    "type": "DECIMAL(10,2)"
                },

                {
                    "name": "status",
                    "type": "VARCHAR(50)"
                },

                {
                    "name": "customer_id",
                    "type": "INTEGER"
                }
            ],

            "foreign_keys": [

                {
                    "column": "customer_id",
                    "references": "customers.id"
                }
            ]
        },

        # -----------------------------------------------------
        # PAYMENTS
        # -----------------------------------------------------

        {
            "table": "payments",

            "columns": [

                {
                    "name": "id",
                    "type": "INTEGER",
                    "primary_key": True,
                    "nullable": False
                },

                {
                    "name": "payment_date",
                    "type": "DATE"
                },

                {
                    "name": "amount",
                    "type": "DECIMAL(10,2)"
                },

                {
                    "name": "order_id",
                    "type": "INTEGER"
                }
            ],

            "foreign_keys": [

                {
                    "column": "order_id",
                    "references": "orders.id"
                }
            ]
        },

        # -----------------------------------------------------
        # ORDER ITEMS
        # -----------------------------------------------------

        {
            "table": "order_items",

            "columns": [

                {
                    "name": "id",
                    "type": "INTEGER",
                    "primary_key": True,
                    "nullable": False
                },

                {
                    "name": "order_id",
                    "type": "INTEGER",
                    "nullable": False
                },

                {
                    "name": "product_id",
                    "type": "INTEGER",
                    "nullable": False
                },

                {
                    "name": "quantity",
                    "type": "INTEGER"
                },

                {
                    "name": "price",
                    "type": "DECIMAL(10,2)"
                }
            ],

            "foreign_keys": [

                {
                    "column": "order_id",
                    "references": "orders.id"
                },

                {
                    "column": "product_id",
                    "references": "products.id"
                }
            ],

            "unique_constraints": [

                [
                    "order_id",
                    "product_id"
                ]
            ]
        }
    ]

    sqlalchemy_builder.build_schema(
        sqlalchemy_schema_definition
    )

    sqlalchemy_builder.display_schema()

    # =========================================================
    # DATABASE CREATION
    # =========================================================

    database_manager = DatabaseManager()

    # Reset the existing database so that the
    # current generated schema is always applied.
    database_manager.reset_database()

    database_manager.execute_schema(
        schema
    )

    # =========================================================
    # INDEX CREATION
    # =========================================================

    database_manager.create_indexes(
        optimization_analysis["indexes"]
    )

    # =========================================================
    # DATABASE INSPECTION
    # =========================================================

    print_section("DATABASE TABLES")

    database_manager.show_tables()

    database_manager.show_table_structure()

    database_manager.show_foreign_keys()

    database_manager.show_indexes()

    # =========================================================
    # DATABASE VALIDATION
    # =========================================================

    database_manager.validate_database()

    # =========================================================
    # DATABASE / ER DIAGRAM
    # =========================================================

    diagram_generator = (
        DatabaseDiagramGenerator()
    )

    diagram_generator.display_diagram()

    # =========================================================
    # COMPLETION
    # =========================================================

    print_section(
        "DATABASE GENERATION COMPLETED SUCCESSFULLY"
    )


if __name__ == "__main__":

    main()