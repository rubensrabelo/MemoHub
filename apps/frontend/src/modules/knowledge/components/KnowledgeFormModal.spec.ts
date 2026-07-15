import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import KnowledgeFormModal from './KnowledgeFormModal.vue'

describe('KnowledgeFormModal.vue', () => {
  it('nao deve renderizar o conteudo da modal quando isOpen for false', () => {
    const wrapper = mount(KnowledgeFormModal, {
      props: { isOpen: false }
    })
    expect(wrapper.find('.fixed').exists()).toBe(false)
  })

  it('deve renderizar a modal completa quando isOpen for true', () => {
    const wrapper = mount(KnowledgeFormModal, {
      props: { isOpen: true }
    })
    expect(wrapper.find('.fixed').exists()).toBe(true)
    expect(wrapper.find('input').exists()).toBe(true)
    expect(wrapper.findAll('textarea').length).toBe(2)
  })

  it('deve desativar o botao de envio se os campos obrigatorios estiverem vazios', () => {
    const wrapper = mount(KnowledgeFormModal, {
      props: { isOpen: true }
    })
    const submitButton = wrapper.find('button.bg-primary')
    expect(submitButton.attributes('disabled')).toBeDefined()
  })

  it('deve alternar o estado do campo favorito ao clicar no bloco correspondente', async () => {
    const wrapper = mount(KnowledgeFormModal, {
      props: { isOpen: true }
    })
    const favoriteBlock = wrapper.find('.cursor-pointer.select-none')
    
    expect(favoriteBlock.classes()).not.toContain('bg-amber-500/10')
    await favoriteBlock.trigger('click')
    expect(favoriteBlock.classes()).toContain('bg-amber-500/10')
  })

  it('deve emitir o evento save com o payload preenchido e fechar a modal com sucesso', async () => {
    const wrapper = mount(KnowledgeFormModal, {
      props: { isOpen: true }
    })

    const input = wrapper.find('input')
    const textareas = wrapper.findAll('textarea')
    
    await input.setValue('Backend')
    await textareas[0].setValue('O que é FastAPI?')
    await textareas[1].setValue('Um framework web moderno e rápido.')

    const submitButton = wrapper.find('button.bg-primary')
    expect(submitButton.attributes('disabled')).toBeUndefined()

    await submitButton.trigger('click')

    expect(wrapper.emitted('save')).toBeTruthy()
    expect(wrapper.emitted('save')?.[0]?.[0]).toEqual({
      category: 'Backend',
      question: 'O que é FastAPI?',
      answer: 'Um framework web moderno e rápido.',
      favorite: false
    })
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('deve limpar o formulario e emitir o evento close ao clicar no botao Cancelar', async () => {
    const wrapper = mount(KnowledgeFormModal, {
      props: { isOpen: true }
    })

    await wrapper.find('input').setValue('Temporario')
    
    const cancelButton = wrapper.find('button.border-slate-300')
    await cancelButton.trigger('click')

    expect(wrapper.emitted('close')).toBeTruthy()
  })
})
