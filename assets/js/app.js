import { OrderFindParcel } from './core/orderFindParcel.js'
import { OrderForm } from './core/orderForm.js'

document.addEventListener('DOMContentLoaded', () => {
  const formOrder = new OrderForm() // eslint-disable-line no-new

  const onPropertySelect = (value) => {
    formOrder.activate()
    const input = formOrder.inputPropertyId
    if (input) {
      input.value = value
    }
  }

  const onPropertyReset = () => {
    formOrder.deactivate()
    const input = formOrder.inputPropertyId
    if (input) {
      input.value = null
    }
  }

  new OrderFindParcel(onPropertySelect, onPropertyReset) // eslint-disable-line no-new
})
