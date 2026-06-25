---
name: travel-logistics-tracker
description: >-
  Watches for trip/conference email threads and consolidates flights, hotels, and agendas into one
  clear brief per trip, so conference season stops being chaos. Use when asked "my travel brief",
  "upcoming trips", "travel logistics", or run on a daily schedule. Requires Gmail and Google
  Calendar connectors.
---

# Travel Logistics Tracker

## Purpose
Pull scattered confirmation emails and calendar holds into a single, trip-by-trip brief — so you
have flights, hotel, and agenda in one place instead of digging through your inbox at the gate.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Look ahead ~30 days for upcoming trips. If a trip is happening *today/
   imminently*, put it first and include same-day details (gate-time, check-in).
2. Scan Gmail for travel signals: flight confirmations (airlines, PNRs), hotel bookings, car/rail,
   conference registrations, itineraries. Cross-reference Google Calendar for travel holds and
   event dates.
3. **Group by trip** (cluster by destination + date range). For each trip, consolidate:
   - **Flights:** carrier, flight #, dates/times, confirmation code, seat if known.
   - **Lodging:** hotel, check-in/out dates, confirmation.
   - **Ground:** car/rail/transfers if present.
   - **Agenda:** conference/meeting events during the trip (from Calendar + emails).
   - **Gaps/risks:** missing hotel, tight connections, no return flight, overlapping holds.
4. Order trips by start date.

## Output format
```
✈️ Travel Brief — as of <date>

<Destination> · <date range>
  Flights: <carrier FL123> dep <…> → arr <…> · conf <CODE>
  Hotel: <name> · <check-in>–<check-out> · conf <CODE>
  Agenda: <key events>
  ⚠️ Gaps: <e.g. no return flight booked>
```
If no upcoming trips, say "No upcoming trips detected."

## Guardrails
- **Read-only.** Consolidates and reports; never books, cancels, replies, or changes calendar.
- Treat confirmation codes/PNRs as sensitive — include them in your brief but never share or send
  anywhere.
- Flag uncertainty (e.g. "hotel not found for this trip") rather than guessing.
- Idempotent; rerunning rebuilds the brief.
