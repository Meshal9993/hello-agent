<script setup>
import { ref } from 'vue'

import { calculate } from './services/calculatorApi'

const operationSymbols = {
  add: '+',
  subtract: '−',
  multiply: '×',
  divide: '÷',
}

const displayValue = ref('0')
const firstValue = ref(null)
const operation = ref(null)
const waitingForOperand = ref(false)
const expression = ref('')
const errorMessage = ref('')
const isCalculating = ref(false)

function inputDigit(digit) {
  if (isCalculating.value) return

  errorMessage.value = ''

  if (waitingForOperand.value || displayValue.value === '0') {
    displayValue.value = digit
    waitingForOperand.value = false
    return
  }

  if (displayValue.value.replace('-', '').replace('.', '').length < 12) {
    displayValue.value += digit
  }
}

function inputDecimal() {
  if (isCalculating.value) return

  errorMessage.value = ''

  if (waitingForOperand.value) {
    displayValue.value = '0.'
    waitingForOperand.value = false
  } else if (!displayValue.value.includes('.')) {
    displayValue.value += '.'
  }
}

function chooseOperation(nextOperation) {
  if (isCalculating.value) return

  errorMessage.value = ''

  if (firstValue.value === null || !waitingForOperand.value) {
    firstValue.value = Number(displayValue.value)
  }

  operation.value = nextOperation
  expression.value = `${formatValue(firstValue.value)} ${operationSymbols[nextOperation]}`
  waitingForOperand.value = true
}

function clearCalculator() {
  displayValue.value = '0'
  firstValue.value = null
  operation.value = null
  waitingForOperand.value = false
  expression.value = ''
  errorMessage.value = ''
}

function backspace() {
  if (isCalculating.value || waitingForOperand.value) return

  errorMessage.value = ''

  if (displayValue.value.length === 1 || /^-\d$/.test(displayValue.value)) {
    displayValue.value = '0'
  } else {
    displayValue.value = displayValue.value.slice(0, -1)
  }
}

function toggleSign() {
  if (isCalculating.value || displayValue.value === '0') return

  displayValue.value = displayValue.value.startsWith('-')
    ? displayValue.value.slice(1)
    : `-${displayValue.value}`
}

function applyPercent() {
  if (isCalculating.value) return

  displayValue.value = formatValue(Number(displayValue.value) / 100)
  errorMessage.value = ''
}

function formatValue(value) {
  return Number.parseFloat(Number(value).toPrecision(12)).toString()
}

async function calculateResult() {
  if (
    isCalculating.value ||
    firstValue.value === null ||
    operation.value === null ||
    waitingForOperand.value
  ) {
    errorMessage.value = 'Enter a value, choose an operation, then enter another value.'
    return
  }

  const secondValue = Number(displayValue.value)
  const selectedOperation = operation.value
  errorMessage.value = ''
  isCalculating.value = true

  try {
    const result = await calculate({
      operation: selectedOperation,
      a: firstValue.value,
      b: secondValue,
    })

    expression.value = `${formatValue(firstValue.value)} ${operationSymbols[selectedOperation]} ${formatValue(secondValue)} =`
    displayValue.value = formatValue(result)
    firstValue.value = null
    operation.value = null
    waitingForOperand.value = true
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    isCalculating.value = false
  }
}
</script>

