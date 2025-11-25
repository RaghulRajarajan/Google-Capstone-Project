"""
Mock Calendar tool (OpenAPI style).
Provides a function `schedule_followup(meeting_id, date, attendees)` that 'schedules' an event.
In a real deployment integrate Google Calendar API; here we record to memory or print.
"""
import logging
logger = logging.getLogger("calendar_tool")

class CalendarTool:
    def schedule_followup(self, meeting_id, date, attendees):
        # mock scheduling
        logger.info("Mock scheduled follow-up for %s on %s with %s", meeting_id, date, attendees)
        return {"status": "ok", "meeting_id": meeting_id, "date": date, "attendees": attendees}
