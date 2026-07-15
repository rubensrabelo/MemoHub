import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import KnowledgeCard from './KnowledgeCard.vue'

describe('KnowledgeCard.vue', () => {
  const mockKnowledge = {
    id: 42,
    category: 'Vue 3',
    question: 'Como funciona a Composition API?',
    answer: 'Ela organiza a lógica por recursos funcionais.',
    favorite: false,
    created_at: '2026-07-15T12:00:00',
    updated_at: '2026-07-15T12:00:00'
  }

  it('deve renderizar a pergunta e a categoria reativas vindas via props', () => {
    const wrapper = mount(KnowledgeCard, {
      props: { knowledge: mockKnowledge }
    })

    expect(wrapper.text()).toContain('Vue 3')
    expect(wrapper.text()).toContain('Como funciona a Composition API?')
  })

  it('deve formatar a data de criacao omitindo a string de ligacao', () => {
    const wrapper = mount(KnowledgeCard, {
      props: { knowledge: mockKnowledge }
    })

    expect(wrapper.text()).toContain('15 jul de 2026')
  })

  it('deve alternar a visibilidade da resposta modificando a classe ao clicar no botao', async () => {
    const wrapper = mount(KnowledgeCard, {
      props: { knowledge: mockKnowledge }
    })

    const toggleButton = wrapper.find('button.text-primary')
    expect(wrapper.text()).not.toContain('Ocultar resposta')

    await toggleButton.trigger('click')
    expect(wrapper.text()).toContain('Ocultar resposta')
  })

  it('deve emitir o evento toggle-favorite com o ID correto do conhecimento', async () => {
    const wrapper = mount(KnowledgeCard, {
      props: { knowledge: mockKnowledge }
    })

    const favoriteButton = wrapper.find('button.rounded-lg')
    await favoriteButton.trigger('click')

    expect(wrapper.emitted('toggle-favorite')).toBeTruthy()
    expect(wrapper.emitted('toggle-favorite')?.[0]).toEqual([42])
  })
})
