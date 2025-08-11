import datetime
import os
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import inflect
from pathlib import Path

# Load environment variables
load_dotenv()

# Initialize inflection engine (for singular/plural conversions)
p = inflect.engine()

# Type mapping from PostgreSQL to Python types for SQLModel
PG_TO_PYTHON_TYPE_MAP = {
    'integer': 'int',
    'bigint': 'int',
    'smallint': 'int',
    'character varying': 'str',
    'varchar': 'str',
    'text': 'str',
    'boolean': 'bool',
    'timestamp': 'datetime.datetime',
    'timestamp with time zone': 'datetime.datetime',
    'timestamp without time zone': 'datetime.datetime',
    'date': 'datetime.date',
    'time': 'datetime.time',
    'numeric': 'float',
    'real': 'float',
    'double precision': 'float',
    'json': 'Dict[str, Any]',
    'jsonb': 'Dict[str, Any]',
    'uuid': 'UUID',
    'bytea': 'bytes',
    'array': 'List[Any]',
}


def fetch_schema_information():
    """
    Connect to PostgreSQL and fetch schema information directly from system tables
    """
    # Connection parameters from environment variables
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "your_database")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASSWORD", "password")

    # Define what schemas to include - exclude PostgreSQL system schemas
    exclude_schemas = ['pg_catalog', 'information_schema', 'pg_toast', 'pg_temp', 'pg_toast_temp']

    # Dictionary to store table information
    tables_info = {}

    # Connect to PostgreSQL
    conn_string = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASS}"

    with psycopg2.connect(conn_string) as conn:
        # Use RealDictCursor to get column names in results
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Query tables
            cursor.execute(
                """
                SELECT
                    t.table_schema,
                    t.table_name
                FROM
                    information_schema.tables t
                WHERE
                    t.table_type = 'BASE TABLE'
                    AND t.table_schema NOT IN %s
                    AND t.table_schema NOT LIKE 'pg\_%%'
                ORDER BY
                    t.table_schema, t.table_name
            """, (tuple(exclude_schemas), ))

            tables = cursor.fetchall()

            # For each table, get its columns
            for table in tables:
                schema_name = table['table_schema']
                table_name = table['table_name']
                full_table_name = f"{schema_name}.{table_name}"

                # Skip tables in excluded schemas
                if schema_name in exclude_schemas:
                    continue

                # Get columns for this table
                cursor.execute(
                    """
                    SELECT
                        c.column_name,
                        c.data_type,
                        c.udt_name,
                        c.character_maximum_length,
                        c.is_nullable,
                        c.column_default,
                        CASE
                            WHEN pk.column_name IS NOT NULL THEN TRUE
                            ELSE FALSE
                        END as is_primary_key
                    FROM
                        information_schema.columns c
                    LEFT JOIN (
                        SELECT
                            tc.table_schema, tc.table_name,
                            kcu.column_name
                        FROM
                            information_schema.table_constraints tc
                        JOIN
                            information_schema.key_column_usage kcu
                        ON
                            tc.constraint_name = kcu.constraint_name
                            AND tc.table_schema = kcu.table_schema
                        WHERE
                            tc.constraint_type = 'PRIMARY KEY'
                    ) pk
                    ON
                        c.table_schema = pk.table_schema
                        AND c.table_name = pk.table_name
                        AND c.column_name = pk.column_name
                    WHERE
                        c.table_schema = %s
                        AND c.table_name = %s
                    ORDER BY
                        c.ordinal_position
                """, (schema_name, table_name))

                columns = cursor.fetchall()

                # Store the table information
                if table_name not in tables_info:
                    tables_info[table_name] = {
                        'schema': schema_name,
                        'columns': {},
                        'primary_keys': []
                    }

                # Process column information
                for col in columns:
                    col_name = col['column_name']
                    is_primary_key = col['is_primary_key']

                    # Determine the correct data type
                    data_type = col['data_type']
                    if data_type == 'USER-DEFINED':
                        data_type = col['udt_name']    # Use UDT name for custom types

                    # Check if it's an array type
                    if data_type.startswith('_'):
                        # PostgreSQL internally represents arrays with _ prefix
                        base_type = data_type[1:]    # Remove _ to get base type
                        data_type = f"array"

                    tables_info[table_name]['columns'][col_name] = {
                        'type': data_type,
                        'length': col['character_maximum_length'],
                        'nullable': col['is_nullable'] == 'YES',
                        'default': col['column_default'],
                        'primary_key': is_primary_key
                    }

                    # Add to primary keys list if applicable
                    if is_primary_key:
                        tables_info[table_name]['primary_keys'].append(col_name)

    return tables_info


