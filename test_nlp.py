from src.nlp_processor import NLPProcessor


# Create NLP processor
processor = NLPProcessor()

# Sample database requirement
text = """
Customers have multiple orders.
Each customer has a name and email.
Each order has an order date and total amount.
"""

# Process the text
result = processor.preprocess_text(text)

# Display the result
print("Original Text:")
print(text)

print("\nProcessed Tokens:")
print(result)