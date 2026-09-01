<script setup>
import { ref } from 'vue'

import { calculate } from './services/calculatorApi'

const leftValue = ref('')
const rightValue = ref('')
const operation = ref('add')
const result = ref(null)
const errorMessage = ref('')
const isCalculating = ref(false)

async function calculateResult() {
  errorMessage.value = ''
  result.value = null

  if (leftValue.value === '' || rightValue.value === '') {
    errorMessage.value = 'Enter a number in both fields.'
    return
  }

  isCalculating.value = true

  try {
    result.value = await calculate({
      operation: operation.value,
      a: Number(leftValue.value),
      b: Number(rightValue.value),
    })
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
      <p class="eyebrow">Hello Agent</p>
      <h1 id="calculator-title">Calculator</h1>

      <form @submit.prevent="calculateResult">
        <label for="left-value">First number</label>
        <input
          id="left-value"
          v-model="leftValue"
          type="number"
          step="any"
          inputmode="decimal"
          required
        >

        <label for="operation">Operation</label>
        <select id="operation" v-model="operation">
          <option value="add">Add (+)</option>
          <option value="subtract">Subtract (−)</option>
          <option value="multiply">Multiply (×)</option>
          <option value="divide">Divide (÷)</option>
        </select>

        <label for="right-value">Second number</label>
        <input
          id="right-value"
          v-model="rightValue"
          type="number"
          step="any"
          inputmode="decimal"
          required
        >

        <button type="submit" :disabled="isCalculating">
          {{ isCalculating ? 'Calculating…' : 'Calculate' }}
        </button>
      </form>

      <section class="result" aria-live="polite" aria-labelledby="result-title">
        <h2 id="result-title">Result</h2>
        <output v-if="result !== null">{{ result }}</output>
        <p v-else>Enter values and calculate to see the result.</p>
      </section>

      <section class="error" aria-live="assertive" aria-labelledby="error-title">
        <h2 id="error-title">Error</h2>
        <p>{{ errorMessage || 'No errors.' }}</p>
      </section>
    </section>
  </main>
</template>

<style scoped>
:global(*) {
  box-sizing: border-box;
}

:global(body) {
  margin: 0;
  color: #2d2520;
  background: #f7f2eb;
  font-family: Inter, system-ui, sans-serif;
}

.calculator-page {
  display: grid;
  min-height: 100vh;
  padding: 2rem;
  place-items: center;
}

.calculator {
  width: min(100%, 28rem);
  padding: 2rem;
  background: #fffdf9;
  border: 1px solid #ded4c8;
  border-radius: 1rem;
  box-shadow: 0 1rem 3rem rgb(68 48 32 / 12%);
}

.eyebrow {
  margin: 0;
  color: #8a4b13;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

h1,
h2 {
  margin-top: 0;
}

h1 {
  margin-bottom: 1.5rem;
}

form {
  display: grid;
  gap: 0.55rem;
}

label {
  margin-top: 0.65rem;
  font-weight: 700;
}

input,
select,
button {
  min-height: 2.75rem;
  border-radius: 0.5rem;
  font: inherit;
}

input,
select {
  padding: 0.65rem 0.75rem;
  color: inherit;
  background: #fff;
  border: 1px solid #b9aa9b;
}

button {
  margin-top: 1rem;
  color: #fff;
  cursor: pointer;
  background: #a95312;
  border: 1px solid #8a430d;
  font-weight: 700;
}

button:hover:not(:disabled) {
  background: #843d0b;
}

button:disabled {
  cursor: wait;
  opacity: 0.65;
}

.result,
.error {
  margin-top: 1.5rem;
  padding: 1rem;
  border-radius: 0.5rem;
}

.result {
  background: #f5ead7;
}

.error {
  color: #7e1f1f;
  background: #fbe9e6;
}

.result h2,
.error h2,
.result p,
.error p {
  margin: 0;
}

.result output {
  display: block;
  margin-top: 0.4rem;
  font-size: 1.5rem;
  font-weight: 700;
}
</style>
