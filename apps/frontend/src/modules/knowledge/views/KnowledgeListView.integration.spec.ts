import { describe, it, expect, beforeAll, afterEach, afterAll, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'
import KnowledgeListView from './KnowledgeListView.vue'

vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: vi.fn()
  })
}))

const mockApiUrl = 'http://localhost:8000/api/v1/knowledge/'

let mockDatabase = [
  {
    id: 1,
    category: 'Frontend',
    question: 'O que e Vue 3?',
    answer: 'Um framework progressivo JavaScript.',
    favorite: false,
    created_at: '2026-07-15T12:00:00',
    updated_at: '2026-07-15T12:00:00'
  },
  {
    id: 2,
    category: 'Backend',
    question: 'O que e FastAPI?',
    answer: 'Um framework Python de alta performance.',
    favorite: true,
    created_at: '2026-07-14T12:00:00',
    updated_at: '2026-07-14T12:00:00'
  }
]

const server = setupServer(
  http.get(mockApiUrl, ({ request }) => {
    const url = new URL(request.url)
    const search = url.searchParams.get('search')

    if (search) {
      const filtered = mockDatabase.filter(item => 
        item.question.toLowerCase().includes(search.toLowerCase())
      )
      return HttpResponse.json(filtered)
    }

    return HttpResponse.json(mockDatabase)
  }),

  http.post(mockApiUrl, async ({ request }) => {
    const body = await request.json() as any
    const newRecord = {
      id: 3,
      ...body,
      created_at: '2026-07-15T12:00:00',
      updated_at: '2026-07-15T12:00:00'
    }
    mockDatabase.push(newRecord)
    return HttpResponse.json(newRecord, { status: 201 })
  }),

  http.put(`${mockApiUrl}:id`, async ({ params, request }) => {
    const id = Number(params.id)
    const body = await request.json() as any
    const updatedRecord = {
      id,
      ...body,
      created_at: '2026-07-15T12:00:00',
      updated_at: '2026-07-16T12:00:00'
    }
    mockDatabase = mockDatabase.map(item => item.id === id ? updatedRecord : item)
    return HttpResponse.json(updatedRecord)
  }),

  http.delete(`${mockApiUrl}:id`, ({ params }) => {
    const id = Number(params.id)
    mockDatabase = mockDatabase.filter(item => item.id !== id)
    return new HttpResponse(null, { status: 204 })
  })
)

describe('KnowledgeListView.vue (Integration)', () => {
  beforeAll(() => server.listen({ onUnhandledRequest: 'bypass' }))
  afterEach(() => {
    server.resetHandlers()
    mockDatabase = [
      {
        id: 1,
        category: 'Frontend',
        question: 'O que e Vue 3?',
        answer: 'Um framework progressivo JavaScript.',
        favorite: false,
        created_at: '2026-07-15T12:00:00',
        updated_at: '2026-07-15T12:00:00'
      },
      {
        id: 2,
        category: 'Backend',
        question: 'O que e FastAPI?',
        answer: 'Um framework Python de alta performance.',
        favorite: true,
        created_at: '2026-07-14T12:00:00',
        updated_at: '2026-07-14T12:00:00'
      }
    ]
  })
  afterAll(() => server.close())

  it('deve exibir o esqueleto de loading e renderizar os cards apos a resposta da API', async () => {
    const wrapper = mount(KnowledgeListView)

    expect(wrapper.find('.animate-pulse').exists()).toBe(true)

    await flushPromises()

    expect(wrapper.find('.animate-pulse').exists()).toBe(false)
    expect(wrapper.text()).toContain('O que e Vue 3?')
    expect(wrapper.text()).toContain('O que e FastAPI?')
  })

  it('deve disparar nova requisicao e filtrar os cards na tela ao digitar na busca', async () => {
    const wrapper = mount(KnowledgeListView)
    await flushPromises()

    const searchInput = wrapper.find('input[type="text"]')
    await searchInput.setValue('FastAPI')
    await searchInput.trigger('input')

    await flushPromises()

    expect(wrapper.text()).toContain('O que e FastAPI?')
    expect(wrapper.text()).not.toContain('O que e Vue 3?')
  })

  it('deve renderizar a modal de cadastro ao disparar o clique na Sidebar e injetar o registro criado na lista', async () => {
    const wrapper = mount(KnowledgeListView)
    await flushPromises()

    const sidebarNewButton = wrapper.find('aside button')
    await sidebarNewButton.trigger('click')

    expect(wrapper.find('.fixed.inset-0').exists()).toBe(true)

    const modalInput = wrapper.find('.fixed input')
    const modalTextareas = wrapper.findAll('.fixed textarea')
    
    await modalInput.setValue('DevOps')
    await modalTextareas.at(0)!.setValue('O que e Docker?')
    await modalTextareas.at(1)!.setValue('Plataforma de conteinerizacao.')

    const submitButton = wrapper.find('.fixed button.bg-primary')
    await submitButton.trigger('click')

    await flushPromises()

    expect(wrapper.text()).toContain('O que e Docker?')
  })

  it('deve exibir mensagem de estado vazio caso a API retorne uma lista sem registros', async () => {
    server.use(
      http.get(mockApiUrl, () => HttpResponse.json([]))
    )

    const wrapper = mount(KnowledgeListView)
    await flushPromises()

    expect(wrapper.text()).toContain('Nenhum conhecimento cadastrado no backend.')
  })

  it('deve abrir o modal populado ao clicar em editar e atualizar as informacoes na tela apos salvar', async () => {
    const wrapper = mount(KnowledgeListView)
    await flushPromises()

    const editButton = wrapper.find('button[title="Editar"]')
    await editButton.trigger('click')

    const modalTextareas = wrapper.findAll('.fixed textarea')
    const questionTextarea = modalTextareas.at(0)!
    
    expect((questionTextarea.element as HTMLTextAreaElement).value).toBe('O que e Vue 3?')

    await questionTextarea.setValue('O que e Vue 3.4?')
    const submitButton = wrapper.find('.fixed button.bg-primary')
    await submitButton.trigger('click')
    await flushPromises()

    expect(wrapper.text()).toContain('O que e Vue 3.4?')
  })

  it('deve remover o registro do layout ao confirmar a acao de exclusao fisica', async () => {
    vi.spyOn(window, 'confirm').mockImplementation(() => true)

    const wrapper = mount(KnowledgeListView)
    await flushPromises()

    expect(wrapper.text()).toContain('O que e Vue 3?')

    const deleteButton = wrapper.find('button[title="Excluir"]')
    await deleteButton.trigger('click')
    await flushPromises()

    expect(wrapper.text()).not.toContain('O que e Vue 3?')
    expect(wrapper.text()).toContain('O que e FastAPI?')
  })
})
