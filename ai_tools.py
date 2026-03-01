"""AI tools for the Recruitment module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListJobPositions(AssistantTool):
    name = "list_job_positions"
    description = "List job positions/openings."
    module_id = "recruitment"
    required_permission = "recruitment.view_jobposition"
    parameters = {
        "type": "object",
        "properties": {"status": {"type": "string", "description": "draft, open, closed, on_hold"}, "department": {"type": "string"}},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from recruitment.models import JobPosition
        qs = JobPosition.objects.all()
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        if args.get('department'):
            qs = qs.filter(department__icontains=args['department'])
        return {"positions": [{"id": str(p.id), "title": p.title, "department": p.department, "status": p.status, "vacancies": p.vacancies, "is_active": p.is_active} for p in qs]}


@register_tool
class CreateJobPosition(AssistantTool):
    name = "create_job_position"
    description = "Create a job position/opening."
    module_id = "recruitment"
    required_permission = "recruitment.add_jobposition"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "title": {"type": "string"}, "department": {"type": "string"},
            "description": {"type": "string"}, "vacancies": {"type": "integer"},
        },
        "required": ["title"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from recruitment.models import JobPosition
        p = JobPosition.objects.create(title=args['title'], department=args.get('department', ''), description=args.get('description', ''), vacancies=args.get('vacancies', 1))
        return {"id": str(p.id), "title": p.title, "created": True}


@register_tool
class ListCandidates(AssistantTool):
    name = "list_candidates"
    description = "List job candidates."
    module_id = "recruitment"
    required_permission = "recruitment.view_candidate"
    parameters = {
        "type": "object",
        "properties": {"position_id": {"type": "string"}, "stage": {"type": "string", "description": "applied, screening, interview, offer, hired, rejected"}, "limit": {"type": "integer"}},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from recruitment.models import Candidate
        qs = Candidate.objects.select_related('position').all()
        if args.get('position_id'):
            qs = qs.filter(position_id=args['position_id'])
        if args.get('stage'):
            qs = qs.filter(stage=args['stage'])
        limit = args.get('limit', 20)
        return {"candidates": [{"id": str(c.id), "name": c.name, "email": c.email, "position": c.position.title if c.position else None, "stage": c.stage, "rating": c.rating} for c in qs[:limit]]}


@register_tool
class CreateCandidate(AssistantTool):
    name = "create_candidate"
    description = "Add a candidate to a job position."
    module_id = "recruitment"
    required_permission = "recruitment.add_candidate"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "position_id": {"type": "string"}, "name": {"type": "string"},
            "email": {"type": "string"}, "phone": {"type": "string"},
            "resume_notes": {"type": "string"},
        },
        "required": ["position_id", "name"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from recruitment.models import Candidate
        c = Candidate.objects.create(position_id=args['position_id'], name=args['name'], email=args.get('email', ''), phone=args.get('phone', ''), resume_notes=args.get('resume_notes', ''))
        return {"id": str(c.id), "name": c.name, "created": True}
