



"""
Execution Planner Agent

Main agent that integrates all sub-agents to create comprehensive
execution plans for tasks after decision making.
"""

from datetime import datetime
from typing import Dict, Any, List
from .timeline_estimator import estimate_timeline
from .deadline_calculator import DeadlineCalculator
from .scheduling_integrator import SchedulingIntegrator
from .followup_notifier import FollowUpNotifier
from .dependency_detector import detect_dependencies
from .risk_classifier import classify_risks
from .final_decision_maker import make_final_decision

class ExecutionPlannerAgent:
    """
    Main execution planner agent that coordinates all sub-agents
    to create comprehensive execution plans.
    """

    def __init__(self):
        """Initialize with all sub-agents"""
        self.deadline_calculator = DeadlineCalculator()
        self.scheduling_integrator = SchedulingIntegrator()
        self.followup_notifier = FollowUpNotifier()

    def plan_execution(self, task_data: Dict[str, Any], decision: str) -> Dict[str, Any]:
        """
        Creates comprehensive execution plan for a task.

        Args:
            task_data: Task data
            decision: Decision from DecisionAgent (recommend, defer, reject)

        Returns:
            Execution plan with all details
        """
        # Step 1: Timeline estimation
        timeline = estimate_timeline(
            task_data.get("estimated_effort_days", 3),
            task_data.get("priority", "medium"),
            task_data.get("criticality", "medium")
        )

        # Step 2: Deadline calculation
        current_dt = datetime.now()
        effort_hours = task_data.get("effort_hours", 12)
        deadline_info = self.deadline_calculator.calculate_deadline_info(current_dt, effort_hours)

        # Step 3: Dependency detection
        dependencies = detect_dependencies(
            task_data.get("description", ""),
            task_data.get("dependencies", []),
            task_data.get("stakeholders", [])
        )

        # Step 4: Risk classification
        constraints = {
            "deadline": deadline_info["deadline_date"],
            "budget": task_data.get("budget", 5000),
            "team_size": task_data.get("team_size", 2)
        }
        risks = classify_risks(
            task_data.get("description", ""),
            constraints,
            task_data.get("stakeholders", [])
        )

        # Step 5: Final decision making
        final_decision_data = {
            "priority_score": task_data.get("priority_score", 5),
            "consistency_check": {"is_consistent": True},  # Placeholder
            "effort_estimate": task_data.get("effort", "medium"),
            "criticality": task_data.get("criticality", "medium"),
            "strategic_alignment": task_data.get("strategic_alignment", True)
        }
        final_decision = make_final_decision(final_decision_data)

        # Step 6: Scheduling integration
        scheduling_data = {
            "title": task_data.get("title", "Untitled Task"),
            "description": task_data.get("description", ""),
            "assigned_to": task_data.get("assigned_to", "Unassigned"),
            "priority": task_data.get("priority", "medium"),
            "category": task_data.get("category", "General"),
            "due_date": datetime.fromisoformat(deadline_info["deadline_date"])
        }
        scheduled_task = self.scheduling_integrator.integrate_task(**scheduling_data)

        # Step 7: Follow-up notifications
        followup_data = {
            "decision": final_decision["decision"],
            "created_at": current_dt,
            "due_date": datetime.fromisoformat(deadline_info["deadline_date"])
        }
        followups = self.followup_notifier.create_reminders(**followup_data)

        # Compile comprehensive execution plan
        execution_plan = {
            "task_id": task_data.get("task_id", "unknown"),
            "original_decision": decision,
            "final_decision": final_decision,
            "timeline_estimation": timeline,
            "deadline_calculation": deadline_info,
            "dependency_analysis": dependencies,
            "risk_assessment": risks,
            "scheduled_task": scheduled_task,
            "followup_notifications": followups,
            "execution_status": "planned"
        }

        return execution_plan

    def plan_batch_execution(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Plans execution for a batch of tasks.

        Args:
            tasks: List of task data with decisions

        Returns:
            List of execution plans
        """
        return [self.plan_execution(task["task"], task["decision"]) for task in tasks]







