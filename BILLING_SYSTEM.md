

# Billing System for AI Backlog Assistant

## Overview

This document describes the billing system implementation for the AI Backlog Assistant project. The system supports:

- **Tariff Plans**: Different subscription levels (Free, Pro, Team) with included limits
- **PAYG (Pay-As-You-Go)**: Charging for usage beyond included limits
- **Premium/Exclusive Features**: Access control for special features
- **Usage Tracking**: Detailed logging of feature usage
- **Balance Management**: Organization-level balance tracking

## Components

### 1. Database Models

The billing system uses SQLAlchemy models to store billing-related data:

- `TariffPlan`: Subscription plans with limits and discounts
- `OrganizationBalance`: Organization balances and tariff assignments
- `UsageLog`: Records of feature usage and charges
- `FeatureConfig`: Configuration of features, pricing, and access

### 2. BillingManager

Central service that handles all billing operations:

- `check_access()`: Verify feature access
- `get_price()`: Get feature pricing with discounts
- `check_limit()`: Check remaining usage limits
- `charge()`: Charge for feature usage (from limits or balance)
- `log_usage()`: Record usage events
- `get_balance()`: Get current balance
- `top_up()`: Add funds to balance

### 3. API Endpoints

REST API for billing management:

- `GET /api/v1/billing/balance`: Get organization balance
- `GET /api/v1/billing/usage`: Get usage history
- `GET /api/v1/billing/limits`: Get current limits
- `POST /api/v1/billing/topup`: Add funds to balance
- `GET /api/v1/billing/features`: Get available features

### 4. Integration

Billing is integrated through:

- **Decorators**: `@billing_required` decorator for agent methods
- **Middleware**: Billing checks in pipeline execution
- **Wrappers**: Billed versions of agents (e.g., `BilledCategorizationAgent`)

## Usage Example

### Basic Integration

```python
from web_server.billing_middleware import billing_required

class MyAgent:
    @billing_required("MyFeature", units=1)
    def process(self, data):
        # Agent logic here
        pass
```

### Checking Balance

```python
from web_server.billing_manager import BillingManager

balance = BillingManager.get_balance(organization_id)
print(f"Current balance: {balance} RUB")
```

### Charging for Usage

```python
from web_server.billing_manager import BillingManager

amount_charged = BillingManager.charge(
    organization_id=org_id,
    feature_name="CategorizationAgent",
    units=1,
    user_id=user_id
)
```

## Configuration

Billing configuration is defined in `config/billing_config.py`:

- `FEATURE_CONFIG`: Feature pricing and access settings
- `TARIFF_PLANS`: Subscription plans with limits and discounts

## Initialization

The system is initialized with default data using:

```bash
python web_server/init_billing.py
```

## Testing

A test script is available at `test_billing_system.py` to demonstrate the billing functionality.

## Future Enhancements

- Multi-currency support
- Automatic balance recharge
- Usage notifications
- Detailed analytics and reporting
- Integration with payment gateways