<template>
  <main class="calculator-page">
    <section class="calculator" aria-labelledby="calculator-title">
      <h1 id="calculator-title" class="visually-hidden">Hello Agent calculator</h1>

      <header class="calculator-header" aria-hidden="true">
        <div class="window-controls">
          <span class="window-dot window-dot--red"></span>
          <span class="window-dot window-dot--yellow"></span>
          <span class="window-dot window-dot--gray"></span>
        </div>
      </header>

      <section class="display" aria-live="polite" aria-atomic="true">
        <p class="expression">{{ expression || 'Ready' }}</p>
        <output class="display-value">{{ isCalculating ? '…' : displayValue }}</output>
        <p class="error-message" role="alert">{{ errorMessage }}</p>
      </section>

      <div class="keypad" aria-label="Calculator keypad">
        <button type="button" class="key key--utility" aria-label="Backspace" @click="backspace">
          ⌫
        </button>
        <button type="button" class="key key--utility" aria-label="Clear all" @click="clearCalculator">
          AC
        </button>
        <button type="button" class="key key--utility" aria-label="Percent" @click="applyPercent">
          %
        </button>
        <button
          type="button"
          class="key key--operation"
          :class="{ 'is-selected': operation === 'divide' }"
          :aria-pressed="operation === 'divide'"
          aria-label="Divide"
          @click="chooseOperation('divide')"
        >
          ÷
        </button>

        <button type="button" class="key" aria-label="Seven" @click="inputDigit('7')">7</button>
        <button type="button" class="key" aria-label="Eight" @click="inputDigit('8')">8</button>
        <button type="button" class="key" aria-label="Nine" @click="inputDigit('9')">9</button>
        <button
          type="button"
          class="key key--operation"
          :class="{ 'is-selected': operation === 'multiply' }"
          :aria-pressed="operation === 'multiply'"
          aria-label="Multiply"
          @click="chooseOperation('multiply')"
        >
          ×
        </button>

        <button type="button" class="key" aria-label="Four" @click="inputDigit('4')">4</button>
        <button type="button" class="key" aria-label="Five" @click="inputDigit('5')">5</button>
        <button type="button" class="key" aria-label="Six" @click="inputDigit('6')">6</button>
        <button
          type="button"
          class="key key--operation"
          :class="{ 'is-selected': operation === 'subtract' }"
          :aria-pressed="operation === 'subtract'"
          aria-label="Subtract"
          @click="chooseOperation('subtract')"
        >
          −
        </button>

        <button type="button" class="key" aria-label="One" @click="inputDigit('1')">1</button>
        <button type="button" class="key" aria-label="Two" @click="inputDigit('2')">2</button>
        <button type="button" class="key" aria-label="Three" @click="inputDigit('3')">3</button>
        <button
          type="button"
          class="key key--operation"
          :class="{ 'is-selected': operation === 'add' }"
          :aria-pressed="operation === 'add'"
          aria-label="Add"
          @click="chooseOperation('add')"
        >
          +
        </button>

        <button type="button" class="key" aria-label="Toggle sign" @click="toggleSign">+/−</button>
        <button type="button" class="key" aria-label="Zero" @click="inputDigit('0')">0</button>
        <button type="button" class="key" aria-label="Decimal point" @click="inputDecimal">.</button>
        <button
          type="button"
          class="key key--operation key--equals"
          :disabled="isCalculating"
          aria-label="Equals"
          @click="calculateResult"
        >
          =
        </button>
      </div>
    </section>
  </main>
</template>

<style scoped>
:global(*) {
  box-sizing: border-box;
}

:global(body) {
  margin: 0;
  color: #f8f8f8;
  background: #e8e5df;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
}

button {
  font: inherit;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.calculator-page {
  display: grid;
  min-height: 100vh;
  padding: 1.5rem;
  place-items: center;
}

.calculator {
  width: min(100%, 28rem);
  padding: 1.6rem;
  overflow: hidden;
  background: #1e1e1f;
  border: 1px solid #454547;
  border-radius: 2.6rem;
  box-shadow:
    inset 0 0 0 1px #111,
    0 1.5rem 3.5rem rgb(26 23 20 / 28%);
}

.calculator-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.window-controls {
  display: flex;
  gap: 0.8rem;
}

.window-dot {
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
}

.window-dot--red {
  background: #ff5f57;
}

.window-dot--yellow {
  background: #ffbd2e;
}

.window-dot--gray {
  background: #555557;
}

.display {
  display: flex;
  min-height: 10rem;
  padding: 1.5rem 0.25rem 1rem;
  flex-direction: column;
  align-items: flex-end;
  justify-content: flex-end;
}

.expression,
.error-message {
  min-height: 1.35rem;
  margin: 0;
}

.expression {
  color: #9e9ea1;
  font-size: 1.3rem;
}

.display-value {
  max-width: 100%;
  overflow: hidden;
  color: #f4f4f5;
  font-size: clamp(3rem, 16vw, 4.7rem);
  font-weight: 300;
  letter-spacing: -0.055em;
  line-height: 1.05;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.error-message {
  max-width: 100%;
  padding-top: 0.35rem;
  color: #ff938c;
  font-size: 0.82rem;
  text-align: right;
}

.keypad {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.75rem;
}

.key {
  aspect-ratio: 1;
  min-width: 0;
  color: #f8f8f8;
  cursor: pointer;
  background: #4b4b4d;
  border: 1px solid #666669;
  border-radius: 50%;
  box-shadow: inset 0 1px 0 rgb(255 255 255 / 8%);
  font-size: clamp(1.35rem, 7vw, 2.25rem);
  font-weight: 400;
  transition:
    background 120ms ease,
    transform 120ms ease;
}

.key:hover:not(:disabled) {
  background: #5b5b5e;
}

.key:active:not(:disabled) {
  transform: scale(0.95);
}

.key:focus-visible {
  outline: 3px solid #fff;
  outline-offset: 2px;
}

.key--utility {
  background: #777779;
  border-color: #969699;
  font-size: clamp(1rem, 5vw, 1.65rem);
}

.key--utility:hover:not(:disabled) {
  background: #89898c;
}

.key--operation {
  color: #fff;
  background: #ff9500;
  border-color: #ffab32;
}

.key--operation:hover:not(:disabled),
.key--operation.is-selected {
  color: #ff9500;
  background: #fff;
}

.key--equals:disabled {
  cursor: wait;
  opacity: 0.65;
}

@media (max-width: 28rem) {
  .calculator-page {
    padding: 0;
  }

  .calculator {
    min-height: 100vh;
    border-radius: 0;
  }
}
</style>
