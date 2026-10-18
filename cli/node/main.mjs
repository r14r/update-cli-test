#!/usr/bin/env node
// Dependency-free Node.js CLI fixture.
export function compute(a, b) {
  if (!Number.isSafeInteger(a) || !Number.isSafeInteger(b)) {
    throw new TypeError('safe integers required')
  }
  return a + b
}

export function run(args) {
  if (args[0] === 'health' && args.length === 1) return { status: 'ok', runtime: 'node' }
  if (args[0] === 'add' && args.length === 3) return { result: compute(Number(args[1]), Number(args[2])) }
  throw new Error('usage: fixture-node health | add INT INT')
}

if (process.argv[1] && import.meta.url === new URL(`file://${process.argv[1]}`).href) {
  try { console.log(JSON.stringify(run(process.argv.slice(2)))) }
  catch (error) { console.error(error.message); process.exitCode = 2 }
}
