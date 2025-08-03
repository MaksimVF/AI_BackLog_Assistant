




















#!/usr/bin/env python3

"""
Check database directly
"""

from web_server.app import app, db
from web_server.billing_models import OrganizationBalance, TariffPlan

def check_db():
    """Check database directly."""
    with app.app_context():
        # Get all organization balances
        org_balances = OrganizationBalance.query.all()
        for org_balance in org_balances:
            print(f"Org ID: {org_balance.organization_id}")
            print(f"Balance: {org_balance.balance_rub}")
            print(f"Team members: {org_balance.team_members}")
            print(f"Tariff plan ID: {org_balance.tariff_plan_id}")
            print("---")

        # Get all tariff plans
        tariff_plans = TariffPlan.query.all()
        for tariff in tariff_plans:
            print(f"Tariff ID: {tariff.id}")
            print(f"Name: {tariff.name}")
            print(f"Max team members: {tariff.max_team_members}")
            print(f"Member price: {tariff.member_price}")
            print("---")

if __name__ == "__main__":
    check_db()






















