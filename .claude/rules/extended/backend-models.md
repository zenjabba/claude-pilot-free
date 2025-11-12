
# Backend Models

## When to use this skill

- When creating or modifying database model files (models.py, models/, schema.prisma, etc.)
- When defining ORM classes or ActiveRecord models for database tables
- When establishing table relationships (one-to-many, many-to-many, has-many, belongs-to)
- When configuring foreign keys, indexes, and cascade behaviors
- When implementing model-level validation rules
- When adding timestamp fields (created_at, updated_at) for auditing
- When setting database constraints (NOT NULL, UNIQUE, CHECK constraints)
- When choosing appropriate data types for model fields
- When balancing normalization with query performance needs
- When defining model methods or scopes for common queries

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle backend models.

## Instructions

- **Clear Naming**: Use singular names for models and plural for tables following your framework's conventions
- **Timestamps**: Include created and updated timestamps on all tables for auditing and debugging
- **Data Integrity**: Use database constraints (NOT NULL, UNIQUE, foreign keys) to enforce data rules at the database level
- **Appropriate Data Types**: Choose data types that match the data's purpose and size requirements
- **Indexes on Foreign Keys**: Index foreign key columns and other frequently queried fields for performance
- **Validation at Multiple Layers**: Implement validation at both model and database levels for defense in depth
- **Relationship Clarity**: Define relationships clearly with appropriate cascade behaviors and naming conventions
- **Avoid Over-Normalization**: Balance normalization with practical query performance needs
