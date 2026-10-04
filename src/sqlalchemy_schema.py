from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Text,
    Date,
    Numeric,
    ForeignKey,
    UniqueConstraint
)


class SQLAlchemySchemaBuilder:
    """
    Builds a SQLAlchemy representation of the generated
    database schema.
    """

    def __init__(self):
        self.metadata = MetaData()

    # =========================================================
    # DATA TYPE MAPPING
    # =========================================================

    def get_column_type(self, data_type):
        """Convert generated SQL types to SQLAlchemy types."""

        data_type = data_type.upper()

        if data_type.startswith("INTEGER"):
            return Integer

        if data_type.startswith("VARCHAR"):

            if "(" in data_type:

                size = int(
                    data_type.split("(")[1]
                    .split(")")[0]
                )

                return String(size)

            return String

        if data_type.startswith("TEXT"):
            return Text

        if data_type.startswith("DATE"):
            return Date

        if data_type.startswith("DECIMAL"):

            return Numeric(
                precision=10,
                scale=2
            )

        return String(255)

    # =========================================================
    # BUILD TABLE
    # =========================================================

    def add_table(
        self,
        table_name,
        columns,
        foreign_keys=None,
        unique_constraints=None
    ):
        """
        Add a table to the SQLAlchemy metadata.
        """

        foreign_keys = foreign_keys or []
        unique_constraints = unique_constraints or []

        sqlalchemy_columns = []

        for column in columns:

            column_name = column["name"]
            data_type = column["type"]

            is_primary_key = column.get(
                "primary_key",
                False
            )

            is_nullable = column.get(
                "nullable",
                True
            )

            sqlalchemy_type = (
                self.get_column_type(
                    data_type
                )
            )

            foreign_key = None

            for fk in foreign_keys:

                if fk["column"] == column_name:

                    foreign_key = ForeignKey(
                        fk["references"]
                    )

                    break

            if foreign_key:

                sqlalchemy_column = Column(
                    column_name,
                    sqlalchemy_type,
                    foreign_key,
                    primary_key=is_primary_key,
                    nullable=is_nullable
                )

            else:

                sqlalchemy_column = Column(
                    column_name,
                    sqlalchemy_type,
                    primary_key=is_primary_key,
                    nullable=is_nullable
                )

            sqlalchemy_columns.append(
                sqlalchemy_column
            )

        constraints = []

        for unique_constraint in unique_constraints:

            constraints.append(
                UniqueConstraint(
                    *unique_constraint
                )
            )

        Table(
            table_name,
            self.metadata,
            *sqlalchemy_columns,
            *constraints
        )

    # =========================================================
    # BUILD COMPLETE SCHEMA
    # =========================================================

    def build_schema(self, schema_definition):
        """
        Build all tables from a structured schema definition.
        """

        self.metadata.clear()

        for table in schema_definition:

            self.add_table(
                table_name=table["table"],
                columns=table["columns"],
                foreign_keys=table.get(
                    "foreign_keys",
                    []
                ),
                unique_constraints=table.get(
                    "unique_constraints",
                    []
                )
            )

        return self.metadata

    # =========================================================
    # DISPLAY SCHEMA
    # =========================================================

    def display_schema(self):
        """Display the SQLAlchemy schema structure."""

        print("\n" + "=" * 70)
        print("SQLALCHEMY SCHEMA REPRESENTATION")
        print("=" * 70)

        for table in self.metadata.sorted_tables:

            print(
                f"\nTable: {table.name}"
            )

            print(
                "-" * 70
            )

            for column in table.columns:

                primary_key = ""

                if column.primary_key:
                    primary_key = " PRIMARY KEY"

                nullable = ""

                if not column.nullable:
                    nullable = " NOT NULL"

                print(
                    f"  {column.name:<20}"
                    f"{str(column.type):<18}"
                    f"{primary_key}"
                    f"{nullable}"
                )

            for constraint in table.constraints:

                if isinstance(
                    constraint,
                    UniqueConstraint
                ):

                    columns = ", ".join(
                        column.name
                        for column in constraint.columns
                    )

                    print(
                        f"  UNIQUE ({columns})"
                    )

    # =========================================================
    # GENERATE SQL USING SQLALCHEMY
    # =========================================================

    def generate_sql(
        self,
        database_url="sqlite:///:memory:"
    ):
        """
        Generate SQL-compatible schema through SQLAlchemy.
        """

        engine = create_engine(
            database_url
        )

        from sqlalchemy.schema import CreateTable

        statements = []

        for table in self.metadata.sorted_tables:

            statements.append(
                str(
                    CreateTable(table).compile(
                        engine
                    )
                )
                + ";"
            )

        return "\n\n".join(
            statements
        )


# =============================================================
# TEST SQLALCHEMY SCHEMA BUILDER
# =============================================================

if __name__ == "__main__":

    schema_definition = [

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

    # =========================================================
    # BUILD SQLALCHEMY SCHEMA
    # =========================================================

    builder = SQLAlchemySchemaBuilder()

    builder.build_schema(
        schema_definition
    )

    # =========================================================
    # DISPLAY SQLALCHEMY STRUCTURE
    # =========================================================

    builder.display_schema()

    # =========================================================
    # GENERATE SQL
    # =========================================================

    print("\n" + "=" * 70)
    print("SQLALCHEMY GENERATED SQL")
    print("=" * 70)

    print(
        builder.generate_sql()
    )