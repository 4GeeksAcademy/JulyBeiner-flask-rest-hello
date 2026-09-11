"""Update Instagram data model

Revision ID: 328a368249f4
Revises: e2ac6069d4e0
Create Date: 2026-09-11 22:34:19.451872
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "328a368249f4"
down_revision = "e2ac6069d4e0"
branch_labels = None
depends_on = None


def upgrade():
    # Create Media table
    op.create_table(
        "media",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("url", sa.String(length=250), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["post.id"]),
        sa.PrimaryKeyConstraint("id")
    )

    # Update Comment table
    with op.batch_alter_table("comment", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("comment_text", sa.String(length=250), nullable=False)
        )
        batch_op.add_column(
            sa.Column("author_id", sa.Integer(), nullable=False)
        )

        batch_op.drop_constraint(
            "comment_user_id_fkey",
            type_="foreignkey"
        )

        batch_op.create_foreign_key(
            "comment_author_id_fkey",
            "user",
            ["author_id"],
            ["id"]
        )

        batch_op.drop_column("user_id")
        batch_op.drop_column("text")

    # Update Follower table
    with op.batch_alter_table("follower", schema=None) as batch_op:
        batch_op.drop_column("id")

        batch_op.create_primary_key(
            "pk_follower",
            ["user_from_id", "user_to_id"]
        )

    # Update Post table
    with op.batch_alter_table("post", schema=None) as batch_op:
        batch_op.drop_column("caption")
        batch_op.drop_column("image_url")

    # Update User table
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("firstname", sa.String(length=80), nullable=False)
        )
        batch_op.add_column(
            sa.Column("lastname", sa.String(length=80), nullable=False)
        )

        batch_op.drop_column("password")
        batch_op.drop_column("is_active")


def downgrade():
    # Restore User table
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "is_active",
                sa.Boolean(),
                nullable=False
            )
        )

        batch_op.add_column(
            sa.Column(
                "password",
                sa.String(length=80),
                nullable=False
            )
        )

        batch_op.drop_column("lastname")
        batch_op.drop_column("firstname")

    # Restore Post table
    with op.batch_alter_table("post", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "image_url",
                sa.String(length=250),
                nullable=False
            )
        )

        batch_op.add_column(
            sa.Column(
                "caption",
                sa.String(length=250),
                nullable=True
            )
        )

    # Restore Follower table
    with op.batch_alter_table("follower", schema=None) as batch_op:
        batch_op.drop_constraint(
            "pk_follower",
            type_="primary"
        )

        batch_op.add_column(
            sa.Column(
                "id",
                sa.Integer(),
                autoincrement=True,
                nullable=False
            )
        )

        batch_op.create_primary_key(
            "follower_pkey",
            ["id"]
        )

    # Restore Comment table
    with op.batch_alter_table("comment", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "text",
                sa.String(length=250),
                nullable=False
            )
        )

        batch_op.add_column(
            sa.Column(
                "user_id",
                sa.Integer(),
                nullable=False
            )
        )

        batch_op.drop_constraint(
            "comment_author_id_fkey",
            type_="foreignkey"
        )

        batch_op.create_foreign_key(
            "comment_user_id_fkey",
            "user",
            ["user_id"],
            ["id"]
        )

        batch_op.drop_column("author_id")
        batch_op.drop_column("comment_text")

    # Remove Media table
    op.drop_table("media")
