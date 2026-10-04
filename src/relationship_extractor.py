import re


class RelationshipExtractor:
    """Extract relationships between entities from natural-language requirements."""

    def singularize(self, word):
        """Convert common plural nouns to singular form."""

        word = word.lower().strip()

        if word.endswith("ies"):
            return word[:-3] + "y"

        if word.endswith("ses"):
            return word[:-2]

        if word.endswith("s") and not word.endswith("ss"):
            return word[:-1]

        return word

    def pluralize(self, word):
        """Convert common singular nouns to plural form."""

        word = self.singularize(word)

        if word.endswith("y") and not word.endswith(
            ("ay", "ey", "iy", "oy", "uy")
        ):
            return word[:-1] + "ies"

        if word.endswith(("s", "x", "z", "ch", "sh")):
            return word + "es"

        return word + "s"

    def normalize_entity(self, word):
        """Return a consistent plural table/entity name."""

        return self.pluralize(word)

    def extract_relationships(self, text, entities):
        """
        Extract relationships between known entities.

        Supported relationship types:
        - One-to-Many
        - Many-to-Many
        - One-to-One
        - Many-to-One
        """

        relationships = []

        # --------------------------------------------------
        # Normalize known entities
        # --------------------------------------------------

        known_entities = set()

        for entity in entities:
            known_entities.add(
                self.singularize(entity)
            )

        # --------------------------------------------------
        # 1. ONE-TO-MANY
        #
        # Example:
        # Customers can place multiple orders.
        #
        # Result:
        # customers -> orders
        # --------------------------------------------------

        pattern_one_to_many = (
            r"(\w+)\s+can\s+"
            r"(?:place|create|make|have)\s+"
            r"(?:multiple|many)\s+(\w+)"
        )

        matches = re.findall(
            pattern_one_to_many,
            text,
            re.IGNORECASE
        )

        for entity1, entity2 in matches:

            entity1 = self.singularize(entity1)
            entity2 = self.singularize(entity2)

            if (
                entity1 in known_entities
                and entity2 in known_entities
            ):

                relationship = {
                    "from": self.normalize_entity(entity1),
                    "to": self.normalize_entity(entity2),
                    "type": "One-to-Many"
                }

                if relationship not in relationships:
                    relationships.append(relationship)

        # --------------------------------------------------
        # 2. MANY-TO-MANY
        #
        # Example:
        # Each order contains products.
        #
        # Result:
        # orders -> products
        # --------------------------------------------------

        pattern_many_to_many = (
            r"each\s+(\w+)\s+contains\s+(\w+)"
        )

        matches = re.findall(
            pattern_many_to_many,
            text,
            re.IGNORECASE
        )

        for entity1, entity2 in matches:

            entity1 = self.singularize(entity1)
            entity2 = self.singularize(entity2)

            if (
                entity1 in known_entities
                and entity2 in known_entities
            ):

                relationship = {
                    "from": self.normalize_entity(entity1),
                    "to": self.normalize_entity(entity2),
                    "type": "Many-to-Many"
                }

                if relationship not in relationships:
                    relationships.append(relationship)

        # --------------------------------------------------
        # 3. ONE-TO-ONE
        #
        # Example:
        # Each order contains products and has a payment.
        #
        # Result:
        # orders -> payments
        #
        # The .*? allows other words/phrases between
        # the entity and "has".
        #
        # It also prevents:
        # payments -> payments
        # from:
        # "Each payment has a payment date and amount."
        # --------------------------------------------------

        pattern_one_to_one = (
            r"each\s+(\w+)\s+.*?\bhas\s+(?:a|an)\s+(\w+)"
        )

        matches = re.findall(
            pattern_one_to_one,
            text,
            re.IGNORECASE
        )

        for entity1, entity2 in matches:

            entity1 = self.singularize(entity1)
            entity2 = self.singularize(entity2)

            # Prevent false self-relationships.
            if entity1 == entity2:
                continue

            if (
                entity1 in known_entities
                and entity2 in known_entities
            ):

                relationship = {
                    "from": self.normalize_entity(entity1),
                    "to": self.normalize_entity(entity2),
                    "type": "One-to-One"
                }

                if relationship not in relationships:
                    relationships.append(relationship)

        # --------------------------------------------------
        # 4. MANY-TO-ONE
        #
        # Example:
        # Products belong to categories.
        #
        # Result:
        # products -> categories
        # --------------------------------------------------

        pattern_many_to_one = (
            r"(\w+)\s+belong\s+to\s+(\w+)"
        )

        matches = re.findall(
            pattern_many_to_one,
            text,
            re.IGNORECASE
        )

        for entity1, entity2 in matches:

            entity1 = self.singularize(entity1)
            entity2 = self.singularize(entity2)

            if (
                entity1 in known_entities
                and entity2 in known_entities
            ):

                relationship = {
                    "from": self.normalize_entity(entity1),
                    "to": self.normalize_entity(entity2),
                    "type": "Many-to-One"
                }

                if relationship not in relationships:
                    relationships.append(relationship)

        return relationships


# ==========================================================
# TEST THE RELATIONSHIP EXTRACTOR
# ==========================================================

if __name__ == "__main__":

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

    entities = [
        "customer",
        "product",
        "category",
        "order",
        "payment"
    ]

    extractor = RelationshipExtractor()

    relationships = extractor.extract_relationships(
        requirement,
        entities
    )

    print("Extracted Relationships:")

    for relationship in relationships:

        print(
            f"- {relationship['from']} → "
            f"{relationship['to']} "
            f"({relationship['type']})"
        )