def generate_sqlmodel_models(tables_info: Dict[str, Dict[str, Any]],
                             output_file: str = "sqlmodel_models.py"):
    """
    Generate SQLModel classes based on the database schema
    """
    # List of SQLModel reserved attribute names that should be renamed
    sqlmodel_reserved_attrs = [
        "schema", "metadata", "registry", "table", "__tablename__", "__table_args__",
        "model_config", "model_fields"
    ]

    with open(output_file, 'w') as f:
        # Add imports
        f.write("# SQLModel models generated from database schema\n\n")
        f.write("from typing import Optional, List, Dict, Any\n")
        f.write("from sqlmodel import Field, SQLModel, Relationship\n")
        f.write("import datetime\n")
        f.write("from uuid import UUID\n\n")

        # Add a type utility for Pylance
        f.write("# Class decorator to fix type checking issues\n")
        f.write("def table_class(cls):\n")
        f.write(
            "    \"\"\"Decorator to mark a class as a SQLModel table with proper type annotations\"\"\"\n"
        )
        f.write(
            "    setattr(cls, '__annotations__', {**getattr(cls, '__annotations__', {}), '__tablename__': str})\n"
        )
        f.write("    setattr(cls, 'model_config', {\"table\": True})\n")
        f.write("    return cls\n\n")

        # Process each table
        for table_name, table_info in tables_info.items():
            # Convert to PascalCase for class name (singular form)
            singular = p.singular_noun(table_name)
            if not singular:    # If already singular
                singular = table_name
            class_name = ''.join(word.capitalize() for word in singular.split('_'))

            # Create table model with proper type annotations
            f.write(f"@table_class\n")
            f.write(f"class {class_name}(SQLModel, table=True):\n")
            f.write(f"    \"\"\"SQLModel class for {table_name} table\"\"\"\n")
            f.write(f"    __tablename__ = \"{table_name}\"\n")

            if table_info['schema'] != 'public':
                f.write(f"    __table_args__ = {{'schema': '{table_info['schema']}'}}\n\n")
            else:
                f.write("\n")

            # Add columns
            for col_name, col_info in table_info['columns'].items():
                # Check if column name is a reserved attribute in SQLModel
                field_name = col_name
                if col_name in sqlmodel_reserved_attrs:
                    # Add comment about renaming to avoid shadowing
                    f.write(
                        f"    # Renamed field '{col_name}' to avoid shadowing SQLModel attribute\n"
                    )
                    # Rename field in Python but keep original DB column name
                    field_name = f"{col_name}_field"

                # Determine Python type
                pg_type = col_info['type']
                py_type = PG_TO_PYTHON_TYPE_MAP.get(pg_type, "str")

                # Make nullable fields Optional unless it's a primary key with default
                is_nullable = col_info['nullable'] and not col_info['primary_key']
                if is_nullable:
                    py_type = f"Optional[{py_type}]"

                # Build field definition
                f.write(f"    {field_name}: {py_type} = Field(\n")

                # If field was renamed, add column name parameter
                if field_name != col_name:
                    f.write(f"        sa_column_kwargs={{'name': '{col_name}'}},\n")

                # Add primary key info
                if col_info['primary_key']:
                    f.write("        primary_key=True,\n")

                    # Auto-increment primary key (if default contains nextval or serial)
                    default = col_info.get('default', '')
                    if default and isinstance(default, str):
                        if 'nextval' in default or (col_info['type']
                                                    and 'serial' in str(col_info['type']).lower()):
                            f.write("        default=None,\n")

                # Add nullable constraint
                if not is_nullable and not col_info['primary_key']:
                    f.write("        nullable=False,\n")

                # Add specific length for strings
                if col_info['length'] is not None and pg_type in ('character varying', 'varchar'):
                    f.write(f"        max_length={col_info['length']},\n")

                # Add default if present and not auto-increment
                default_value = col_info.get('default')
                if default_value and isinstance(default_value, str):
                    # Check for auto-increment before processing default
                    is_auto_increment = 'nextval' in default_value or (
                        col_info['type'] and 'serial' in str(col_info['type']).lower())

                    if not is_auto_increment:
                        # Clean up the default value to be Python compatible
                        if default_value.startswith("'") and default_value.endswith("'"):
                            # String literal
                            default_value = default_value.strip("'")
                            f.write(f"        default=\"{default_value}\",\n")
                        elif default_value.lower() == 'true':
                            f.write(f"        default=True,\n")
                        elif default_value.lower() == 'false':
                            f.write(f"        default=False,\n")
                        elif default_value.lower() in ('now()', 'current_timestamp'):
                            f.write(f"        default=datetime.datetime.now,\n")
                        else:
                            # Try to keep as is for numeric values, etc.
                            f.write(f"        default={default_value},\n")

                f.write("    )\n")

            # Add empty line between classes
            f.write("\n\n")

        # Now create Pydantic models for API operations
        f.write("\n# API models for request/response operations\n\n")

        for table_name, table_info in tables_info.items():
            singular = p.singular_noun(table_name) or table_name
            class_name = ''.join(word.capitalize() for word in singular.split('_'))

            # Create model for creation (omitting auto-generated primary keys)
            f.write(f"class {class_name}Create(SQLModel):\n")
            for col_name, col_info in table_info['columns'].items():
                # Check if column name needs renaming
                field_name = col_name
                if col_name in sqlmodel_reserved_attrs:
                    field_name = f"{col_name}_field"
                    f.write(
                        f"    # Renamed field '{col_name}' to avoid shadowing SQLModel attribute\n"
                    )

                # Skip auto-increment primary keys for creation
                default = col_info.get('default', '')
                is_auto_increment = False

                if isinstance(default, str) and 'nextval' in default:
                    is_auto_increment = True
                elif col_info['type'] and isinstance(col_info['type'],
                                                     str) and 'serial' in col_info['type'].lower():
                    is_auto_increment = True

                if col_info['primary_key'] and is_auto_increment:
                    continue

                # Determine Python type
                pg_type = col_info['type']
                py_type = PG_TO_PYTHON_TYPE_MAP.get(pg_type, "str")

                # Make nullable fields Optional
                if col_info['nullable']:
                    py_type = f"Optional[{py_type}]"

                # Build field definition
                field_def = f"    {field_name}: {py_type}"

                # Add defaults
                if col_info['nullable']:
                    field_def += " = None"

                f.write(f"{field_def}\n")

            f.write("\n\n")

            # Create model for response (including all fields)
            f.write(f"class {class_name}Read(SQLModel):\n")
            for col_name, col_info in table_info['columns'].items():
                # Check if column name needs renaming
                field_name = col_name
                if col_name in sqlmodel_reserved_attrs:
                    field_name = f"{col_name}_field"
                    f.write(
                        f"    # Renamed field '{col_name}' to avoid shadowing SQLModel attribute\n"
                    )

                # Determine Python type
                pg_type = col_info['type']
                py_type = PG_TO_PYTHON_TYPE_MAP.get(pg_type, "str")

                # Build field definition
                field_def = f"    {field_name}: {py_type}"

                f.write(f"{field_def}\n")

            f.write("\n\n")

            # Create model for update (all fields optional)
            f.write(f"class {class_name}Update(SQLModel):\n")
            for col_name, col_info in table_info['columns'].items():
                # Skip primary keys for update
                if col_info['primary_key']:
                    continue

                # Check if column name needs renaming
                field_name = col_name
                if col_name in sqlmodel_reserved_attrs:
                    field_name = f"{col_name}_field"
                    f.write(
                        f"    # Renamed field '{col_name}' to avoid shadowing SQLModel attribute\n"
                    )

                # Determine Python type
                pg_type = col_info['type']
                py_type = PG_TO_PYTHON_TYPE_MAP.get(pg_type, "str")

                # All fields optional for update
                py_type = f"Optional[{py_type}]"

                # Build field definition
                field_def = f"    {field_name}: {py_type} = None"

                f.write(f"{field_def}\n")

            f.write("\n\n")

    print(f"SQLModel models generated successfully to {output_file}")
    return output_file


