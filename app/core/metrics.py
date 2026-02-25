from prometheus_client import Counter

inbound_messages_total = Counter("inbound_messages_total", "Inbound messages")
outbound_messages_total = Counter("outbound_messages_total", "Outbound messages")
webhook_duplicates_total = Counter("webhook_duplicates_total", "Webhook duplicate events")
job_runs_total = Counter("job_runs_total", "Job runs", ["job"])
job_failures_total = Counter("job_failures_total", "Job failures", ["job"])
fine_checks_total = Counter("fine_checks_total", "Fine checks")
reminders_sent_total = Counter("reminders_sent_total", "Reminder messages")
safety_sessions_started_total = Counter("safety_sessions_started_total", "Safety sessions started")
safety_escalations_total = Counter("safety_escalations_total", "Safety escalations")
