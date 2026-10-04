# AI Database Design Assistant

An AI-assisted database design tool that converts natural-language system requirements into a structured relational database schema.

The project uses Natural Language Processing (NLP) techniques to identify entities, attributes, relationships, foreign keys, data types, normalization requirements, and database optimization opportunities from natural-language requirements.

---

## Project Overview

Designing a database manually from textual requirements requires identifying entities, attributes, relationships, keys, data types, constraints, and normalization rules.

The **AI Database Design Assistant** automates several of these database-design tasks.

The system accepts a natural-language database requirement and processes it through multiple stages to generate a structured relational database schema.

### System Workflow

```text
Natural Language Requirement
            ↓
      NLP Processing
            ↓
      Entity Extraction
            ↓
     Attribute Extraction
            ↓
    Relationship Detection
            ↓
    Foreign Key Generation
            ↓
   Many-to-Many Detection
            ↓
    Normalization Analysis
            ↓
      Data Type Mapping
            ↓
    Optimization Analysis
            ↓
     SQL Schema Generation
            ↓
      SQLAlchemy Schema
            ↓
       SQLite Database
            ↓
         Validation
            ↓
      Database / ER Diagram


## Objectives

The main objectives of this project are:
- Convert natural-language requirements into database design components.
- Automatically identify potential database entities.
- Extract attributes associated with entities.
- Detect relationships between entities.
- Generate appropriate primary keys and foreign keys.
- Handle One-to-Many, Many-to-One, One-to-One, and Many-to-Many relationships.
- Generate junction tables for Many-to-Many relationships.
- Analyze basic 1NF, 2NF, and 3NF normalization requirements.
- Suggest appropriate SQL data types.
- Generate executable SQL database schemas.
- Represent the database schema using SQLAlchemy.
- Create and manage a SQLite database.
- Generate useful database indexes.
- Provide basic database optimization recommendations.
- Validate the generated database structure and foreign-key relationships.
- Generate a database/ER diagram from the created database.

## Features

1. Natural Language Processing
The system preprocesses natural-language requirements using NLTK.
The NLP processing stage performs tasks such as:
- Tokenization
- Stop-word removal
- Part-of-speech tagging
- Lemmatization
This processed information is used by subsequent database-design components.

2. Entity Extraction
Potential database entities are automatically extracted from the natural-language requirement.
For the demonstration e-commerce system, entities such as:
Customer
Product
Category
Order
Payment
are identified.
The extracted entities are then used as the basis for generating database tables.

3. Attribute Extraction
The system identifies attributes associated with each extracted entity.
For example:
Customer
name
email
phone
address

Product
name
description
price
quantity

Order
order_date
total_amount
status

Payment
payment_date
amount

These attributes are later mapped to database columns.

4. Relationship Detection
The system detects relationships between entities based on natural-language statements.
The demonstration requirement produces relationships such as:
Customers → Orders
One-to-Many

Orders → Products
Many-to-Many

Orders → Payments
One-to-One

Products → Categories
Many-to-One

These relationships are used to generate foreign keys and junction tables.

5. Foreign Key Generation
Foreign keys are automatically generated based on detected relationships.
For example:
orders.customer_id → customers.id
payments.order_id → orders.id
products.category_id → categories.id

The generated foreign keys establish relationships between the database tables.

6. Many-to-Many Relationship Handling
Many-to-Many relationships require an intermediate junction table.
For example:
Orders ←→ Products
is represented using:
order_items

The order_items table contains:
id
order_id
product_id
quantity
price

The table also includes foreign keys:
order_items.order_id → orders.id
order_items.product_id → products.id

A composite UNIQUE constraint is also used:
UNIQUE (order_id, product_id)

This helps prevent duplicate combinations of the same order and product. 


7. Data Type Mapping
The system suggests SQL data types based on attribute names.
Examples:
| Attribute | Suggested SQL Type |
|-----------|--------------------|
| `name` | `VARCHAR(100)` |
| `email` | `VARCHAR(255)` |
| `phone` | `VARCHAR(20)` |
| `price` | `DECIMAL(10,2)` |
| `quantity` | `INTEGER` |
| `order_date` | `DATE` |
| `description` | `TEXT` |
| `address` | `VARCHAR(255)` |

The data type mapper uses predefined rules and attribute-name patterns to provide suitable type suggestions.


8. Database Normalization Analysis
The system performs basic heuristic checks for:
- First Normal Form (1NF)
- Second Normal Form (2NF)
- Third Normal Form (3NF)
For the current demonstration schema, the implemented checks report that the schema satisfies the basic requirements for 1NF, 2NF, and 3NF.
Normalization Note
The normalization analyzer provides heuristic analysis based on the extracted schema.
It is not intended to replace a formal database normalization proof or detailed dependency analysis.


9. Database Optimization
The system analyzes foreign keys and Many-to-Many relationships to suggest useful database indexes.
The current demonstration produces index recommendations such as:
idx_orders_customer_id
idx_payments_order_id
idx_products_category_id
idx_order_items_order_id
idx_order_items_product_id
The system also provides basic optimization recommendations, including:
- Indexing foreign-key columns.
- Indexing Many-to-Many relationship columns.
- Avoiding unnecessary indexes.
- Using appropriate data types.
- Considering the storage and update overhead of indexes.
- Recognizing that primary keys are automatically indexed by SQLite.


10. SQL Schema Generation
The system generates SQL CREATE TABLE statements from the extracted database design.
Example:
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    address VARCHAR(255)
);

The generated schema includes:
- Primary keys
- Foreign keys
- Appropriate data types
- Junction tables
- UNIQUE constraints


11. SQLAlchemy Integration
The project uses SQLAlchemy to represent the database schema using Python database objects.
The SQLAlchemy component demonstrates:
- Tables
- Columns
- Primary keys
- Foreign keys
- Data types
- Unique constraints
The project also demonstrates generating SQL statements from the SQLAlchemy schema representation.


12. SQLite Database Creation
The generated SQL schema is executed against a SQLite database.
The project creates:
database.db
The database contains the generated tables, foreign keys, and indexes.
SQLite is used because it provides a lightweight relational database environment without requiring an external database server.


13. Database Inspection
The project provides functionality for inspecting the generated database.
The database manager can display:
- Database tables
- Table structures
- Columns
- Primary keys
- Foreign keys
- Indexes
This allows the generated database to be inspected directly from the program output.


14. Database Validation
The generated SQLite database is validated using SQLite integrity checks.
The system checks:
- Database integrity
- Foreign-key enforcement
- Foreign-key consistency
- Generated tables
- Generated indexes
Example validation output:
✓ Database integrity check passed.
✓ Foreign-key enforcement is enabled.
✓ Foreign-key integrity check passed.


15. Database / ER Diagram
The project includes a database diagram generator that reads the SQLite database structure.
The diagram functionality displays:
- Tables
- Columns
- Primary keys
- Foreign keys
- Relationships
- Total number of tables
- Total number of relationships
The project also includes a visual ER diagram for documentation.
The visual diagram is stored in:
docs/er_diagram.png


### Example Requirement
The current demonstration uses an e-commerce database requirement.
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

The system processes this requirement and generates a relational database design.


### Generated Database Design
The system generates the following six tables:
categories
customers
products
orders
payments
order_items


### Generated Entities
customer
product
category
order
payment


### Generated Attributes
Customer
name
email
phone
address

Category
name

Product
name
description
price
quantity

Order
order_date
total_amount
status

Payment
payment_date
amount


### Generated Relationships
customers → orders
One-to-Many

orders → products
Many-to-Many

orders → payments
One-to-One

products → categories
Many-to-One


### Generated Foreign Keys
orders.customer_id → customers.id
payments.order_id → orders.id
products.category_id → categories.id
order_items.order_id → orders.id
order_items.product_id → products.id


#### Generated Database Structure
1. categories
categories
│
├── id
└── name

Primary Key:id

2. customers
customers
│
├── id
├── name
├── email
├── phone
└── address

Primary Key:id

3. products
products
│
├── id
├── name
├── description
├── price
├── quantity
└── category_id

Primary Key:id

Foreign Key:category_id → categories.id

4. orders
orders
│
├── id
├── order_date
├── total_amount
├── status
└── customer_id

Primary Key:id

Foreign Key:customer_id → customers.id

5. payments
payments
│
├── id
├── payment_date
├── amount
└── order_id

Primary Key:id

Foreign Key:order_id → orders.id

6. order_items
order_items
│
├── id
├── order_id
├── product_id
├── quantity
└── price

Primary Key:id

Foreign Keys:order_id → orders.id

product_id → products.id

Unique Constraint:
UNIQUE (order_id, product_id)


Database Relationships
The final database contains five foreign-key relationships:
order_items.product_id → products.id

order_items.order_id → orders.id

orders.customer_id → customers.id

payments.order_id → orders.id

products.category_id → categories.id

Overall relationship structure:
                 ┌──────────────┐
                 │  categories  │
                 └──────┬───────┘
                        │
                        │ category_id
                        │
                 ┌──────▼───────┐
                 │   products   │
                 └──────┬───────┘
                        │
                        │ product_id
                        │
                 ┌──────▼────────┐
                 │  order_items  │
                 └──────┬────────┘
                        │
                        │ order_id
                        │
                 ┌──────▼───────┐
                 │    orders    │
                 └──────┬───────┘
                        │
              ┌─────────┴─────────┐
              │                   │
              │ customer_id       │ order_id
              │                   │
       ┌──────▼───────┐    ┌──────▼───────┐
       │  customers   │    │   payments   │
       └──────────────┘    └──────────────┘


### Normalization Analysis
The current implementation performs basic checks for:
1NF
2NF
3NF

The current sample schema produces:
1NF
✓ Schema satisfies basic 1NF requirements.

2NF
✓ Schema satisfies basic 2NF requirements.

3NF
✓ Schema satisfies basic 3NF requirements.

The implementation uses heuristic checks rather than a formal dependency-analysis engine.


### Optimization Analysis
The system identifies indexing opportunities based on foreign keys and Many-to-Many relationships.
Suggested Indexes
idx_orders_customer_id
idx_payments_order_id
idx_products_category_id
idx_order_items_order_id
idx_order_items_product_id

#### Optimization Recommendations
The system provides recommendations such as:
- Foreign-key columns can benefit from indexes for faster joins and relationship lookups.
- Junction-table relationship columns should be indexed for efficient Many-to-Many queries.
- Composite UNIQUE constraints can help prevent duplicate relationships.
- Unnecessary indexes should be avoided because they require storage and can affect write performance.
- Appropriate data types can reduce storage requirements.
- Primary keys are automatically indexed by SQLite.


SQLAlchemy Schema
The project also builds a SQLAlchemy representation of the database schema.
The representation includes:
categories
customers
products
orders
payments
order_items

It represents:
- Columns
- Primary keys
- Foreign keys
- SQL data types
- UNIQUE constraints
This demonstrates the integration of SQLAlchemy into the database-design pipeline.



### Project Structure
AI_Database_Design_Assistant/
│
├── docs/
│   └── er_diagram.png
│
├── src/
│   ├── nlp_processor.py
│   ├── entity_extractor.py
│   ├── attribute_extractor.py
│   ├── relationship_extractor.py
│   ├── foreign_key_generator.py
│   ├── schema_generator.py
│   ├── database_manager.py
│   ├── normalization_analyzer.py
│   ├── data_type_mapper.py
│   ├── optimization_analyzer.py
│   ├── sqlalchemy_schema.py
│   └── database_diagram.py
│
├── venv/
│
├── database.db
├── main.py
├── requirements.txt
├── README.md
│
├── test_nlp.py
├── test_entity_extractor.py
├── test_database.py
└── test_schema_database.py


### File Description
| File                          | Purpose                                                        |
|------                         |--------                                                        |
| `main.py`                     | Main application pipeline                                      |
| `nlp_processor.py`            | NLP preprocessing                                              |
| `entity_extractor.py`         | Entity extraction                                              |
| `attribute_extractor.py`      | Attribute extraction                                           |
| `relationship_extractor.py`   | Relationship detection                                         | 
| `foreign_key_generator.py`    | Foreign-key generation                                         |
| `schema_generator.py`         | SQL schema generation                                          |
| `database_manager.py`         | SQLite database creation, inspection, indexing, and validation |
| `normalization_analyzer.py`   | Basic 1NF, 2NF, and 3NF analysis                               |
| `data_type_mapper.py`         | SQL data type suggestions                                      |
| `optimization_analyzer.py`    | Index suggestions and optimization recommendations             |
| `sqlalchemy_schema.py`        | SQLAlchemy schema representation                               |
| `database_diagram.py`         | Database/ER diagram generation                                 |
| `er_diagram.png`              | Visual database/ER diagram                                     |
| `requirements.txt`            | Python dependencies                                            |
| `database.db`                 | Generated SQLite database                                      |
| `test_*.py`                   | Component testing files                                        |


#### Technologies Used
Programming Language
- Python
Natural Language Processing
- NLTK
Database
- SQLite
- SQL
Database Toolkit / ORM
- SQLAlchemy
Development Environment
- Visual Studio Code
- Python Virtual Environment



### Requirements
The project requires Python and the following Python packages:
nltk
SQLAlchemy

These dependencies are listed in:
requirements.txt


### Installation
1. Clone the Repository
git clone <repository-url>

2. Navigate to the Project Directory
cd AI_Database_Design_Assistant

3. Create a Virtual Environment
python -m venv venv

4. Activate the Virtual Environment
Windows PowerShell
.\venv\Scripts\Activate.ps1

5. Install Dependencies
pip install -r requirements.txt


#### Running the Project
Make sure the virtual environment is activated.
Run:
python main.py

The complete pipeline will then execute.
The program performs the following operations:
1. Process natural-language requirement
2. Extract entities
3. Extract attributes
4. Detect relationships
5. Generate foreign keys
6. Generate Many-to-Many junction tables
7. Analyze normalization
8. Analyze optimization opportunities
9. Generate SQL schema
10. Build SQLAlchemy schema
11. Create SQLite database
12. Create database indexes
13. Inspect database structure
14. Validate database
15. Display database/ER diagram


#### Running Individual Components
Individual modules can also be executed separately.
For example:
python -m src.database_diagram

This displays the database tables and relationships detected from the SQLite database.
Testing
The project contains test files for important components.
test_nlp.py
test_entity_extractor.py
test_database.py
test_schema_database.py

These files are used to verify individual parts of the system.
The main application can also be executed using:
python main.py

A successful execution should create the database schema and complete the validation checks without database errors.
Sample Output
A successful execution produces output similar to the following.
Extracted Entities
- customer
- product
- category
- order
- payment

Extracted Relationships
- customers → orders (One-to-Many)
- orders → products (Many-to-Many)
- orders → payments (One-to-One)
- products → categories (Many-to-One)

Generated Foreign Keys
- Table: orders | Column: customer_id | References: customers(id)
- Table: payments | Column: order_id | References: orders(id)
- Table: products | Column: category_id | References: categories(id)

Many-to-Many Table
- order_items (junction table)
  Connects orders and products
  Includes quantity and price

Database Result
Total tables: 6
Total relationships: 5

Database Validation
✓ Database integrity check passed.
✓ Foreign-key enforcement is enabled.
✓ Foreign-key integrity check passed.


### Current Results
The implemented system successfully demonstrates:
- Natural-language requirement processing
- NLP preprocessing using NLTK
- Automated entity extraction
- Automated attribute extraction
- Relationship detection
- Foreign-key generation
- Many-to-Many relationship handling
- Junction-table generation
- SQL data type mapping
- SQL schema generation
- SQLAlchemy schema representation
- SQLite database creation
- Database inspection
- Database indexing
- Normalization analysis
- Database validation
- Database/ER diagram generation
- Basic database optimization recommendations
The current demonstration generates a six-table e-commerce database consisting of:
categories
customers
products
orders
payments
order_items

The generated database contains five foreign-key relationships and five recommended indexes.



### Limitations
The current implementation has some limitations:
- Entity and attribute extraction is based on NLP rules and may not correctly interpret every type of natural-language requirement.
- Relationship detection is based on predefined linguistic patterns.
- Data type suggestions are based primarily on attribute names.
- Normalization analysis is heuristic rather than a complete functional-dependency analysis.
- The current demonstration uses a predefined e-commerce requirement.
- More complex business rules may require additional processing or manual refinement.



#### Future Enhancements
Possible future improvements include:
- Integration with spaCy or transformer-based NLP models.
- Support for more complex natural-language requirements.
- Improved semantic relationship detection.
- More advanced normalization analysis.
- Flask or Django web interface.
- Export support for MySQL and PostgreSQL.
- Interactive schema editing.
- AI-based schema recommendations.
- More advanced query-performance analysis.
- Support for additional database constraints.
- Improved handling of complex business rules.


### Internship Project
Project: AI Database Design Assistant
Task ID: AI-PR-007
Student Code: DAS011094
This project was developed as part of an AI/database design internship task.


### Author
Komal Joshi
MCA Student
Birla Institute of Applied Sciences, Nainital
Areas of Interest
- Data Science
- Data Analytics
- Artificial Intelligence
- Machine Learning
- Database Systems


### Conclusion
The AI Database Design Assistant demonstrates a complete workflow for transforming natural-language database requirements into a structured relational database design.
The project combines:

Natural Language Processing
          +
Entity & Attribute Extraction
          +
Relationship Detection
          +
Foreign Key Generation
          +
Normalization Analysis
          +
Data Type Mapping
          +
Optimization Analysis
          +
SQL Schema Generation
          +
SQLAlchemy
          +
SQLite
          +
Database Validation
          +
ER Diagram


The resulting system provides an automated starting point for database design from natural-language requirements while demonstrating core concepts of NLP, relational database design, normalization, SQL, SQLAlchemy, and database optimization.