
function roundUp(num, precision) {
  return Math.ceil(num / precision) * precision
}

function roundDown(num, precision) {
  return Math.floor(num / precision) * precision
}

function countDigits(num) {
  let count = 0
  while (num >= 1) {
    num = num / 10
    count++
  }
  return count
}

function round(fn, num, otherNum) {
  /**
   * FIXME: this logic more or less works, but clearly, it's shit to understand.
   * somewhere out there in the land of maths _must_ be a clean way to do this.
   */
  let digits = countDigits(num)

  if (num > 50 && (Math.abs(num - otherNum) > 1)) {
    if (fn == roundUp) {
      num = Math.ceil(num)
    } else {
      num = Math.floor(num)
    }
  }

  if (num % (10 ** (digits - 1)) === 0 || num % 10 === 0) {
    return num
  }

  let precision = 10 ** (digits - 2)
  if (num < 10) {
    precision = 0.1
  }

  if (num > 1000 && num % precision === 0) {
    return num
  }

  // really while (rounded == num) { ... } but, floating point
  let rounded = num
  while (Math.abs(rounded - num) < .000001) {
    rounded = fn(num, precision)
    precision *= 10
  }
  return rounded
}

export function niceLogMax(min, max) {
  return round(roundUp, max, min)
}

export function niceLogMin(min, max) {
  if (min < 2) {
    return Math.max(0.01, min * 0.8)
  }
  return Math.max(0.01, round(roundDown, min, max))
}


export function getLogTickValues(logMin, logMax) {
  const steps = [0.01, 0.05, 0.1, 0.2, 0.25, 0.5, 1]
  let multiplier = 1,
      yInterval = (logMax - logMin) / 10,
      searching = true

  while (searching) {
    for (let i = 1; i < steps.length; i++) {
      const step = steps[i] * multiplier
      const numLines = (logMax - logMin) / (steps[i-1] * multiplier)
      if (yInterval <= step && numLines < 16) {
        yInterval = steps[i-1] * multiplier
        searching = false
        break
      }
    }
    multiplier *= 10
  }

  let tickValues = []
  for (let i = 0;; i++) {
    const tick = logMax - (yInterval * i)
    if (tick < logMin) {
      break
    }
    tickValues.push(tick)
  }

  return tickValues
}
