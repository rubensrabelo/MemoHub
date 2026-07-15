import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseButton from './BaseButton.vue'

describe('BaseButton.vue', () => {
  it('deve renderizar o conteudo enviado pelo slot corretamente', () => {
    const wrapper = mount(BaseButton, {
      slots: { default: 'Enviar' }
    })

    expect(wrapper.text()).toBe('Enviar')
  })

  it('deve aplicar as classes corretas para a variante primary por padrao', () => {
    const wrapper = mount(BaseButton)

    expect(wrapper.classes()).toContain('bg-primary')
    expect(wrapper.classes()).toContain('text-white')
  })

  it('deve aplicar as classes de outline corretas para a variante secondary', () => {
    const wrapper = mount(BaseButton, {
      props: { variant: 'secondary' }
    })

    expect(wrapper.classes()).toContain('border-2')
    expect(wrapper.classes()).toContain('border-primary')
    expect(wrapper.classes()).toContain('text-primary')
  })

  it('deve aplicar as classes corretas para a variante danger', () => {
    const wrapper = mount(BaseButton, {
      props: { variant: 'danger' }
    })

    expect(wrapper.classes()).toContain('bg-danger')
    expect(wrapper.classes()).toContain('text-white')
  })

  it('deve desativar o botao e aplicar a propriedade disabled quando a prop disabled for true', () => {
    const wrapper = mount(BaseButton, {
      props: { disabled: true }
    })

    const button = wrapper.find('button')
    expect(button.element.disabled).toBe(true)
  })

  it('deve exibir o spinner de carregamento e desativar o botao no estado loading', () => {
    const wrapper = mount(BaseButton, {
      props: { loading: true },
      slots: { default: 'Salvar' }
    })

    const button = wrapper.find('button')
    expect(button.element.disabled).toBe(true)

    const spinner = wrapper.find('.animate-spin')
    expect(spinner.exists()).toBe(true)
    expect(wrapper.text()).not.toContain('Salvar')
  })
})
