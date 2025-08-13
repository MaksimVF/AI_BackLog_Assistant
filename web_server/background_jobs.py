

"""
Background Jobs for AI Backlog Assistant

Handles scheduled tasks including:
- Storage cleanup
- Billing processing
- Maintenance tasks
"""

import threading
import time
from datetime import datetime, timedelta
from flask import current_app as app
from .storage_manager import StorageManager
from .billing_manager import BillingManager

class BackgroundJobScheduler:
    """Scheduler for background jobs."""

    def __init__(self):
        self.jobs = []
        self.running = False

    def start(self):
        """Start the background job scheduler."""
        if not self.running:
            self.running = True
            threading.Thread(target=self._run_scheduler, daemon=True).start()

    def stop(self):
        """Stop the background job scheduler."""
        self.running = False

    def add_job(self, job_func, interval_seconds, *args, **kwargs):
        """
        Add a job to the scheduler.

        Args:
            job_func: Function to execute
            interval_seconds: Interval between executions in seconds
            *args, **kwargs: Arguments to pass to the function
        """
        job = {
            'func': job_func,
            'interval': interval_seconds,
            'args': args,
            'kwargs': kwargs,
            'last_run': None,
            'next_run': datetime.utcnow()
        }
        self.jobs.append(job)

    def _run_scheduler(self):
        """Main scheduler loop."""
        while self.running:
            now = datetime.utcnow()

            for job in self.jobs:
                if now >= job['next_run']:
                    try:
                        # Execute the job
                        job['func'](*job['args'], **job['kwargs'])
                        job['last_run'] = now
                        job['next_run'] = now + timedelta(seconds=job['interval'])
                    except Exception as e:
                        app.logger.error(f"Background job error: {str(e)}")

            # Sleep for a short interval
            time.sleep(60)  # Check every minute

def setup_background_jobs():
    """Set up background jobs."""
    scheduler = BackgroundJobScheduler()

    # Add storage cleanup job (daily)
    scheduler.add_job(storage_cleanup_job, 86400)  # 24 hours

    # Add billing processing job (daily)
    scheduler.add_job(billing_processing_job, 86400)  # 24 hours

    return scheduler

def storage_cleanup_job():
    """Background job for storage cleanup."""
    try:
        result = StorageManager.cleanup_expired_storage()
        app.logger.info(f"Storage cleanup completed: {result}")
    except Exception as e:
        app.logger.error(f"Storage cleanup job failed: {str(e)}")

def billing_processing_job():
    """Background job for billing processing."""
    try:
        # For now, just log that the job ran
        # In production, this would process monthly billing, etc.
        app.logger.info("Billing processing job completed")
    except Exception as e:
        app.logger.error(f"Billing processing job failed: {str(e)}")

# Global scheduler instance
scheduler = None

def init_background_jobs():
    """Initialize background jobs."""
    global scheduler
    scheduler = setup_background_jobs()
    scheduler.start()

def get_scheduler():
    """Get the global scheduler instance."""
    return scheduler

