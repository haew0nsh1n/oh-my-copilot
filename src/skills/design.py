"""Design skill — maintain DESIGN.md in repo root."""

from typing import Optional
from domain import (
    DesignDocument, DesignSection, DesignSectionType, DesignReport,
)


class DesignSkill:
    name = "design"
    description = "Maintain repo-local DESIGN.md — architecture and interaction design"

    def __init__(self):
        self.documents: dict = {}

    def create_document(self, project_name: str) -> DesignDocument:
        doc = DesignDocument(project_name=project_name)
        self.documents[project_name] = doc
        return doc

    def add_section(self, doc: DesignDocument, title: str, section_type: DesignSectionType, content: str = "") -> DesignSection:
        section = DesignSection(title=title, section_type=section_type, content=content)
        doc.add_section(section)
        return section

    def update_section(self, doc: DesignDocument, title: str, content: str) -> bool:
        return doc.update_section(title, content)

    def get_section(self, doc: DesignDocument, title: str) -> Optional[DesignSection]:
        return doc.get_section(title)

    def to_markdown(self, doc: DesignDocument) -> str:
        return doc.to_markdown()

    def generate_report(self, doc: DesignDocument) -> DesignReport:
        has_arch = any(s.section_type == DesignSectionType.ARCHITECTURE for s in doc.sections)
        has_decisions = any(s.section_type == DesignSectionType.DECISIONS for s in doc.sections)
        return DesignReport(
            project_name=doc.project_name,
            sections_count=len(doc.sections),
            last_updated=doc.last_updated,
            has_architecture=has_arch,
            has_decisions=has_decisions,
            summary=f"DESIGN.md: {len(doc.sections)} sections, v{doc.version}"
        )

    def get_document(self, project_name: str) -> Optional[DesignDocument]:
        return self.documents.get(project_name)
