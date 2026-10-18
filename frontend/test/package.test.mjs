import test from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs'

const pkg = JSON.parse(fs.readFileSync(new URL('../package.json', import.meta.url)))
test('Nuxt UI is configured', () => {
  assert.ok(pkg.dependencies['@nuxt/ui'])
  assert.ok(pkg.dependencies.nuxt)
})
