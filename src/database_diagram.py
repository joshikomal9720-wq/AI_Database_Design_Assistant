import sqlite3


class DatabaseDiagramGenerator:
    """
    Generates a text-based ER/database diagram
    from the SQLite database schema.
    """

    def __init__(self, database_name="database.db"):
        self.database_name = database_name

    # =========================================================
    # DATABASE CONNECTION
    # =========================================================

    def connect(self):
        """Create a connection to the SQLite database."""

        return sqlite3.connect(
            self.database_name
        )

    # =========================================================
    # GET TABLES
    # =========================================================

    def get_tables(self, connection):
        """Return all user-created database tables."""

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
            """
        )

        return [
            row[0]
            for row in cursor.fetchall()
        ]

    # =========================================================
    # GET COLUMNS
    # =========================================================

    def get_columns(
        self,
        connection,
        table_name
    ):
        """Return column information for a table."""

        cursor = connection.cursor()

        cursor.execute(
            f'PRAGMA table_info("{table_name}");'
        )

        columns = []

        for row in cursor.fetchall():

            columns.append(
                {
                    "name": row[1],
                    "type": row[2],
                    "primary_key": bool(row[5]),
                    "nullable": not bool(row[3])
                }
            )

        return columns

    # =========================================================
    # GET FOREIGN KEYS
    # =========================================================

    def get_foreign_keys(
        self,
        connection,
        table_name
    ):
        """Return foreign-key information for a table."""

        cursor = connection.cursor()

        cursor.execute(
            f'PRAGMA foreign_key_list("{table_name}");'
        )

        foreign_keys = []

        for row in cursor.fetchall():

            foreign_keys.append(
                {
                    "column": row[3],
                    "references_table": row[2],
                    "references_column": row[4]
                }
            )

        return foreign_keys

    # =========================================================
    # GENERATE TABLE BLOCK
    # =========================================================

    def generate_table_block(
        self,
        connection,
        table_name
    ):
        """Generate a visual block for one database table."""

        columns = self.get_columns(
            connection,
            table_name
        )

        foreign_keys = self.get_foreign_keys(
            connection,
            table_name
        )

        foreign_key_columns = {
            fk["column"]
            for fk in foreign_keys
        }

        width = 38

        lines = []

        lines.append(
            "┌" + "─" * width + "┐"
        )

        title = (
            f"│ {table_name.upper():<{width - 1}}│"
        )

        lines.append(title)

        lines.append(
            "├" + "─" * width + "┤"
        )

        for column in columns:

            prefix = "   "

            if column["primary_key"]:
                prefix = "PK "

            elif column["name"] in foreign_key_columns:
                prefix = "FK "

            column_text = (
                f"{prefix}"
                f"{column['name']} "
                f"({column['type']})"
            )

            lines.append(
                f"│ {column_text:<{width - 1}}│"
            )

        lines.append(
            "└" + "─" * width + "┘"
        )

        return "\n".join(lines)

    # =========================================================
    # GENERATE RELATIONSHIP LIST
    # =========================================================

    def generate_relationships(
        self,
        connection,
        tables
    ):
        """Generate a list of foreign-key relationships."""

        relationships = []

        for table in tables:

            foreign_keys = self.get_foreign_keys(
                connection,
                table
            )

            for foreign_key in foreign_keys:

                relationship = (
                    f"{table}.{foreign_key['column']}"
                    f" → "
                    f"{foreign_key['references_table']}."
                    f"{foreign_key['references_column']}"
                )

                relationships.append(
                    relationship
                )

        return relationships

    # =========================================================
    # DISPLAY DIAGRAM
    # =========================================================

    def display_diagram(self):
        """Display the complete database diagram."""

        connection = self.connect()

        try:

            tables = self.get_tables(
                connection
            )

            print("\n" + "=" * 70)
            print("DATABASE / ER DIAGRAM")
            print("=" * 70)

            if not tables:

                print(
                    "\nNo database tables found."
                )

                return

            # -------------------------------------------------
            # TABLE STRUCTURE
            # -------------------------------------------------

            print(
                "\nTABLE STRUCTURE"
            )

            print(
                "-" * 70
            )

            for index, table in enumerate(tables):

                print(
                    self.generate_table_block(
                        connection,
                        table
                    )
                )

                if index < len(tables) - 1:

                    print(
                        "\n"
                    )

            # -------------------------------------------------
            # RELATIONSHIPS
            # -------------------------------------------------

            relationships = (
                self.generate_relationships(
                    connection,
                    tables
                )
            )

            print(
                "\nRELATIONSHIPS"
            )

            print(
                "-" * 70
            )

            if relationships:

                for relationship in relationships:

                    print(
                        f"  {relationship}"
                    )

            else:

                print(
                    "  No relationships detected."
                )

            # -------------------------------------------------
            # SUMMARY
            # -------------------------------------------------

            print(
                "\n" + "-" * 70
            )

            print(
                f"Total tables: {len(tables)}"
            )

            print(
                f"Total relationships: "
                f"{len(relationships)}"
            )

            print(
                "=" * 70
            )

        except sqlite3.Error as error:

            print(
                f"Database diagram error: {error}"
            )

        finally:

            connection.close()


# =============================================================
# TEST DATABASE DIAGRAM
# =============================================================

if __name__ == "__main__":

    generator = DatabaseDiagramGenerator()

    generator.display_diagram()