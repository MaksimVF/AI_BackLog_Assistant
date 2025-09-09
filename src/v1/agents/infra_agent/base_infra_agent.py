

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("InfraAgent")

class BaseInfraAgent(ABC):
    """Base class for infrastructure monitoring agents."""

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.last_check = None
        self.status = "initializing"
        logger.info(f"Initialized {self.name}")

    @abstractmethod
    def check_status(self) -> Dict[str, Any]:
        """Check the status of the monitored component."""
        pass

    def run_check(self) -> None:
        """Run a status check and update internal state."""
        try:
            self.last_check = datetime.now()
            result = self.check_status()
            self.status = result.get("status", "unknown")
            logger.info(f"{self.name} check completed: {self.status}")
            return result
        except Exception as e:
            self.status = "error"
            logger.error(f"{self.name} check failed: {e}")
            return {"status": "error", "error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Get current status information."""
        return {
            "name": self.name,
            "status": self.status,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "config": self.config
        }

