from src.entity_extractor import EntityExtractor


# Create entity extractor
extractor = EntityExtractor()

# Sample database requirement
text = """
We need an e-commerce system with customers, products,
categories, orders, and payments.
Customers can place multiple orders.
Each order contains products and has a payment.
"""

# Extract entities
entities = extractor.extract_entities(text)

print("Original Requirement:")
print(text)

print("\nExtracted Entities:")
for entity in entities:
    print("-", entity)