def generate_fastapi_crud_routes(tables_info: Dict[str, Dict[str, Any]], output_dir: str = "app"):
    """
    Generate FastAPI CRUD route files for each table with improved project structure
    that avoids circular imports by using a separate database module
    """
    # List of SQLModel reserved attribute names that should be renamed
    sqlmodel_reserved_attrs = [
        "schema", "metadata", "registry", "table", "__tablename__", "__table_args__",
        "model_config", "model_fields"
    ]

    # Create the output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path(f"{output_dir}/routers").mkdir(parents=True, exist_ok=True)

    # Create __init__.py files
    Path(f"{output_dir}/__init__.py").touch()
    Path(f"{output_dir}/routers/__init__.py").touch()

    # Generate database.py file for shared database functionality
    with open(f"{output_dir}/database.py", "w") as f:
        f.write("# Database connection and session management\n")
        f.write("from sqlmodel import SQLModel, create_engine, Session\n")
        f.write("import os\n")
        f.write("from dotenv import load_dotenv\n\n")

        f.write("# Load environment variables\n")
        f.write("load_dotenv()\n\n")

        # Database connection setup
        f.write("# Database connection\n")
        f.write("DB_HOST = os.getenv(\"DB_HOST\", \"localhost\")\n")
        f.write("DB_PORT = os.getenv(\"DB_PORT\", \"5432\")\n")
        f.write("DB_NAME = os.getenv(\"DB_NAME\", \"your_database\")\n")
        f.write("DB_USER = os.getenv(\"DB_USER\", \"postgres\")\n")
        f.write("DB_PASS = os.getenv(\"DB_PASSWORD\", \"password\")\n\n")

        f.write("# SQLAlchemy connection string\n")
        f.write(
            "DATABASE_URL = f\"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}\"\n\n"
        )

        f.write("# Create SQLAlchemy engine\n")
        f.write("engine = create_engine(DATABASE_URL)\n\n")

        f.write("# Dependency for database session\n")
        f.write("def get_session():\n")
        f.write("    with Session(engine) as session:\n")
        f.write("        yield session\n")

    # Generate main FastAPI app file
    with open(f"{output_dir}/main.py", "w") as f:
        f.write("# Main FastAPI application\n")
        f.write("from fastapi import FastAPI\n")
        f.write("from sqlmodel import SQLModel\n\n")

        # Import all router modules
        for table_name in tables_info.keys():
            snake_case = table_name.lower()
            f.write(f"from .routers import {snake_case}\n")

        f.write("\n# Create FastAPI app\n")
        f.write("app = FastAPI(\n")
        f.write("    title=\"Generated API\",\n")
        f.write("    description=\"API automatically generated from database schema\",\n")
        f.write("    version=\"1.0.0\",\n")
        f.write(")\n\n")

        # Include routers
        f.write("# Include routers\n")
        for table_name in tables_info.keys():
            snake_case = table_name.lower()
            f.write(f"app.include_router({snake_case}.router)\n")

    # Generate router files for each table
    for table_name, table_info in tables_info.items():
        # Convert to snake_case for file names
        snake_case = table_name.lower()
        singular = p.singular_noun(table_name) or table_name
        class_name = ''.join(word.capitalize() for word in singular.split('_'))

        with open(f"{output_dir}/routers/{snake_case}.py", "w") as f:
            # Imports
            f.write("from fastapi import APIRouter, Depends, HTTPException, Query, status\n")
            f.write("from sqlmodel import Session, select\n")
            f.write("from typing import List, Optional\n\n")
            f.write("# Import from database module instead of main to avoid circular imports\n")
            f.write("from ..database import get_session\n")
            f.write(
                f"from ..models import {class_name}, {class_name}Create, {class_name}Read, {class_name}Update\n\n"
            )

            # Create router
            f.write(f"router = APIRouter(prefix=\"/{snake_case}\", tags=[\"{snake_case}\"])\n\n")

            # Find primary key column
            pk_column = next(iter(table_info['primary_keys']), None)
            pk_type = None

            if pk_column:
                pk_type = PG_TO_PYTHON_TYPE_MAP.get(table_info['columns'][pk_column]['type'],
                                                    "str")
                if pk_type == "UUID":
                    pk_type = "UUID"
                elif pk_type == "int":
                    pk_type = "int"
                else:
                    pk_type = "str"

                # Check if primary key column name needs renaming in Python
                pk_field_name = pk_column
                if pk_column in sqlmodel_reserved_attrs:
                    pk_field_name = f"{pk_column}_field"

            # Create CRUD endpoints
            # GET all
            f.write(f"@router.get(\"/\", response_model=List[{class_name}Read])\n")
            f.write(f"def read_all_{snake_case}(*, session: Session = Depends(get_session),\n")
            f.write(
                f"                     offset: int = 0, limit: int = Query(default=100, lte=100)):\n"
            )
            f.write(f"    \"\"\"\n")
            f.write(f"    Get all {table_name} with pagination\n")
            f.write(f"    \"\"\"\n")
            f.write(
                f"    {snake_case} = session.exec(select({class_name}).offset(offset).limit(limit)).all()\n"
            )
            f.write(f"    return {snake_case}\n\n")

            # GET one
            if pk_column:
                # Use original column name in URL path parameter
                f.write(f"@router.get(\"/{{{pk_column}}}\", response_model={class_name}Read)\n")
                f.write(f"def read_one_{singular}(*, \n")
                f.write(f"                    session: Session = Depends(get_session),\n")
                # Use original column name in function parameter
                f.write(f"                    {pk_column}: {pk_type}):\n")
                f.write(f"    \"\"\"\n")
                f.write(f"    Get a specific {singular} by {pk_column}\n")
                f.write(f"    \"\"\"\n")
                # Use the appropriate field name when accessing the model
                if pk_column in sqlmodel_reserved_attrs:
                    # Add comment about field name change
                    f.write(
                        f"    # Note: '{pk_column}' is renamed to '{pk_field_name}' in the model\n"
                    )
                    # Use a dictionary to set the primary key when it's renamed
                    f.write(
                        f"    {singular} = session.get({class_name}, {{{pk_field_name!r}: {pk_column}}})\n"
                    )
                else:
                    # Use the parameter directly when field name is unchanged
                    f.write(f"    {singular} = session.get({class_name}, {pk_column})\n")

                f.write(f"    if not {singular}:\n")
                f.write(
                    f"        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"{singular.capitalize()} not found\")\n"
                )
                f.write(f"    return {singular}\n\n")

            # POST create
            f.write(
                f"@router.post(\"/\", response_model={class_name}Read, status_code=status.HTTP_201_CREATED)\n"
            )
            f.write(f"def create_{singular}(*, \n")
            f.write(f"                  session: Session = Depends(get_session),\n")
            f.write(f"                  {singular}: {class_name}Create):\n")
            f.write(f"    \"\"\"\n")
            f.write(f"    Create a new {singular}\n")
            f.write(f"    \"\"\"\n")
            f.write(f"    db_{singular} = {class_name}.from_orm({singular})\n")
            f.write(f"    session.add(db_{singular})\n")
            f.write(f"    session.commit()\n")
            f.write(f"    session.refresh(db_{singular})\n")
            f.write(f"    return db_{singular}\n\n")

            # PUT update
            if pk_column:
                # Use original column name in URL path parameter
                f.write(f"@router.put(\"/{{{pk_column}}}\", response_model={class_name}Read)\n")
                f.write(f"def update_{singular}(*, \n")
                f.write(f"                  session: Session = Depends(get_session),\n")
                # Use original column name in function parameter
                f.write(f"                  {pk_column}: {pk_type},\n")
                f.write(f"                  {singular}: {class_name}Update):\n")
                f.write(f"    \"\"\"\n")
                f.write(f"    Update a {singular}\n")
                f.write(f"    \"\"\"\n")
                # Use the appropriate field name when accessing the model
                if pk_column in sqlmodel_reserved_attrs:
                    # Add comment about field name change
                    f.write(
                        f"    # Note: '{pk_column}' is renamed to '{pk_field_name}' in the model\n"
                    )
                    # Use a dictionary to find by the primary key when it's renamed
                    f.write(
                        f"    db_{singular} = session.get({class_name}, {{{pk_field_name!r}: {pk_column}}})\n"
                    )
                else:
                    # Use the parameter directly when field name is unchanged
                    f.write(f"    db_{singular} = session.get({class_name}, {pk_column})\n")

                f.write(f"    if not db_{singular}:\n")
                f.write(
                    f"        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"{singular.capitalize()} not found\")\n"
                )
                f.write(f"    \n")
                f.write(f"    # Update model with provided fields\n")
                f.write(f"    {singular}_data = {singular}.dict(exclude_unset=True)\n")
                f.write(f"    for key, value in {singular}_data.items():\n")
                f.write(f"        setattr(db_{singular}, key, value)\n")
                f.write(f"    \n")
                f.write(f"    session.add(db_{singular})\n")
                f.write(f"    session.commit()\n")
                f.write(f"    session.refresh(db_{singular})\n")
                f.write(f"    return db_{singular}\n\n")

                # DELETE
                # Use original column name in URL path parameter
                f.write(
                    f"@router.delete(\"/{{{pk_column}}}\", status_code=status.HTTP_204_NO_CONTENT)\n"
                )
                f.write(f"def delete_{singular}(*, \n")
                f.write(f"                  session: Session = Depends(get_session),\n")
                # Use original column name in function parameter
                f.write(f"                  {pk_column}: {pk_type}):\n")
                f.write(f"    \"\"\"\n")
                f.write(f"    Delete a {singular}\n")
                f.write(f"    \"\"\"\n")
                # Use the appropriate field name when accessing the model
                if pk_column in sqlmodel_reserved_attrs:
                    # Add comment about field name change
                    f.write(
                        f"    # Note: '{pk_column}' is renamed to '{pk_field_name}' in the model\n"
                    )
                    # Use a dictionary to find by the primary key when it's renamed
                    f.write(
                        f"    {singular} = session.get({class_name}, {{{pk_field_name!r}: {pk_column}}})\n"
                    )
                else:
                    # Use the parameter directly when field name is unchanged
                    f.write(f"    {singular} = session.get({class_name}, {pk_column})\n")

                f.write(f"    if not {singular}:\n")
                f.write(
                    f"        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"{singular.capitalize()} not found\")\n"
                )
                f.write(f"    \n")
                f.write(f"    session.delete({singular})\n")
                f.write(f"    session.commit()\n")
                f.write(f"    return None\n")

    # Generate a simple README.md with instructions
    with open(f"{output_dir}/README.md", "w") as f:
        f.write("# Generated FastAPI Application\n\n")
        f.write("This FastAPI application was auto-generated from your database schema.\n\n")
        f.write("## Project Structure\n\n")
        f.write("```\n")
        f.write("app/\n")
        f.write("├── __init__.py\n")
        f.write("├── database.py     # Database connection and session management\n")
        f.write("├── main.py         # FastAPI application and router registration\n")
        f.write("├── models.py       # SQLModel models\n")
        f.write("├── routers/\n")
        f.write("    ├── __init__.py\n")
        for table_name in tables_info.keys():
            snake_case = table_name.lower()
            f.write(f"    ├── {snake_case}.py\n")
        f.write("```\n\n")
        f.write("## Running the Application\n\n")
        f.write("```bash\n")
        f.write("# Install dependencies\n")
        f.write("pip install fastapi sqlmodel uvicorn python-dotenv\n\n")
        f.write("# Run the server\n")
        f.write("uvicorn app.main:app --reload\n")
        f.write("```\n\n")
        f.write("## API Documentation\n\n")
        f.write("Once running, access:\n")
        f.write("- Swagger UI: http://127.0.0.1:8000/docs\n")
        f.write("- ReDoc: http://127.0.0.1:8000/redoc\n")

    print(f"FastAPI CRUD routes generated successfully in {output_dir}/ with improved structure")


