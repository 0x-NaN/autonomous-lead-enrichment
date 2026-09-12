from pydantic import BaseModel, Field
from typing import Optional
from typing import List


class ContactPoints(BaseModel):
    email: str
    type: str


class TeamMember(BaseModel):
    name: str
    role: str
    linkedin_url: Optional[str] = None


class CompanyEnrichment(BaseModel):
    domain: str
    company_overview: str = Field(..., description="2-sentence summary")
    target_audience: str = Field(..., description="ICP description")
    contact_points: List[ContactPoints] = Field(default_factory=list)
    key_leadership: List[TeamMember] = Field(default_factory=list)
    data_confidence_score: float = Field(..., ge=0.0, le=1.0)
    errors: Optional[List[str]] = None