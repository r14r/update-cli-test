import test from 'node:test'
import assert from 'node:assert/strict'
import { compute, run } from './main.mjs'

test('health fixture', () => assert.deepEqual(run(['health']), {status: 'ok', runtime: 'node'}))
test('addition', () => assert.equal(compute(20, 22), 42))
test('invalid input', () => assert.throws(() => compute(1.5, 2), /safe integers/))
