"""add user password hash

Revision ID: e252b6d3948d
Revises: 727564422356
Create Date: 2026-08-22 19:42:21.876872

"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash


# revision identifiers, used by Alembic.
revision = "e252b6d3948d"
down_revision = "727564422356"
branch_labels = None
depends_on = None


def upgrade():
    # Add the column temporarily as nullable so existing users
    # can be migrated safely.
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "password_hash",
                sa.String(length=255),
                nullable=True,
            )
        )

    # Set an initial password hash for existing users.
    # This password is temporary and must be changed after login.
    connection = op.get_bind()

    connection.execute(
        sa.text(
            """
            UPDATE users
            SET password_hash = :password_hash
            WHERE password_hash IS NULL
            """
        ),
        {
            "password_hash": generate_password_hash(
                "ChangeMe123!"
            )
        },
    )

    # Enforce the final NOT NULL constraint.
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column(
            "password_hash",
            existing_type=sa.String(length=255),
            nullable=False,
        )


def downgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("password_hash")
