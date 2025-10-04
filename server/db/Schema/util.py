# Assuming db.Schema contains the SQLAlchemy declarative Base and all models
import db.Schema as Schema

# Get the Base class from the imported schema module
# CRITICAL: All models must be imported and defined in db.Schema
# *before* this module is imported, so that Base.metadata.tables is populated.
Base = Schema.Base

# The dynamic map is built once when the module is imported.
# It maps the string table name (e.g., "users") to its ORM class (User).
_MODEL_MAP = {}
try:
    # FIX: Use Base.registry.mappers to correctly access the mapped classes in SQLAlchemy 2.0+
    # The 'class_for_table' method is not directly available on the registry.
    for mapper in Base.registry.mappers:
        # Ensure the mapper has a local table defined
        if mapper.local_table is not None:
            # Map the table name string to the actual ORM class
            _MODEL_MAP[mapper.local_table.name] = mapper.class_

except AttributeError:
    # This block is defensive, catching cases where Base might not be fully ready.
    print("WARNING: SQLAlchemy Base registry not fully available during import.")


def get_record_factory(table_name):
    """
    Dynamically maps a database table name string to its corresponding
    SQLAlchemy ORM class (e.g., "users" -> User).

    This replaces the need to manually maintain a dictionary mapping.

    Args:
        table_name (str): The name of the table to look up.

    Returns:
        SQLAlchemy Base Class: The ORM class for the given table.
    """
    if table_name not in _MODEL_MAP:
        # Attempt to rebuild map if empty, just in case models were defined late
        if not _MODEL_MAP:
            # Rebuild logic using the fixed mapper iteration
            try:
                for mapper in Base.registry.mappers:
                    if mapper.local_table is not None:
                        _MODEL_MAP[mapper.local_table.name] = mapper.class_

                if table_name in _MODEL_MAP:
                    return _MODEL_MAP[table_name]
            except AttributeError:
                # If rebuilding fails, continue to raise the ValueError
                pass

        raise ValueError(f"Table name '{table_name}' not found in ORM registry.")

    return _MODEL_MAP[table_name]
