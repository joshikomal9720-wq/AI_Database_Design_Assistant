class ForeignKeyGenerator:
    """Generates foreign keys from detected relationships."""

    def singularize(self, word):
        """Convert common plural nouns to singular form."""

        if word.endswith("ies"):
            return word[:-3] + "y"

        if word.endswith("ses"):
            return word[:-2]

        if word.endswith("s") and not word.endswith("ss"):
            return word[:-1]

        return word

    def generate_foreign_keys(self, relationships):
        foreign_keys = []

        for relationship in relationships:

            parent = relationship["from"].lower()
            child = relationship["to"].lower()
            relationship_type = relationship["type"]

            # One-to-Many
            # Example: customers -> orders
            # FK goes into orders
            if relationship_type == "One-to-Many":

                parent_singular = self.singularize(parent)

                foreign_key = {
                    "table": child,
                    "column": f"{parent_singular}_id",
                    "references": f"{parent}(id)",
                    "relationship_type": relationship_type
                }

            # Many-to-One
            # Example: products -> categories
            # FK goes into products
            elif relationship_type == "Many-to-One":

                child_singular = self.singularize(child)

                foreign_key = {
                    "table": parent,
                    "column": f"{child_singular}_id",
                    "references": f"{child}(id)",
                    "relationship_type": relationship_type
                }

            # One-to-One
            # Example: orders -> payments
            # FK goes into payments
            elif relationship_type == "One-to-One":

                parent_singular = self.singularize(parent)

                foreign_key = {
                    "table": child,
                    "column": f"{parent_singular}_id",
                    "references": f"{parent}(id)",
                    "relationship_type": relationship_type
                }

            # Many-to-Many
            # Requires a junction table.
            # We will handle this separately later.
            elif relationship_type == "Many-to-Many":

                continue

            else:
                continue

            # Avoid duplicate foreign keys
            if foreign_key not in foreign_keys:
                foreign_keys.append(foreign_key)

        return foreign_keys


if __name__ == "__main__":

    relationships = [
        {
            "from": "customers",
            "to": "orders",
            "type": "One-to-Many"
        },
        {
            "from": "products",
            "to": "categories",
            "type": "Many-to-One"
        },
        {
            "from": "orders",
            "to": "payments",
            "type": "One-to-One"
        }
    ]

    generator = ForeignKeyGenerator()

    foreign_keys = generator.generate_foreign_keys(
        relationships
    )

    print("Detected Relationships:")

    for relationship in relationships:
        print(
            f"- {relationship['from']} → "
            f"{relationship['to']} "
            f"({relationship['type']})"
        )

    print("\nGenerated Foreign Keys:")

    for foreign_key in foreign_keys:
        print(
            f"- Table: {foreign_key['table']} | "
            f"Column: {foreign_key['column']} | "
            f"References: {foreign_key['references']}"
        )