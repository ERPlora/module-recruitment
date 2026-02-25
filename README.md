# Recruitment Module

Job postings, candidates and hiring pipeline.

## Features

- Create and manage job positions with status tracking (draft, open, closed, on hold)
- Define department, description, and number of vacancies per position
- Track candidates through a multi-stage hiring pipeline (applied, screening, interview, offer, hired, rejected)
- Store candidate contact information and resume notes
- Rate candidates for easy comparison
- Activate or deactivate job positions

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Recruitment > Settings**

## Usage

Access via: **Menu > Recruitment**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/recruitment/dashboard/` | Overview of recruitment activity |
| Positions | `/m/recruitment/positions/` | List and manage job positions |
| Candidates | `/m/recruitment/candidates/` | List and manage candidates |
| Settings | `/m/recruitment/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `JobPosition` | Job opening with title, department, description, status, vacancy count, and active flag |
| `Candidate` | Candidate linked to a position with name, email, phone, pipeline stage, resume notes, and rating |

## Permissions

| Permission | Description |
|------------|-------------|
| `recruitment.view_jobposition` | View job positions |
| `recruitment.add_jobposition` | Create new job positions |
| `recruitment.change_jobposition` | Edit existing job positions |
| `recruitment.delete_jobposition` | Delete job positions |
| `recruitment.view_candidate` | View candidates |
| `recruitment.add_candidate` | Add new candidates |
| `recruitment.change_candidate` | Edit existing candidates |
| `recruitment.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
