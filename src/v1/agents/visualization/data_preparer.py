



"""
Data Preparer Agent

Prepares and structures data for visualization.
"""

from typing import List, Dict, Any, Optional

class DataPreparer:
    """
    Prepares and structures data for visualization.
    """

    def __init__(self, raw_data: List[Dict[str, Any]]):
        self.raw_data = raw_data
        self.prepared_data = None

    def validate(self) -> bool:
        """
        Validates data structure and required fields.
        """
        if not self.raw_data:
            raise ValueError("Data cannot be empty")

        # Check that all items have consistent structure
        if len(self.raw_data) > 0:
            first_keys = set(self.raw_data[0].keys())
            for item in self.raw_data[1:]:
                if not first_keys.issuperset(item.keys()):
                    raise ValueError("Inconsistent data structure")

        return True

    def clean(self) -> None:
        """
        Cleans data by removing duplicates and filling missing values.
        """
        # Remove duplicates
        seen = set()
        unique_data = []
        for item in self.raw_data:
            item_key = tuple(item.items())
            if item_key not in seen:
                seen.add(item_key)
                unique_data.append(item)

        # Fill missing values with defaults
        if unique_data:
            all_keys = set().union(*(d.keys() for d in unique_data))
            for item in unique_data:
                for key in all_keys:
                    if key not in item:
                        item[key] = None  # Could be customized per field

        self.raw_data = unique_data

    def aggregate(self, group_by_fields: List[str]) -> Dict[str, Any]:
        """
        Aggregates data by specified fields.

        Args:
            group_by_fields: Fields to group by

        Returns:
            Aggregated data
        """
        grouped = {}
        for item in self.raw_data:
            key = tuple(item.get(field, "unknown") for field in group_by_fields)
            if key not in grouped:
                grouped[key] = {
                    "count": 0,
                    "items": [],
                    "total_value": 0  # Example aggregation
                }
            grouped[key]["count"] += 1
            grouped[key]["items"].append(item)
            # Example: sum a 'value' field if it exists
            if "value" in item:
                grouped[key]["total_value"] += item["value"]

        # Convert keys to readable format
        result = []
        for key, data in grouped.items():
            group_dict = {
                "group": key,
                "count": data["count"],
                "total_value": data["total_value"],
                "items": data["items"]
            }
            result.append(group_dict)

        self.prepared_data = result
        return result

    def get_prepared_data(self) -> Optional[Dict[str, Any]]:
        """
        Returns prepared data.
        """
        return self.prepared_data



