"""Global database feature support policy.

Provides decorators to mark tests requiring specific feature support from the
target database.

External dialect test suites should subclass SuiteRequirements
to provide specific inclusion/exlusions.

"""

from . import exclusions

class Requirements(object):
    def __init__(self, db, config):
        self.db = db
        self.config = config


class SuiteRequirements(Requirements):

    @property
    def create_table(self):
        """target platform can emit basic CreateTable DDL."""

        return exclusions.open()

    @property
    def drop_table(self):
        """target platform can emit basic DropTable DDL."""

        return exclusions.open()

    @property
    def foreign_keys(self):
        """Target database must support foreign keys."""

        return exclusions.open()

    @property
    def self_referential_foreign_keys(self):
        """Target database must support self-referential foreign keys."""

        return exclusions.open()

    @property
    def foreign_key_ddl(self):
        """Target database must support the DDL phrases for FOREIGN KEY."""

        return exclusions.open()

    @property
    def named_constraints(self):
        """target database must support names for constraints."""

        return exclusions.open()

    @property
    def subqueries(self):
        """Target database must support subqueries."""

        return exclusions.open()

    @property
    def autoincrement_insert(self):
        """target platform generates new surrogate integer primary key values
        when insert() is executed, excluding the pk column."""

        return exclusions.open()

    @property
    def returning(self):
        """target platform supports RETURNING."""

        return exclusions.only_if(
                lambda: self.config.db.dialect.implicit_returning,
                "'returning' not supported by database"
            )

    @property
    def denormalized_names(self):
        """Target database must have 'denormalized', i.e.
        UPPERCASE as case insensitive names."""

        return exclusions.skip_if(
                    lambda: not self.db.dialect.requires_name_normalize,
                    "Backend does not require denormalized names."
                )

    @property
    def implements_get_lastrowid(self):
        """"target dialect implements the executioncontext.get_lastrowid()
        method without reliance on RETURNING.

        """
        return exclusions.open()

    @property
    def emulated_lastrowid(self):
        """"target dialect retrieves cursor.lastrowid, or fetches
        from a database-side function after an insert() construct executes,
        within the get_lastrowid() method.

        Only dialects that "pre-execute", or need RETURNING to get last
        inserted id, would return closed/fail/skip for this.

        """
        return exclusions.closed()

    @property
    def dbapi_lastrowid(self):
        """"target platform includes a 'lastrowid' accessor on the DBAPI
        cursor object.

        """
        return exclusions.closed()

    @property
    def views(self):
        """Target database must support VIEWs."""

        return exclusions.closed()

    @property
    def schemas(self):
        """Target database must support external schemas, and have one
        named 'test_schema'."""

        return exclusions.closed()

    @property
    def sequences(self):
        """Target database must support SEQUENCEs."""

        return exclusions.only_if([
                lambda: self.config.db.dialect.supports_sequences
            ], "no SEQUENCE support")

    @property
    def reflects_pk_names(self):
        return exclusions.closed()

    @property
    def table_reflection(self):
        return exclusions.open()

    @property
    def view_reflection(self):
        return self.views

    @property
    def schema_reflection(self):
        return self.schemas

    @property
    def primary_key_constraint_reflection(self):
        return exclusions.open()

    @property
    def foreign_key_constraint_reflection(self):
        return exclusions.open()

    @property
    def index_reflection(self):
        return exclusions.open()

    @property
    def unbounded_varchar(self):
        """Target database must support VARCHAR with no length"""

        return exclusions.open()

    @property
    def unicode_data(self):
        """Target database/dialect must support Python unicode objects with
        non-ASCII characters represented, delivered as bound parameters
        as well as in result rows.

        """
        return exclusions.open()

    @property
    def text_type(self):
        """Target database must support an unbounded Text() "
        "type such as TEXT or CLOB"""

        return exclusions.open()

    @property
    def empty_strings(self):
        """target database can persist/return an empty string."""

        return exclusions.open()


    @property
    def update_from(self):
        """Target must support UPDATE..FROM syntax"""
        return exclusions.closed()

    @property
    def update_where_target_in_subquery(self):
        """Target must support UPDATE where the same table is present in a
        subquery in the WHERE clause.

        This is an ANSI-standard syntax that apparently MySQL can't handle,
        such as:

        UPDATE documents SET flag=1 WHERE documents.title IN
            (SELECT max(documents.title) AS title
                FROM documents GROUP BY documents.user_id
            )
        """
        return exclusions.open()