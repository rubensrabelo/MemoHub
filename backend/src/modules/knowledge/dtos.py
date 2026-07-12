from datetime import datetime
from pydantic import BaseModel, Field

class KnowledgeBaseDTO(BaseModel):
    question: str = Field(..., description="Pergunta detalhada")
    answer: str = Field(..., description="Resposta explicativa")
    category: str = Field(..., max_length=100, description="Categoria do conhecimento")
    favorite: bool = Field(default=False, description="Indica se é favorita")

class KnowledgeCreateDTO(KnowledgeBaseDTO):
    pass

class KnowledgeUpdateDTO(KnowledgeBaseDTO):
    pass

class KnowledgeResponseDTO(KnowledgeBaseDTO):
    id: int
    created_at: datetime
    updated_at: datetime
