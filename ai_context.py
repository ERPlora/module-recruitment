"""
AI context for the Recruitment module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Recruitment

### Models

**JobPosition**
- title (str), department (str, optional), description (text)
- status: draft | open | closed | on_hold
- vacancies (int, how many positions open), is_active (bool)

**Candidate**
- position (FK → JobPosition, related_name='candidates')
- name (str), email (optional), phone (optional)
- stage: applied | screening | interview | offer | hired | rejected
- resume_notes (text), rating (int 0–5)

### Key flows

1. **Create a job opening**: Create JobPosition with status=open, set vacancies count
2. **Add a candidate**: Create Candidate linked to position, stage defaults to 'applied'
3. **Advance candidate**: Update stage in sequence: applied → screening → interview → offer → hired
4. **Reject candidate**: Set stage=rejected at any point
5. **Close position**: Set JobPosition.status=closed once vacancies are filled
6. **Put on hold**: Set JobPosition.status=on_hold to pause without closing

### Notes

- There is no separate interview or offer model — all tracking is via the Candidate.stage field
- rating (0–5) is a simple integer score for quick assessment
- Multiple candidates can exist for the same position
- Hired candidates should trigger creating a StaffMember in the staff module (not automated)
"""
