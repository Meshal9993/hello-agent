const API_PREFIX = '/api'

/**
 * Request a calculator result from the backend.
 *
 * @param {{ operation: string, a: number, b: number }} calculation
 * @returns {Promise<number>}
 */
export async function calculate({ operation, a, b }) {
  const query = new URLSearchParams({ a: String(a), b: String(b) })
  const response = await fetch(`${API_PREFIX}/${operation}?${query}`)
  const body = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(body.detail || 'The calculation could not be completed.')
  }

  return body.result
}
