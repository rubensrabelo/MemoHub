import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import Sidebar from './Sidebar.vue'

const mockPush = vi.fn()

vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: mockPush
  })
}))

describe('Sidebar.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('deve aplicar as classes ativas corretas com base na propriedade currentRoute', () => {
    const wrapper = mount(Sidebar, {
      props: { currentRoute: 'knowledge' }
    })

    const buttons = wrapper.findAll('nav button')
    expect(buttons[0].classes()).toContain('text-primary')
    expect(buttons[1].classes()).not.toContain('text-primary')
  })

  it('deve aplicar as classes ativas corretas para a aba de favoritos quando selecionada', () => {
    const wrapper = mount(Sidebar, {
      props: { currentRoute: 'favorites' }
    })

    const buttons = wrapper.findAll('nav button')
    expect(buttons[0].classes()).not.toContain('text-primary')
    expect(buttons[1].classes()).toContain('text-primary')
  })

  it('deve emitir o evento new-knowledge ao clicar no botao de criar conhecimento', async () => {
    const wrapper = mount(Sidebar)

    const createButton = wrapper.find('button')
    await createButton.trigger('click')

    expect(wrapper.emitted('new-knowledge')).toBeTruthy()
  })

  it('deve acionar o router.push com o nome correto ao clicar no botao Conhecimentos', async () => {
    const wrapper = mount(Sidebar)

    const buttons = wrapper.findAll('nav button')
    await buttons[0].trigger('click')

    expect(mockPush).toHaveBeenCalledWith({ name: 'knowledge' })
  })

  it('deve acionar o router.push com o nome correto ao clicar no botao Favoritos', async () => {
    const wrapper = mount(Sidebar)

    const buttons = wrapper.findAll('nav button')
    await buttons[1].trigger('click')

    expect(mockPush).toHaveBeenCalledWith({ name: 'favorites' })
  })
})
