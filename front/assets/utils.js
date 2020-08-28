export function setPopupPosition(target_selector, popup_selector) {
  var target = document.querySelector(target_selector)
  var targetRect = target.getBoundingClientRect()
  var popup = document.querySelector(popup_selector)
  var popupRect = popup.getBoundingClientRect()
  var menu = document.querySelector('#menu')
  var menuRect = menu.getBoundingClientRect()
  let width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0)
  let height = Math.max(document.documentElement.clientHeight, window.innerHeight || 0)
  const doc = document.documentElement
  var containerScrollLeft = (window.pageXOffset || doc.scrollLeft) - (doc.clientLeft || 0)
  var containerScrollTop = (window.pageYOffset || doc.scrollTop) - (doc.clientTop || 0)

  var top = targetRect.top
  var left = parseInt(target.style.left.substring(0, target.style.left.length - 2))

  if (top + popupRect.height >= height - 5) {
    top -=  popupRect.height + 20
    if (top < 0) {
      top = 0
    }
  } else {
    top += 20
  }

  if (left + popupRect.width + menuRect.width >= width - 5) {
    left -= popupRect.width + 20
    if (left < 0) {
      left = 0
    }
  } else {
    left += 20
  }

  popup.style.top = `${top}px`
  popup.style.left = `${left}px`
}

export function log (eventValue) {

  let { on, id, key, value, params, obj, data, schema, parent, index, event } = eventValue

  console.log(`-- v-form-base event ---------------------------------------`)
  console.log(`Event: ${on} | Key: ${key}@${id} | Value:`,value)
  // console.log(`Formbase-ID:${id}`)
  // console.log(`Key:${key}`)
  // console.log(`Value:`, value)
  if (params) console.log(`Params:`, params)
  console.log('Value Object:', data)
  console.log('Schema Object:', schema)
  console.log('Key Object:', obj)
  // if (parent) console.log(`Parent ID:${parent.id} | Parent:`, parent)
  // if (index == true) console.log(`Index of Array:>${index}<`)
  // if (event) console.log('Event:', event)

  return eventValue
}
