# `create_engine()` and `sessionmaker()` in SQLAlchemy

In SQLAlchemy, `create_engine()` and `sessionmaker()` are two core components used to interact with a database.

They serve different purposes:

- `create_engine()` → creates the database connection manager
- `sessionmaker()` → creates database sessions for ORM operations

---

## 1. `create_engine()`

### Purpose

`create_engine()` is used to create an **Engine** object.

The Engine is responsible for:

- connecting to the database
- managing connection pooling
- handling SQL communication
- providing low-level database access

Think of the Engine as:

> "The database gateway"

---


### Common Parameters

#### `echo=True`

Print generated SQL queries.
Useful for debugging.

---

#### `pool_size`

Controls number of reusable connections.

---

## 2. `sessionmaker()`

### Purpose

`sessionmaker()` creates a factory for generating `Session` objects.

A Session is used to:

- add objects
- query data
- update rows
- delete rows
- manage transactions

Think of Session as:

> "A conversation with the database"

---

### Workflow

```text
create_engine()
       ↓
    Engine
       ↓
sessionmaker(bind=engine)
       ↓
   Session Factory
       ↓
     Session
```


### Engine vs Session

| Component | Purpose |
|---|---|
| Engine | Handles DB connections |
| Session | Handles ORM operations and transactions |

<br>

---

# `autoflush` vs `autocommit` in `sessionmaker()` (SQLAlchemy)

In SQLAlchemy, both `autoflush` and `autocommit` affect how a `Session` behaves, but they control **completely different things**.

---

## 1. `autoflush`

### What it does

`autoflush=True` means:

> Before executing a query, SQLAlchemy automatically sends pending changes (`INSERT`, `UPDATE`, `DELETE`) to the database using **flush**.

A **flush** does **NOT** commit the transaction.

It only synchronizes the in-memory session state with the database connection.

---

### Example

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine, autoflush=True)
session = Session()

user = User(name="John")
session.add(user)

# No commit yet

result = session.query(User).filter_by(name="John").first()
```

Because `autoflush=True`:

- SQLAlchemy automatically performs a `flush()`
- The `INSERT` is sent to the DB
- The query can now see `"John"`

But:

- the transaction is still uncommitted
- another database connection cannot see it yet

---

## 2. `autocommit`

### What it does

`autocommit=True` means:

> Each operation is automatically committed without requiring explicit `session.commit()`.

However:

- this mode is **deprecated**
- removed in newer SQLAlchemy versions
- modern SQLAlchemy uses explicit transaction management

---

### Old behavior example

```python
Session = sessionmaker(bind=engine, autocommit=True)
```

In old SQLAlchemy versions:

```python
session.execute("INSERT INTO users ...")
```

would commit automatically.

Without autocommit:

```python
session.commit()
```

is required.

---
## Conclusion

Flush = "send SQL now"

- sends SQL to DB
- keeps transaction open
- can still rollback

Commit = "make it permanent"

- permanently saves transaction
