import re


class AttributeExtractor:
    """Extract attributes for database entities from natural language."""

    def extract_attributes(self, text, entity):
        """
        Extract attributes associated with a given entity.

        Example:
        Each customer has a name, email, phone, and address.
        """

        attributes = []

        # Match:
        # customer has ...
        # each customer has ...
        pattern = rf"(?:each\s+)?{re.escape(entity)}s?\s+(?:has|have)\s+(.*?)(?:\.|$)"

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for match in matches:
            attributes.extend(
                self._clean_attributes(match)
            )

        # Remove duplicates while preserving order
        unique_attributes = []

        for attribute in attributes:
            if attribute not in unique_attributes:
                unique_attributes.append(attribute)

        return unique_attributes

    def _clean_attributes(self, attribute_text):
        """Clean and split extracted attribute text."""

        # Remove introductory words
        attribute_text = re.sub(
            r"\b(a|an|the)\b",
            "",
            attribute_text,
            flags=re.IGNORECASE
        )

        # Normalize whitespace
        attribute_text = re.sub(
            r"\s+",
            " ",
            attribute_text
        ).strip()

        # Split by commas
        parts = re.split(
            r",",
            attribute_text
        )

        attributes = []

        for part in parts:

            part = part.strip()

            if not part:
                continue

            # Remove "and" when it appears at the beginning
            # Example:
            # "and address" -> "address"
            part = re.sub(
                r"^\s*and\s+",
                "",
                part,
                flags=re.IGNORECASE
            )

            # Split attributes joined directly by "and"
            and_parts = re.split(
                r"\s+\band\b\s+",
                part,
                flags=re.IGNORECASE
            )

            for attribute in and_parts:

                attribute = attribute.strip().lower()

                # Remove leading "and" if still present
                attribute = re.sub(
                    r"^and\s+",
                    "",
                    attribute,
                    flags=re.IGNORECASE
                )

                # Normalize whitespace
                attribute = re.sub(
                    r"\s+",
                    " ",
                    attribute
                ).strip()

                if attribute:
                    attributes.append(attribute)

        return attributes


if __name__ == "__main__":

    extractor = AttributeExtractor()

    text = """
    Each customer has a name, email, phone, and address.
    Each category has a name.
    Each product has a name, description, price, and quantity.
    Each order has an order date, total amount, and status.
    Each payment has a payment date and amount.
    """

    print("Original Requirement:")
    print(text)

    entities = [
        "customer",
        "category",
        "product",
        "order",
        "payment"
    ]

    print("\nExtracted Attributes:")

    for entity in entities:

        attributes = extractor.extract_attributes(
            text,
            entity
        )

        print(f"\n{entity}:")

        for attribute in attributes:
            print("-", attribute)