import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseInput from './BaseInput.vue'

describe('BaseInput.vue', () => {
  it('deve renderizar o label apenas quando a prop label for enviada', async () => {
    const wrapperWithoutLabel = mount(BaseInput)
    expect(wrapperWithoutLabel.find('label').exists()).toBe(false)

    const wrapperWithLabel = mount(BaseInput, {
      props: { label: 'Nome Completo' }
    })
    expect(wrapperWithLabel.find('label').exists()).toBe(true)
    expect(wrapperWithLabel.find('label').text()).toBe('Nome Completo')
  })

  it('deve emitir o evento update:modelValue com o valor correto ao digitar no input', async () => {
    const wrapper = mount(BaseInput, {
      props: { modelValue: '' }
    })

    const input = wrapper.find('input')
    await input.setValue('Minha anotação')

    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['Minha anotação'])
  })

  it('deve passar corretamente as propriedades de tipo e placeholder para a tag input native', () => {
    const wrapper = mount(BaseInput, {
      props: {
        type: 'password',
        placeholder: 'Digite sua senha'
      }
    })

    const input = wrapper.find('input')
    expect(input.attributes('type')).toBe('password')
    expect(input.attributes('placeholder')).toBe('Digite sua senha')
  })

  it('deve renderizar a mensagem de erro e aplicar as classes visuais de perigo quando houver erro', () => {
    const wrapper = mount(BaseInput, {
      props: { error: 'Campo obrigatorio' }
    })

    const errorSpan = wrapper.find('span')
    expect(errorSpan.exists()).toBe(true)
    expect(errorSpan.text()).toBe('Campo obrigatorio')

    const input = wrapper.find('input')
    expect(input.classes()).toContain('border-danger')
    expect(input.classes()).toContain('focus:ring-danger/20')
    expect(input.classes()).not.toContain('border-(--border-color)')
  })
})
