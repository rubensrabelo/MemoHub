export interface KnowledgeCreateDTO {
  category: string
  question: string
  answer: string
  favorite?: boolean
}

export interface KnowledgeUpdateDTO {
  category?: string
  question?: string
  answer?: string
  favorite?: boolean
}

export interface KnowledgeResponseDTO {
  id: number
  category: string
  question: string
  answer: string
  favorite: boolean
  created_at: string
}

export interface KnowledgeFilters {
  search?: string
  category?: string
  favorite?: boolean
}
