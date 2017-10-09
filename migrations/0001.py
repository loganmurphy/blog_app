import models
import peewee
from playhouse.migrate import migrate, PostgresqlMigrator


def forward ():
    models.DB.create_tables([models.Author])
    author = peewee.ForeignKeyField(
      models.Author, null=True, to_field=models.Author.id)
    migrator = PostgresqlMigrator(models.DB)
    migrate(
      migrator.add_column('blogpost', 'author_id', author),
    )

if __name__ == '__main__':
    forward()
