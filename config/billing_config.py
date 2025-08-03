

"""
Billing Configuration for AI Backlog Assistant

Default feature pricing and tariff plans configuration.
"""

# Feature configuration
FEATURE_CONFIG = {
    "CategorizationAgent": {
        "type": "basic",
        "unit": "call",
        "price": 1.0,
        "description": "Document categorization service"
    },
    "SmartSummaryAgent": {
        "type": "premium",
        "unit": "call",
        "price": 5.0,
        "description": "Advanced document summarization"
    },
    "CodeRefactorAgent": {
        "type": "exclusive",
        "unit": "call",
        "price": 10.0,
        "access": ["Team"],
        "description": "Exclusive code refactoring service"
    },
    "ReflectionAgent": {
        "type": "basic",
        "unit": "call",
        "price": 2.0,
        "description": "Reflection and analysis service"
    },
    "Audio2Text": {
        "type": "basic",
        "unit": "minute",
        "price": 0.5,
        "description": "Audio transcription service"
    },
    "VisualizationAgent": {
        "type": "premium",
        "unit": "call",
        "price": 3.0,
        "description": "Data visualization service"
    }
}

# Tariff plans configuration
TARIFF_PLANS = {
    "Free": {
        "price_per_month": 0.0,
        "included_limits": {
            "CategorizationAgent": 100,
            "ReflectionAgent": 50,
            "Audio2Text": 30
        },
        "discounts": {
            "PAYG": 0.0  # No discount
        },
        "access_features": [
            "CategorizationAgent",
            "ReflectionAgent",
            "Audio2Text"
        ]
    },
    "Pro": {
        "price_per_month": 1000.0,
        "included_limits": {
            "CategorizationAgent": 1000,
            "ReflectionAgent": 500,
            "Audio2Text": 300,
            "SmartSummaryAgent": 100,
            "VisualizationAgent": 50
        },
        "discounts": {
            "PAYG": 0.1  # 10% discount
        },
        "access_features": [
            "CategorizationAgent",
            "ReflectionAgent",
            "Audio2Text",
            "SmartSummaryAgent",
            "VisualizationAgent"
        ]
    },
    "Team": {
        "price_per_month": 3000.0,
        "included_limits": {
            "CategorizationAgent": 5000,
            "ReflectionAgent": 2500,
            "Audio2Text": 1500,
            "SmartSummaryAgent": 500,
            "VisualizationAgent": 250,
            "CodeRefactorAgent": 100
        },
        "discounts": {
            "PAYG": 0.2  # 20% discount
        },
        "access_features": [
            "CategorizationAgent",
            "ReflectionAgent",
            "Audio2Text",
            "SmartSummaryAgent",
            "VisualizationAgent",
            "CodeRefactorAgent"
        ]
    }
}

