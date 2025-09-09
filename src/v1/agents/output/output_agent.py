











"""
Output Agent

Main agent that integrates all output sub-agents for final result delivery.
"""

from typing import Any, Dict, Union
from .response_formatter import ResponseFormatter
from .output_dispatcher import OutputDispatcher, OutputMode
from .format_adapter import FormatAdapter, OutputFormat
from .output_sanitizer import OutputSanitizer
from .access_wrapper import AccessWrapper

class Logger:
    """
    Simple logger for output operations.
    """

    def __init__(self, enable: bool = True):
        self.enable = enable

    def log(self, data: Dict[str, Any]):
        """Logs output data"""
        if not self.enable:
            return
        print("[Log] Output delivered:", data.get("summary", "No summary available"))

class OutputAgent:
    """
    Main output agent that integrates all sub-agents.
    """

    def __init__(
        self,
        mode: Union[OutputMode, str],
        user_profile: Dict[str, Any],
        compact_mode: bool = True,
        enable_logging: bool = True,
        output_format: Union[OutputFormat, str] = OutputFormat.JSON
    ):
        """
        Initialize OutputAgent with all sub-agents.

        Args:
            mode: Output delivery mode (UI, API, FILE, EXTERNAL)
            user_profile: User profile data for access control
            compact_mode: Enable compact output mode
            enable_logging: Enable logging
            output_format: Output format
        """
        # Convert string enums to actual enums if needed
        if isinstance(mode, str):
            mode = OutputMode(mode.lower())
        if isinstance(output_format, str):
            output_format = OutputFormat(output_format.lower())

        self.formatter = ResponseFormatter()
        self.sanitizer = OutputSanitizer(compact_mode=compact_mode)
        self.access_wrapper = AccessWrapper(user_profile=user_profile)
        self.dispatcher = OutputDispatcher(mode=mode)
        self.format_adapter = FormatAdapter(format=output_format)
        self.logger = Logger(enable=enable_logging)

    def process(
        self,
        task_id: str,
        decision_result: Dict[str, Any],
        priority_data: Dict[str, Any],
        effort_data: Dict[str, Any],
        deadline: str,
        visuals: Dict[str, Any] = None,
        schedule: Dict[str, Any] = None
    ) -> Any:
        """
        Processes and delivers final output.

        Args:
            task_id: Task identifier
            decision_result: Decision result data
            priority_data: Priority analysis data
            effort_data: Effort estimation data
            deadline: Calculated deadline
            visuals: Visualization data
            schedule: Scheduling data

        Returns:
            Final output in appropriate format
        """
        # Step 1: Format response
        formatted = self.formatter.format(
            task_id=task_id,
            decision_result=decision_result,
            priority_data=priority_data,
            effort_data=effort_data,
            deadline=deadline,
            visuals=visuals,
            schedule=schedule
        )

        # Step 2: Sanitize output
        sanitized = self.sanitizer.sanitize(formatted)

        # Step 3: Apply access control
        secured = self.access_wrapper.wrap(sanitized)

        # Step 4: Log output
        self.logger.log(secured)

        # Step 5: Dispatch to appropriate interface
        dispatched = self.dispatcher.dispatch(secured)

        # Step 6: Format the dispatched result if needed
        if isinstance(dispatched, dict):
            return self.format_adapter.transform(dispatched)
        return dispatched













