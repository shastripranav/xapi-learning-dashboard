"""Course catalog with skill mappings — shared between demo generator and analytics."""

COURSES = [
    {
        "id": "course-python-101", "name": "Python Fundamentals",
        "domain": "Technical", "difficulty": "beginner",
        "modules": 8, "skills": ["Python", "Programming Basics"],
    },
    {
        "id": "course-cloud-arch", "name": "Cloud Architecture",
        "domain": "Technical", "difficulty": "advanced",
        "modules": 12, "skills": ["Cloud Computing", "System Design"],
    },
    {
        "id": "course-devops-ci", "name": "DevOps & CI/CD",
        "domain": "Technical", "difficulty": "intermediate",
        "modules": 10, "skills": ["DevOps", "Automation"],
    },
    {
        "id": "course-api-design", "name": "API Design Patterns",
        "domain": "Technical", "difficulty": "intermediate",
        "modules": 9, "skills": ["API Design", "System Design"],
    },
    {
        "id": "course-security", "name": "Application Security",
        "domain": "Technical", "difficulty": "advanced",
        "modules": 11, "skills": ["Security", "Risk Management"],
    },
    {
        "id": "course-data-privacy", "name": "Data Privacy Essentials",
        "domain": "Compliance", "difficulty": "beginner",
        "modules": 6, "skills": ["Data Privacy", "Compliance"],
    },
    {
        "id": "course-soc2", "name": "SOC 2 Compliance",
        "domain": "Compliance", "difficulty": "intermediate",
        "modules": 8, "skills": ["Compliance", "Risk Management"],
    },
    {
        "id": "course-gdpr", "name": "GDPR for Practitioners",
        "domain": "Compliance", "difficulty": "intermediate",
        "modules": 7, "skills": ["Data Privacy", "Compliance"],
    },
    {
        "id": "course-mgmt-101", "name": "Management Foundations",
        "domain": "Leadership", "difficulty": "beginner",
        "modules": 7, "skills": ["Leadership", "Communication"],
    },
    {
        "id": "course-communication", "name": "Business Communication",
        "domain": "Leadership", "difficulty": "beginner",
        "modules": 6, "skills": ["Communication", "Collaboration"],
    },
    {
        "id": "course-strategy", "name": "Strategic Thinking",
        "domain": "Leadership", "difficulty": "advanced",
        "modules": 10, "skills": ["Strategy", "Leadership"],
    },
    {
        "id": "course-coaching", "name": "Coaching Skills",
        "domain": "Leadership", "difficulty": "intermediate",
        "modules": 8, "skills": ["Leadership", "Communication"],
    },
    {
        "id": "course-analytics", "name": "Product Analytics",
        "domain": "Product", "difficulty": "intermediate",
        "modules": 9, "skills": ["Analytics", "Data Privacy"],
    },
    {
        "id": "course-user-research", "name": "User Research Methods",
        "domain": "Product", "difficulty": "intermediate",
        "modules": 8, "skills": ["Research", "Communication"],
    },
    {
        "id": "course-roadmapping", "name": "Product Roadmapping",
        "domain": "Product", "difficulty": "advanced",
        "modules": 7, "skills": ["Strategy", "Collaboration"],
    },
]

ALL_SKILLS = sorted({s for c in COURSES for s in c["skills"]})
COURSE_BY_ID = {c["id"]: c for c in COURSES}
