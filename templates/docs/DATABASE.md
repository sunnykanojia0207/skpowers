# Database

The source of truth for the data model. Agents never invent tables, columns, relationships or naming; they propose changes here first.

## 1. Engine and hosting
- Database:
- Hosting / provider:
- Migration tool and command:

## 2. Naming conventions
Tables, columns, primary keys, foreign keys, timestamps, enums.

## 3. Tables
For each table:
### `table_name`
- Purpose:
- Columns: name, type, null/default, constraints
- Ownership: which user or tenant may read and write rows

## 4. Relationships
e.g. `users 1–n projects`, `projects 1–n tasks`.

## 5. Constraints and indexes
- Required and unique fields:
- Foreign keys and on-delete behaviour:
- Indexes, and the queries they serve:

## 6. Data rules
- Validation enforced by the database:
- Soft delete (yes/no, how):
- Auditing (created/updated/deleted by, activity history):
- Sensitive fields and their protection (see `docs/SECURITY.md`):

## 7. Migrations
Every schema change is documented here, has a versioned migration, is tested, is reversible or has a data plan, and never breaks existing production data. Destructive migrations need explicit approval.

## 8. Seed data
What development and demo data exists and how to load it.
