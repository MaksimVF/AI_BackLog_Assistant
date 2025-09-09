


"""
Self-Learning and Retraining Module for Domain Categorizers
"""

import json
import os
from datetime import datetime
from typing import Dict, List
from config.settings import BASE_DIR
from ..second_level_categorization.domain_router import DOMAIN_CATEGORIZERS
from ..second_level_categorization.domains import get_categorizer_class

# Directory for storing logs and taxonomy updates
LOG_DIR = BASE_DIR / "data" / "categorization_logs"
TAXONOMY_DIR = BASE_DIR / "agents" / "categorization" / "second_level_categorization" / "taxonomy"

# Ensure directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(TAXONOMY_DIR, exist_ok=True)

def log_categorization_result(domain: str, result: dict, input_text: str):
    """
    Logs categorization results for potential retraining.

    Args:
        domain: The domain of the categorization
        result: The categorization result dict
        input_text: The original input text
    """
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "domain": domain,
            "category": result.get("category", "unknown"),
            "confidence": float(result.get("confidence", 0)),
            "source": result.get("source", "unknown"),
            "input_text": input_text
        }

        log_file = LOG_DIR / f"{domain}_log.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Error logging categorization result: {e}")

def extract_labeled_examples(domain: str, min_confidence: float = 0.8) -> Dict[str, List[str]]:
    """
    Extracts high-confidence labeled examples from logs.

    Args:
        domain: The domain to extract examples for
        min_confidence: Minimum confidence threshold

    Returns:
        Dictionary mapping categories to lists of example texts
    """
    log_file = LOG_DIR / f"{domain}_log.jsonl"
    if not log_file.exists():
        return {}

    category_examples = {}
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    category = entry.get("category")
                    text = entry.get("input_text")
                    confidence = entry.get("confidence", 0)

                    if (confidence >= min_confidence and
                        category and
                        text and
                        len(text.strip()) > 10):  # Only keep meaningful examples
                        category_examples.setdefault(category, []).append(text)
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"Error extracting labeled examples: {e}")

    return category_examples

def update_taxonomy_examples(domain: str, updates: Dict[str, List[str]]):
    """
    Updates the taxonomy with new examples.

    Args:
        domain: The domain to update
        updates: Dictionary of category to new examples
    """
    taxonomy_path = TAXONOMY_DIR / f"{domain}_taxonomy.json"

    if not taxonomy_path.exists():
        # Create default taxonomy if it doesn't exist
        taxonomy = {}
    else:
        with open(taxonomy_path, "r", encoding="utf-8") as f:
            taxonomy = json.load(f)

    # Update with new examples
    for category, examples in updates.items():
        if category in taxonomy:
            # Add new examples to existing category
            if "examples" not in taxonomy[category]:
                taxonomy[category]["examples"] = []
            taxonomy[category]["examples"].extend(examples)
            # Remove duplicates
            taxonomy[category]["examples"] = list(set(taxonomy[category]["examples"]))
        else:
            # Create new category
            taxonomy[category] = {
                "description": f"Auto-generated category for {category}",
                "examples": examples
            }

    # Save updated taxonomy
    with open(taxonomy_path, "w", encoding="utf-8") as f:
        json.dump(taxonomy, f, ensure_ascii=False, indent=2)

def retrain_domain_categorizer(domain: str):
    """
    Retrains a domain categorizer with new examples.

    Args:
        domain: The domain to retrain
    """
    try:
        # Extract new examples from logs
        new_examples = extract_labeled_examples(domain)

        if not new_examples:
            print(f"No new examples found for domain: {domain}")
            return False

        # Update taxonomy with new examples
        update_taxonomy_examples(domain, new_examples)

        # Get the categorizer class for this domain
        categorizer_class = get_categorizer_class(domain)
        if not categorizer_class:
            print(f"Categorizer class not found for domain: {domain}")
            return False

        # Reinitialize the categorizer with updated taxonomy
        categorizer = categorizer_class()
        DOMAIN_CATEGORIZERS[domain] = categorizer

        print(f"Successfully retrained categorizer for domain: {domain}")
        return True

    except Exception as e:
        print(f"Error retraining domain categorizer: {e}")
        return False

def retrain_all_categorizers():
    """
    Retrains all domain categorizers.
    """
    success_count = 0
    for domain in DOMAIN_CATEGORIZERS.keys():
        if retrain_domain_categorizer(domain):
            success_count += 1

    print(f"Retrained {success_count}/{len(DOMAIN_CATEGORIZERS)} categorizers")
    return success_count

