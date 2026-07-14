import { api } from '../../../core/services/api'
import type { 
  KnowledgeCreateDTO, 
  KnowledgeUpdateDTO, 
  KnowledgeResponseDTO, 
  KnowledgeFilters 
} from '../types'

export const knowledgeService = {
  async getAll(filters?: KnowledgeFilters): Promise<KnowledgeResponseDTO[]> {
    const params = new URLSearchParams()
    
    if (filters?.search) params.append('search', filters.search)
    if (filters?.category) params.append('category', filters.category)
    if (filters?.favorite !== undefined) params.append('favorite', String(filters.favorite))

    const { data } = await api.get<KnowledgeResponseDTO[]>('/knowledge/', { params })
    return data
  },

  async getById(id: number): Promise<KnowledgeResponseDTO> {
    const { data } = await api.get<KnowledgeResponseDTO>(`/knowledge/${id}`)
    return data
  },

  async create(payload: KnowledgeCreateDTO): Promise<KnowledgeResponseDTO> {
    const { data } = await api.post<KnowledgeResponseDTO>('/knowledge/', payload)
    return data
  },

  async update(id: number, payload: KnowledgeUpdateDTO): Promise<KnowledgeResponseDTO> {
    const { data } = await api.put<KnowledgeResponseDTO>(`/knowledge/${id}`, payload)
    return data
  },

  async toggleFavorite(id: number): Promise<KnowledgeResponseDTO> {
    const { data } = await api.patch<KnowledgeResponseDTO>(`/knowledge/${id}/favorite`)
    return data
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/knowledge/${id}`)
  }
}
