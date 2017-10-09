import models
import peewee
from playhouse.migrate import migrate, PostgresqlMigrator


def forward ():
    models.DB.create_tables([models.Comment])
    comment = peewee.ForeignKeyField(
      models.comment, null=True, to_field=models.Comment.id)
    migrator = PostgresqlMigrator(models.DB)
    migrate(
      migrator.add_column('blogpost', 'comment_id'),
    )

if __name__ == '__main__':
    forward()
