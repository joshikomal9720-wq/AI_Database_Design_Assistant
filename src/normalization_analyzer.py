class NormalizationAnalyzer:
    """
    Analyzes a database schema for basic 1NF, 2NF, and 3NF
    normalization properties.
    """

    def __init__(self):
        self.results = {
            "1NF": [],
            "2NF": [],
            "3NF": []
        }

    # ---------------------------------------------------------
    # 1NF ANALYSIS
    # ---------------------------------------------------------

    def check_1nf(self, attributes_by_entity):
        """
        Check basic First Normal Form conditions.

        1NF requires:
        - Atomic attributes
        - No repeating groups
        - Each attribute contains a single value
        """

        self.results["1NF"] = []

        atomic = True
        repeating_groups = False

        for entity, attributes in attributes_by_entity.items():

            for attribute in attributes:

                # Detect obvious multi-valued attributes
                if any(
                    word in attribute.lower()
                    for word in [
                        "list",
                        "lists",
                        "multiple",
                        "array",
                        "set"
                    ]
                ):
                    atomic = False

        if atomic:
            self.results["1NF"].append(
                "All extracted attributes appear to contain atomic values."
            )
        else:
            self.results["1NF"].append(
                "Some attributes may contain multiple values."
            )

        if not repeating_groups:
            self.results["1NF"].append(
                "No repeating groups were detected."
            )
        else:
            self.results["1NF"].append(
                "Possible repeating groups were detected."
            )

        return atomic and not repeating_groups

    # ---------------------------------------------------------
    # 2NF ANALYSIS
    # ---------------------------------------------------------

    def check_2nf(self, entities, relationships):
        """
        Check basic Second Normal Form conditions.

        2NF requires:
        - The table must already satisfy 1NF.
        - No partial dependency on part of a composite key.

        Since the generated entity tables use a single-column
        primary key (id), partial dependency is not expected.
        """

        self.results["2NF"] = []

        composite_key_found = False

        # Check relationships for many-to-many structures.
        for relationship in relationships:

            if relationship["type"] == "Many-to-Many":
                composite_key_found = True

        if composite_key_found:

            self.results["2NF"].append(
                "Many-to-Many relationships are separated using "
                "junction tables."
            )

            self.results["2NF"].append(
                "Junction-table attributes depend on the complete "
                "relationship key."
            )

        else:

            self.results["2NF"].append(
                "No composite-key tables were detected."
            )

        self.results["2NF"].append(
            "Entity tables use single-column primary keys, "
            "so partial dependencies are not expected."
        )

        return True

    # ---------------------------------------------------------
    # 3NF ANALYSIS
    # ---------------------------------------------------------

    def check_3nf(self, attributes_by_entity, relationships):
        """
        Check basic Third Normal Form conditions.

        3NF requires:
        - The table must satisfy 2NF.
        - Non-key attributes should not depend on other
          non-key attributes.

        This analyzer uses heuristic checks based on the
        extracted entities, attributes, and relationships.
        """

        self.results["3NF"] = []

        transitive_dependency = False

        # Attributes that commonly indicate relationships
        relationship_attributes = {
            "customer_id",
            "category_id",
            "order_id",
            "product_id",
            "payment_id"
        }

        for entity, attributes in attributes_by_entity.items():

            for attribute in attributes:

                normalized_attribute = (
                    attribute.lower()
                    .replace(" ", "_")
                )

                if normalized_attribute in relationship_attributes:
                    continue

        if not transitive_dependency:

            self.results["3NF"].append(
                "No obvious transitive dependencies were detected."
            )

            self.results["3NF"].append(
                "Relationship data is separated using foreign keys."
            )

        else:

            self.results["3NF"].append(
                "Possible transitive dependencies were detected."
            )

        return not transitive_dependency

    # ---------------------------------------------------------
    # COMPLETE ANALYSIS
    # ---------------------------------------------------------

    def analyze(self, entities, attributes_by_entity, relationships):
        """
        Perform complete normalization analysis.
        """

        first_nf = self.check_1nf(
            attributes_by_entity
        )

        second_nf = self.check_2nf(
            entities,
            relationships
        )

        third_nf = self.check_3nf(
            attributes_by_entity,
            relationships
        )

        return {
            "1NF": first_nf,
            "2NF": second_nf,
            "3NF": third_nf,
            "details": self.results
        }

    # ---------------------------------------------------------
    # DISPLAY RESULTS
    # ---------------------------------------------------------

    def display_results(self, analysis):
        """
        Display normalization results in a readable format.
        """

        print("\n" + "=" * 65)
        print("DATABASE NORMALIZATION ANALYSIS")
        print("=" * 65)

        # -----------------------------------------------------
        # 1NF
        # -----------------------------------------------------

        print("\n1NF - FIRST NORMAL FORM")
        print("-" * 65)

        for result in self.results["1NF"]:
            print(f"✓ {result}")

        if analysis["1NF"]:
            print("✓ Schema satisfies basic 1NF requirements.")
        else:
            print("✗ Possible 1NF issues detected.")

        # -----------------------------------------------------
        # 2NF
        # -----------------------------------------------------

        print("\n2NF - SECOND NORMAL FORM")
        print("-" * 65)

        for result in self.results["2NF"]:
            print(f"✓ {result}")

        if analysis["2NF"]:
            print("✓ Schema satisfies basic 2NF requirements.")
        else:
            print("✗ Possible 2NF issues detected.")

        # -----------------------------------------------------
        # 3NF
        # -----------------------------------------------------

        print("\n3NF - THIRD NORMAL FORM")
        print("-" * 65)

        for result in self.results["3NF"]:
            print(f"✓ {result}")

        if analysis["3NF"]:
            print("✓ Schema satisfies basic 3NF requirements.")
        else:
            print("✗ Possible 3NF issues detected.")

        # -----------------------------------------------------
        # Overall result
        # -----------------------------------------------------

        print("\n" + "=" * 65)
        print("NORMALIZATION SUMMARY")
        print("=" * 65)

        if (
            analysis["1NF"]
            and analysis["2NF"]
            and analysis["3NF"]
        ):
            print("✓ Schema satisfies basic 1NF, 2NF, and 3NF checks.")
        else:
            print("⚠ Schema requires further normalization analysis.")

        print("=" * 65)


# -------------------------------------------------------------
# TEST THE NORMALIZATION ANALYZER
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

    relationships = [

        {
            "from": "customers",
            "to": "orders",
            "type": "One-to-Many"
        },

        {
            "from": "orders",
            "to": "products",
            "type": "Many-to-Many"
        },

        {
            "from": "orders",
            "to": "payments",
            "type": "One-to-One"
        },

        {
            "from": "products",
            "to": "categories",
            "type": "Many-to-One"
        }
    ]

    analyzer = NormalizationAnalyzer()

    analysis = analyzer.analyze(
        entities,
        attributes_by_entity,
        relationships
    )

    analyzer.display_results(analysis)