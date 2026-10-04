class DataTypeMapper:
    """
    Suggests SQL data types based on attribute names.
    """

    def __init__(self):

        self.type_rules = {

            # Integer attributes
            "id": "INTEGER",
            "quantity": "INTEGER",
            "count": "INTEGER",
            "age": "INTEGER",

            # Decimal attributes
            "price": "DECIMAL(10,2)",
            "amount": "DECIMAL(10,2)",
            "total_amount": "DECIMAL(10,2)",
            "salary": "DECIMAL(10,2)",

            # Date attributes
            "date": "DATE",
            "order_date": "DATE",
            "payment_date": "DATE",
            "birth_date": "DATE",

            # Text attributes
            "description": "TEXT",
            "address": "VARCHAR(255)",

            # Common string attributes
            "name": "VARCHAR(100)",
            "email": "VARCHAR(255)",
            "phone": "VARCHAR(20)",
            "status": "VARCHAR(50)"
        }

    def suggest_type(self, attribute):
        """
        Suggest an SQL data type for an attribute.
        """

        attribute = attribute.lower().strip()

        # Direct match
        if attribute in self.type_rules:
            return self.type_rules[attribute]

        # Foreign-key attributes
        if attribute.endswith("_id"):
            return "INTEGER"

        # Date-related attributes
        if "date" in attribute:
            return "DATE"

        # Amount/price-related attributes
        if (
            "amount" in attribute
            or "price" in attribute
            or "cost" in attribute
        ):
            return "DECIMAL(10,2)"

        # Quantity-related attributes
        if (
            "quantity" in attribute
            or "count" in attribute
        ):
            return "INTEGER"

        # Description/text-related attributes
        if (
            "description" in attribute
            or "comment" in attribute
            or "address" in attribute
        ):
            return "TEXT"

        # Default type
        return "VARCHAR(255)"

    def suggest_types(self, attributes):
        """
        Suggest data types for a list of attributes.
        """

        suggestions = {}

        for attribute in attributes:

            suggestions[attribute] = self.suggest_type(
                attribute
            )

        return suggestions


# ---------------------------------------------------------
# TEST DATA TYPE MAPPER
# ---------------------------------------------------------

if __name__ == "__main__":

    mapper = DataTypeMapper()

    attributes = [
        "id",
        "name",
        "email",
        "phone",
        "address",
        "description",
        "price",
        "quantity",
        "order_date",
        "total_amount",
        "status",
        "category_id"
    ]

    print("=" * 60)
    print("DATA TYPE SUGGESTIONS")
    print("=" * 60)

    suggestions = mapper.suggest_types(attributes)

    for attribute, data_type in suggestions.items():

        print(
            f"- {attribute:<20} → {data_type}"
        )