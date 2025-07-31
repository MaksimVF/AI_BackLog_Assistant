





"""
Interactive Controller Agent

Manages interactive data operations like filtering and sorting.
"""

from typing import List, Dict, Any, Callable, Optional

class InteractiveController:
    """
    Manages interactive data operations.
    """

    def __init__(self, data: List[Dict[str, Any]], on_update: Optional[Callable[[List[Dict[str, Any]]], None]] = None):
        """
        Args:
            data: Original dataset
            on_update: Callback for data updates
        """
        self.original_data = data
        self.filtered_data = data.copy()
        self.on_update = on_update

    def filter_by(self, key: str, value: Any) -> None:
        """
        Filters data by key and value.

        Args:
            key: Field to filter by
            value: Value to filter for
        """
        self.filtered_data = [item for item in self.filtered_data if item.get(key) == value]
        self._notify_update()

    def sort_by(self, key: str, reverse: bool = False) -> None:
        """
        Sorts data by key.

        Args:
            key: Field to sort by
            reverse: Sort in descending order
        """
        self.filtered_data.sort(key=lambda x: x.get(key, None), reverse=reverse)
        self._notify_update()

    def reset(self) -> None:
        """
        Resets to original data.
        """
        self.filtered_data = self.original_data.copy()
        self._notify_update()

    def get_current_data(self) -> List[Dict[str, Any]]:
        """
        Gets current filtered/sorted data.

        Returns:
            Current dataset
        """
        return self.filtered_data

    def _notify_update(self) -> None:
        """
        Notifies about data updates.
        """
        if self.on_update:
            self.on_update(self.filtered_data)







