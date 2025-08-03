


"""
Billing System Initialization Script

This script initializes the billing system with default tariff plans and feature configurations.
"""

import uuid
from .app import app, db
from .billing_models import TariffPlan, FeatureConfig
from config.billing_config import TARIFF_PLANS, FEATURE_CONFIG

def init_billing_system():
    """Initialize the billing system with default data."""
    with app.app_context():
        print("Initializing billing system...")

        # Create tariff plans
        for plan_name, plan_data in TARIFF_PLANS.items():
            existing_plan = TariffPlan.query.filter_by(name=plan_name).first()
            if not existing_plan:
                tariff_plan = TariffPlan(
                    id=str(uuid.uuid4()),
                    name=plan_name,
                    price_per_month=plan_data['price_per_month'],
                    included_limits=plan_data['included_limits'],
                    discounts=plan_data['discounts'],
                    access_features=plan_data['access_features']
                )
                db.session.add(tariff_plan)
                print(f"Created tariff plan: {plan_name}")
            else:
                print(f"Tariff plan already exists: {plan_name}")

        # Create feature configurations
        for feature_name, feature_data in FEATURE_CONFIG.items():
            existing_feature = FeatureConfig.query.filter_by(feature_name=feature_name).first()
            if not existing_feature:
                feature_config = FeatureConfig(
                    feature_name=feature_name,
                    feature_type=feature_data['type'],
                    unit=feature_data['unit'],
                    price_per_unit=feature_data['price'],
                    access_tariffs=feature_data.get('access', []),
                    description=feature_data.get('description', '')
                )
                db.session.add(feature_config)
                print(f"Created feature config: {feature_name}")
            else:
                print(f"Feature config already exists: {feature_name}")

        db.session.commit()
        print("Billing system initialization complete!")

if __name__ == "__main__":
    init_billing_system()

