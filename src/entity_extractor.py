import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer


class EntityExtractor:
    """Extracts potential database entities from natural language."""

    def __init__(self):

        self.stop_words = set(
            stopwords.words("english")
        )

        self.lemmatizer = WordNetLemmatizer()

        # Generic words that should not become database entities
        self.ignored_words = {
            "system",
            "platform",
            "application",
            "software",
            "database",
            "information",
            "data",
            "process",
            "thing",
            "user",

            # Common database attribute names
            "name",
            "email",
            "phone",
            "address",
            "description",
            "price",
            "quantity",
            "date",
            "amount",
            "status",
            "total",
            "order",
        }

    def extract_entities(self, text):
        """
        Identify and normalize nouns that may represent
        database entities.
        """

        # Tokenize the requirement
        tokens = word_tokenize(text)

        # Identify parts of speech
        tagged_tokens = pos_tag(tokens)

        entities = []

        for word, tag in tagged_tokens:

            # Consider nouns as entity candidates
            if tag.startswith("NN"):

                word_lower = word.lower()

                # Ignore stopwords
                if word_lower in self.stop_words:
                    continue

                # Ignore very short words
                if len(word_lower) <= 2:
                    continue

                # Ignore generic words and attributes
                if word_lower in self.ignored_words:
                    continue

                # Convert plural nouns to singular form
                entity = self.lemmatizer.lemmatize(
                    word_lower,
                    pos="n"
                )

                # Add only unique entities
                if entity not in entities:
                    entities.append(entity)

        return entities


if __name__ == "__main__":

    extractor = EntityExtractor()

    requirement = """
    We need an e-commerce system with customers, products,
    categories, orders, and payments.

    Each customer has a name, email, phone, and address.
    Each product has a name, description, price, and quantity.
    Each order has an order date, total amount, and status.
    Each payment has a payment date and amount.
    """

    entities = extractor.extract_entities(
        requirement
    )

    print("Extracted Entities:")

    for entity in entities:
        print("-", entity)