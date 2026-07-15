import { describe, it, expect, vi, beforeEach } from 'vitest'
import { knowledgeService } from './knowledgeService'
import { api } from '../../../core/services/api'

vi.mock('../../../core/services/api', () => ({
  api: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn()
  }
}))

describe('knowledgeService.ts', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('deve chamar getAll e anexar os parametros de busca e favoritos na URL', async () => {
    const mockData = [{ id: 1, question: 'Teste', answer: 'Resposta', category: 'Dev', favorite: true }]
    vi.mocked(api.get).mockResolvedValueOnce({ data: mockData })

    const filters = { search: 'FastAPI', favorite: true }
    const result = await knowledgeService.getAll(filters)

    expect(api.get).toHaveBeenCalledWith('/knowledge/', expect.any(Object))
    const calledOptions = vi.mocked(api.get).mock.calls[0][1] as any
    expect(calledOptions.params.get('search')).toBe('FastAPI')
    expect(calledOptions.params.get('favorite')).toBe('true')
    expect(result).toEqual(mockData)
  })

  it('deve disparar o verbo POST com o payload correto para criar um conhecimento', async () => {
    const payload = { question: 'Q1', answer: 'A1', category: 'Vue', favorite: false }
    const responseMock = { id: 10, ...payload }
    vi.mocked(api.post).mockResolvedValueOnce({ data: responseMock })

    const result = await knowledgeService.create(payload)

    expect(api.post).toHaveBeenCalledWith('/knowledge/', payload)
    expect(result.id).toBe(10)
  })

  it('deve disparar o verbo PATCH para alternar o estado de favorito', async () => {
    const responseMock = { id: 5, favorite: true }
    vi.mocked(api.patch).mockResolvedValueOnce({ data: responseMock })

    const result = await knowledgeService.toggleFavorite(5)

    expect(api.patch).toHaveBeenCalledWith('/knowledge/5/favorite')
    expect(result.favorite).toBe(true)
  })

  it('deve disparar o verbo DELETE para excluir um conhecimento', async () => {
    vi.mocked(api.delete).mockResolvedValueOnce({})

    await knowledgeService.delete(7)

    expect(api.delete).toHaveBeenCalledWith('/knowledge/7')
  })
})
