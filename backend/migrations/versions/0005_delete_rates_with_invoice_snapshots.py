"""Allow deleting rates while retaining invoice snapshots.

Revision ID: 0005_rate_delete_snapshots
Revises: 0004_invoice_due_dates
"""

from alembic import op
import sqlalchemy as sa


revision = "0005_rate_delete_snapshots"
down_revision = "0004_invoice_due_dates"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    if bind.dialect.name == "sqlite":
        convention = {
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
        }
        with op.batch_alter_table("invoices", naming_convention=convention) as batch_op:
            batch_op.drop_constraint("fk_invoices_rate_id_fuel_rates", type_="foreignkey")
            batch_op.alter_column("rate_id", existing_type=sa.Integer(), nullable=True)
            batch_op.create_foreign_key(
                "fk_invoices_rate_id_fuel_rates",
                "fuel_rates",
                ["rate_id"],
                ["id"],
                ondelete="SET NULL",
            )
    else:
        op.drop_constraint("invoices_rate_id_fkey", "invoices", type_="foreignkey")
        op.alter_column("invoices", "rate_id", existing_type=sa.Integer(), nullable=True)
        op.create_foreign_key(
            "invoices_rate_id_fkey",
            "invoices",
            "fuel_rates",
            ["rate_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade():
    bind = op.get_bind()
    if bind.dialect.name == "sqlite":
        convention = {
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
        }
        with op.batch_alter_table("invoices", naming_convention=convention) as batch_op:
            batch_op.drop_constraint("fk_invoices_rate_id_fuel_rates", type_="foreignkey")
            batch_op.alter_column("rate_id", existing_type=sa.Integer(), nullable=False)
            batch_op.create_foreign_key(
                "fk_invoices_rate_id_fuel_rates",
                "fuel_rates",
                ["rate_id"],
                ["id"],
                ondelete="RESTRICT",
            )
    else:
        op.drop_constraint("invoices_rate_id_fkey", "invoices", type_="foreignkey")
        op.alter_column("invoices", "rate_id", existing_type=sa.Integer(), nullable=False)
        op.create_foreign_key(
            "invoices_rate_id_fkey",
            "invoices",
            "fuel_rates",
            ["rate_id"],
            ["id"],
            ondelete="RESTRICT",
        )
