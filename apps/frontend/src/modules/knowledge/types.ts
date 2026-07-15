export interface KnowledgeBaseDTO {
  question: string
  answer: string
  category: string
  favorite: boolean
}

export interface KnowledgeCreateDTO extends KnowledgeBaseDTO {}

export interface KnowledgeUpdateDTO extends KnowledgeBaseDTO {}

export interface KnowledgeResponseDTO extends KnowledgeBaseDTO {
  id: number
  created_at: string
  updated_at: string
}

export interface KnowledgeFilters {
  search?: string
  category?: string
  favorite?: boolean
}