def generate_sql_setup_script(tables_info: Dict[str, Dict[str, Any]],
                              output_file: str = "setup_database.sql"):
    """
    Generate a complete SQL setup script to recreate the database schema
    including foreign keys, indexes, and other constraints
    """
    # First, connect to database to get additional schema information
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "your_database")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASSWORD", "password")

    conn_string = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASS}"

    # Dictionary to store foreign key relationships
    foreign_keys = {}
    # Dictionary to store indexes
    indexes = {}

    with psycopg2.connect(conn_string) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            # Get foreign key constraints
            cursor.execute("""
                SELECT
                    tc.table_schema as schema_name,
                    tc.table_name,
                    kcu.column_name,
                    ccu.table_schema AS foreign_table_schema,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name,
                    tc.constraint_name
                FROM
                    information_schema.table_constraints AS tc
                JOIN
                    information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                JOIN
                    information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                WHERE
                    tc.constraint_type = 'FOREIGN KEY'
                ORDER BY
                    tc.table_schema,
                    tc.table_name,
                    kcu.position_in_unique_constraint;
            """)

            for fk in cursor.fetchall():
                schema = fk['schema_name']
                table = fk['table_name']
                key = f"{schema}.{table}" if schema != 'public' else table

                if key not in foreign_keys:
                    foreign_keys[key] = []

                foreign_keys[key].append({
                    'column': fk['column_name'],
                    'foreign_schema': fk['foreign_table_schema'],
                    'foreign_table': fk['foreign_table_name'],
                    'foreign_column': fk['foreign_column_name'],
                    'constraint_name': fk['constraint_name']
                })

            # Get indexes (excluding those for primary keys and unique constraints)
            cursor.execute("""
                SELECT
                    schemaname as schema_name,
                    tablename as table_name,
                    indexname as index_name,
                    indexdef as index_def
                FROM
                    pg_indexes
                WHERE
                    indexname NOT LIKE '%_pkey'
                    AND indexname NOT LIKE '%_key'
                ORDER BY
                    schemaname, tablename, indexname;
            """)

            for idx in cursor.fetchall():
                schema = idx['schema_name']
                table = idx['table_name']
                key = f"{schema}.{table}" if schema != 'public' else table

                if key not in indexes:
                    indexes[key] = []

                indexes[key].append({'name': idx['index_name'], 'definition': idx['index_def']})

    # Now generate the SQL script
    with open(output_file, 'w') as f:
        # File header
        f.write("-- Database setup script generated from schema information\n")
        f.write("-- Generated on: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("-- This script creates all tables, constraints, and indexes\n\n")

        # Create schemas
        schemas = set(table_info['schema'] for table_info in tables_info.values())
        schemas.discard('public')    # public schema exists by default

        if schemas:
            f.write("-- Create custom schemas\n")
            for schema in schemas:
                f.write(f"CREATE SCHEMA IF NOT EXISTS {schema};\n")
            f.write("\n")

        # Create tables
        f.write("-- Create tables\n")
        for table_name, table_info in tables_info.items():
            schema = table_info['schema']
            qualified_table = f"{schema}.{table_name}" if schema != 'public' else table_name

            f.write(f"CREATE TABLE IF NOT EXISTS {qualified_table} (\n")

            # Define columns
            column_defs = []

            for col_name, col_info in table_info['columns'].items():
                # Build column definition
                col_type = col_info['type']

                # Add length specification for character types if present
                if col_info['length'] is not None and col_type in ('character varying', 'varchar'):
                    col_type = f"{col_type}({col_info['length']})"

                # Start with column name and type
                col_def = f"    {col_name} {col_type}"

                # Add NOT NULL constraint if applicable
                if not col_info['nullable']:
                    col_def += " NOT NULL"

                # Add default value if present
                if col_info.get('default') is not None:
                    col_def += f" DEFAULT {col_info['default']}"

                column_defs.append(col_def)

            # Add primary key constraint
            if table_info['primary_keys']:
                pk_constraint = f"    PRIMARY KEY ({', '.join(table_info['primary_keys'])})"
                column_defs.append(pk_constraint)

            # Join all column definitions
            f.write(',\n'.join(column_defs))
            f.write("\n);\n\n")

        # Add foreign key constraints
        if foreign_keys:
            f.write("-- Add foreign key constraints\n")
            for qualified_table, fks in foreign_keys.items():
                for fk in fks:
                    foreign_schema = fk['foreign_schema']
                    foreign_table = fk['foreign_table']
                    qualified_foreign_table = f"{foreign_schema}.{foreign_table}" if foreign_schema != 'public' else foreign_table

                    f.write(
                        f"ALTER TABLE {qualified_table} ADD CONSTRAINT {fk['constraint_name']} ")
                    f.write(
                        f"FOREIGN KEY ({fk['column']}) REFERENCES {qualified_foreign_table} ({fk['foreign_column']});\n"
                    )
            f.write("\n")

        # Add indexes
        if indexes:
            f.write("-- Create indexes\n")
            for qualified_table, idxs in indexes.items():
                for idx in idxs:
                    # Just use the full index definition from PostgreSQL
                    f.write(f"{idx['definition']};\n")
            f.write("\n")

        f.write("-- End of setup script\n")

    print(f"Comprehensive SQL setup script generated at {output_file}")
    return output_file


def main():
    """Generate SQLModel models and FastAPI CRUD routes from database schema"""
    print("Fetching database schema information...")
    tables_info = fetch_schema_information()

    print(f"Found {len(tables_info)} tables in the database.")

    # Generate SQLModel models but save directly to app/models.py
    output_dir = "app"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    models_file = generate_sqlmodel_models(tables_info, f"{output_dir}/models.py")

    # Generate FastAPI CRUD routes
    generate_fastapi_crud_routes(tables_info, output_dir)

    # Generate SQL setup script
    generate_sql_setup_script(tables_info)

    print("✅ Generated complete FastAPI application with SQLModel models and CRUD routes")
    print("\nTo run your generated FastAPI application:")
    print("1. Install dependencies: pip install fastapi sqlmodel uvicorn python-dotenv")
    print("2. Run the server: uvicorn app.main:app --reload")
    print("3. Visit the API docs: http://127.0.0.1:8000/docs")


if __name__ == "__main__":
    main()
