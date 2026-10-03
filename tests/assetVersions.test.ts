import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const script = resolve(dirname(fileURLToPath(import.meta.url)), '../scripts/version-assets.ts');

test('CLI versions local JS/CSS from their contents and refreshes the URL when an asset changes', () => {
  const root = mkdtempSync(join(tmpdir(), 'fesics-pages-versions-'));
  try {
    mkdirSync(join(root, 'fesicsExternal/lab'), { recursive: true });
    const js = join(root, 'fesicsExternal/fxsound.js');
    const css = join(root, 'fesicsExternal/style.css');
    const html = join(root, 'fesicsExternal/lab/index.html');
    writeFileSync(js, 'window.fx = 1;');
    writeFileSync(css, 'body { color: red; }');
    writeFileSync(
      html,
      '<script src="../fxsound.js?mode=lesson#top"></script>\n<link rel="stylesheet" href="/fesicsExternal/style.css">\n<script src="https://cdn.example.com/external.js"></script>',
    );
    assert.notEqual(spawnSync(process.execPath, [script, root, '--check']).status, 0);
    execFileSync(process.execPath, [script, root]);
    const first = readFileSync(html, 'utf8');
    const jsHash = createHash('sha256').update('window.fx = 1;').digest('hex').slice(0, 12);
    const cssHash = createHash('sha256').update('body { color: red; }').digest('hex').slice(0, 12);
    assert.ok(first.includes(`../fxsound.js?mode=lesson&v=${jsHash}#top`));
    assert.ok(first.includes(`/fesicsExternal/style.css?v=${cssHash}`));
    assert.ok(first.includes('src="https://cdn.example.com/external.js"'));
    execFileSync(process.execPath, [script, root, '--check']);
    execFileSync(process.execPath, [script, root]);
    assert.equal(readFileSync(html, 'utf8'), first);
    writeFileSync(js, 'window.fx = 2;');
    assert.notEqual(spawnSync(process.execPath, [script, root, '--check']).status, 0);
    execFileSync(process.execPath, [script, root]);
    const second = readFileSync(html, 'utf8');
    assert.ok(!second.includes(`v=${jsHash}`));
    assert.ok(second.includes(`v=${createHash('sha256').update('window.fx = 2;').digest('hex').slice(0, 12)}`));
    assert.ok(second.includes(`style.css?v=${cssHash}`));
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('a missing local asset fails before changing any HTML', () => {
  const root = mkdtempSync(join(tmpdir(), 'fesics-pages-missing-'));
  try {
    mkdirSync(join(root, 'fesicsExternal/lab'), { recursive: true });
    const html = join(root, 'fesicsExternal/lab/index.html');
    const source = '<script src="../missing.js"></script>';
    writeFileSync(html, source);
    assert.notEqual(spawnSync(process.execPath, [script, root]).status, 0);
    assert.equal(readFileSync(html, 'utf8'), source);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});
