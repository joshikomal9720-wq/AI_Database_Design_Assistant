import sqlite3


class DatabaseManager:
    """Handles SQLite database operations and schema inspection."""

    def __init__(self, database_name="database.db"):
        self.database_name = database_name

    # =========================================================
    # DATABASE CONNECTION
    # =========================================================

    def connect(self):
        """
        Create a database connection with
        foreign-key enforcement enabled.
        """

        connection = sqlite3.connect(
            self.database_name
        )

        connection.execute(
            "PRAGMA foreign_keys = ON;"
        )

        return connection

    # =========================================================
    # RESET DATABASE
    # =========================================================

    def reset_database(self):
        """
        Remove all existing user-created tables from
        the database so that the current generated schema
        can be created from scratch.
        """

        connection = self.connect()

        try:

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

            tables = cursor.fetchall()

            for table in tables:

                table_name = table[0]

                cursor.execute(
                    f'DROP TABLE IF EXISTS "{table_name}";'
                )

            connection.commit()

            print(
                "Existing database schema reset successfully."
            )

        except sqlite3.Error as error:

            print(
                f"Database reset error: {error}"
            )

        finally:

            connection.close()

    # =========================================================
    # EXECUTE SCHEMA
    # =========================================================

    def execute_schema(self, schema):
        """Execute SQL schema statements."""

        connection = self.connect()

        try:

            connection.executescript(schema)

            connection.commit()

            print(
                "Database schema created successfully."
            )

        except sqlite3.Error as error:

            print(
                f"Database error: {error}"
            )

        finally:

            connection.close()

    # =========================================================
    # SHOW TABLES
    # =========================================================

    def show_tables(self):
        """Display all tables in the database."""

        connection = self.connect()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name NOT LIKE 'sqlite_%'
                ORDER BY name;
                """
            )

            tables = cursor.fetchall()

            print("\nTables in database:")

            if tables:

                for table in tables:

                    print(
                        f"- {table[0]}"
                    )

            else:

                print(
                    "- No tables found."
                )

        finally:

            connection.close()

    # =========================================================
    # SHOW TABLE STRUCTURE
    # =========================================================

    def show_table_structure(self):
        """
        Display columns, data types, primary keys,
        and NOT NULL constraints for every table.
        """

        connection = self.connect()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name NOT LIKE 'sqlite_%'
                ORDER BY name;
                """
            )

            tables = cursor.fetchall()

            print("\n" + "=" * 70)
            print("DATABASE STRUCTURE")
            print("=" * 70)

            for table in tables:

                table_name = table[0]

                print(
                    f"\n{table_name}"
                )

                print(
                    "-" * 70
                )

                cursor.execute(
                    f'PRAGMA table_info("{table_name}");'
                )

                columns = cursor.fetchall()

                for column in columns:

                    column_name = column[1]
                    data_type = column[2]
                    not_null = column[3]
                    primary_key = column[5]

                    key = ""

                    if primary_key:

                        key = " PRIMARY KEY"

                    null_info = ""

                    if not_null:

                        null_info = " NOT NULL"

                    print(
                        f"  {column_name:<20}"
                        f"{data_type:<18}"
                        f"{key}"
                        f"{null_info}"
                    )

        except sqlite3.Error as error:

            print(
                f"Database inspection error: {error}"
            )

        finally:

            connection.close()

    # =========================================================
    # SHOW FOREIGN KEYS
    # =========================================================

    def show_foreign_keys(self):
        """Display all foreign-key relationships."""

        connection = self.connect()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name NOT LIKE 'sqlite_%'
                ORDER BY name;
                """
            )

            tables = cursor.fetchall()

            print("\n" + "=" * 70)
            print("FOREIGN KEY RELATIONSHIPS")
            print("=" * 70)

            found_foreign_key = False

            for table in tables:

                table_name = table[0]

                cursor.execute(
                    f'PRAGMA foreign_key_list("{table_name}");'
                )

                foreign_keys = cursor.fetchall()

                for foreign_key in foreign_keys:

                    found_foreign_key = True

                    referenced_table = foreign_key[2]
                    column = foreign_key[3]
                    referenced_column = foreign_key[4]

                    print(
                        f"- {table_name}.{column} "
                        f"→ "
                        f"{referenced_table}.{referenced_column}"
                    )

            if not found_foreign_key:

                print(
                    "- No foreign keys found."
                )

        except sqlite3.Error as error:

            print(
                f"Foreign-key inspection error: {error}"
            )

        finally:

            connection.close()

    # =========================================================
    # CREATE INDEXES
    # =========================================================

    def create_indexes(self, index_suggestions):
        """
        Create indexes suggested by the
        optimization analyzer.
        """

        connection = self.connect()

        try:

            cursor = connection.cursor()

            print("\n" + "=" * 70)
            print("CREATING DATABASE INDEXES")
            print("=" * 70)

            if not index_suggestions:

                print(
                    "- No indexes to create."
                )

                return

            for index in index_suggestions:

                table = index["table"]
                column = index["column"]

                index_name = (
                    f"idx_{table}_{column}"
                )

                cursor.execute(
                    f"""
                    CREATE INDEX IF NOT EXISTS
                    {index_name}
                    ON {table} ({column});
                    """
                )

                print(
                    f"✓ Created index: "
                    f"{index_name}"
                )

            connection.commit()

        except sqlite3.Error as error:

            print(
                f"Index creation error: {error}"
            )

        finally:

            connection.close()

    # =========================================================
    # SHOW INDEXES
    # =========================================================

    def show_indexes(self):
        """Display indexes created in the database."""

        connection = self.connect()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    name,
                    tbl_name
                FROM sqlite_master
                WHERE type = 'index'
                AND name NOT LIKE 'sqlite_%'
                ORDER BY tbl_name, name;
                """
            )

            indexes = cursor.fetchall()

            print("\n" + "=" * 70)
            print("DATABASE INDEXES")
            print("=" * 70)

            if indexes:

                for index in indexes:

                    print(
                        f"- {index[0]} "
                        f"(table: {index[1]})"
                    )

            else:

                print(
                    "- No indexes found."
                )

        except sqlite3.Error as error:

            print(
                f"Index inspection error: {error}"
            )

        finally:

            connection.close()

    # =========================================================
    # VALIDATE DATABASE
    # =========================================================

    def validate_database(self):
        """Perform basic SQLite database validation."""

        connection = self.connect()

        try:

            cursor = connection.cursor()

            # -------------------------------------------------
            # Database integrity
            # -------------------------------------------------

            cursor.execute(
                "PRAGMA integrity_check;"
            )

            integrity_result = cursor.fetchone()[0]

            print("\n" + "=" * 70)
            print("DATABASE VALIDATION")
            print("=" * 70)

            if integrity_result == "ok":

                print(
                    "✓ Database integrity check passed."
                )

            else:

                print(
                    "✗ Database integrity check failed."
                )

            # -------------------------------------------------
            # Foreign-key enforcement
            # -------------------------------------------------

            cursor.execute(
                "PRAGMA foreign_keys;"
            )

            foreign_keys_enabled = cursor.fetchone()[0]

            if foreign_keys_enabled:

                print(
                    "✓ Foreign-key enforcement is enabled."
                )

            else:

                print(
                    "⚠ Foreign-key enforcement is disabled."
                )

            # -------------------------------------------------
            # Foreign-key integrity
            # -------------------------------------------------

            cursor.execute(
                "PRAGMA foreign_key_check;"
            )

            foreign_key_errors = cursor.fetchall()

            if not foreign_key_errors:

                print(
                    "✓ Foreign-key integrity check passed."
                )

            else:

                print(
                    "✗ Foreign-key integrity issues detected."
                )

                for error in foreign_key_errors:

                    print(
                        f"  - {error}"
                    )

        except sqlite3.Error as error:

            print(
                f"Database validation error: {error}"
            )

        finally:

            connection.close()


# =============================================================
# TEST DATABASE MANAGER
# =============================================================

if __name__ == "__main__":

    manager = DatabaseManager()

    manager.show_tables()

    manager.show_table_structure()

    manager.show_foreign_keys()

    manager.show_indexes()

    manager.validate_database()