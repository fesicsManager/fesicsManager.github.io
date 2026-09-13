import { expect, test } from '../../fesics-react-web/node_modules/@playwright/test/index.mjs';

const CASES = [
  {
    name: 'mobile portrait stimulus response',
    viewport: { width: 390, height: 844 },
    child: '/fesicsExternal/milddle1BioGeo/01_stimulus_response_lab.html',
  },
  {
    name: 'mobile landscape sensory organs',
    viewport: { width: 844, height: 390 },
    child: '/fesicsExternal/milddle3Bio/01_sensory_organs_lab.html',
  },
];

for (const scenario of CASES) {
  test(scenario.name, async ({ page }, testInfo) => {
    await page.setViewportSize(scenario.viewport);
    await page.goto(`/tests/embed-resize-parent.html?child=${encodeURIComponent(scenario.child)}`);

    const frame = page.locator('iframe');
    await expect.poll(() => page.evaluate(() => {
      const child = window.__embedTest.frame.contentDocument;
      const body = child.body;
      const style = getComputedStyle(body);
      const expected = Math.ceil(Math.max(body.getBoundingClientRect().height, body.scrollHeight)
        + (parseFloat(style.marginTop) || 0) + (parseFloat(style.marginBottom) || 0));
      return window.__embedTest.heights.at(-1) === expected;
    })).toBe(true);
    const initial = await page.evaluate(() => {
      const child = window.__embedTest.frame.contentDocument;
      const body = child.body;
      const style = getComputedStyle(body);
      return {
        height: window.__embedTest.heights.at(-1),
        expected: Math.ceil(Math.max(body.getBoundingClientRect().height, body.scrollHeight)
          + (parseFloat(style.marginTop) || 0) + (parseFloat(style.marginBottom) || 0)),
        htmlClass: child.documentElement.className,
        bodyClass: body.className,
        minHeight: style.minHeight,
      };
    });
    expect(initial.height).toBe(initial.expected);
    expect(initial.height).toBeGreaterThan(0);
    expect(initial.htmlClass).toContain('fesics-embed-resize');
    expect(initial.bodyClass).toContain('fesics-embed-resize');
    expect(initial.minHeight).toBe('0px');
    await page.screenshot({ path: testInfo.outputPath('initial.png'), fullPage: true });

    await page.evaluate(() => {
      const child = window.__embedTest.frame.contentDocument;
      child.body.insertAdjacentHTML('beforeend', '<div data-test-growth style="height:240px"></div>');
    });
    await expect.poll(() => page.evaluate(() => window.__embedTest.heights.at(-1))).toBeGreaterThan(initial.height);
    const grown = await page.evaluate(() => window.__embedTest.heights.at(-1));

    await page.evaluate(() => window.__embedTest.frame.contentDocument.querySelector('[data-test-growth]').remove());
    await expect.poll(() => page.evaluate(() => window.__embedTest.heights.at(-1))).toBe(initial.height);
    expect(grown).toBeGreaterThan(initial.height);

    await page.evaluate(() => {
      const test = window.__embedTest;
      test.frame.contentWindow.postMessage({ type: 'fesics:embed-init', requestId: 'replay-request' }, location.origin);
    });
    await expect.poll(() => page.evaluate(() => window.__embedTest.heights.at(-1))).toBe(initial.height);

    await frame.evaluate((node) => node.contentWindow.postMessage({ type: 'fesics:embed-init', requestId: 'x'.repeat(257) }, location.origin));
    await page.waitForTimeout(100);
    expect(await page.evaluate(() => window.__embedTest.heights.at(-1))).toBe(initial.height);
  });
}

test('standalone page keeps viewport minimum height without handshake', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/fesicsExternal/milddle1BioGeo/01_stimulus_response_lab.html');
  await expect.poll(() => page.evaluate(() => getComputedStyle(document.body).minHeight)).toBe('844px');
  expect(await page.evaluate(() => document.documentElement.className)).not.toContain('fesics-embed-resize');
});

test('replays height after BFCache lifecycle and survives without ResizeObserver', async ({ page }) => {
  await page.addInitScript(() => { window.ResizeObserver = undefined; });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/tests/embed-resize-parent.html?child=%2FfesicsExternal%2Fmilddle1BioGeo%2F01_stimulus_response_lab.html');
  await expect.poll(() => page.evaluate(() => window.__embedTest.heights.length)).toBeGreaterThan(0);
  const before = await page.evaluate(() => window.__embedTest.heights[0]);
  await page.evaluate(() => window.__embedTest.frame.contentWindow.dispatchEvent(new Event('resize')));
  expect(before).toBeGreaterThan(0);
  const stableCount = await page.evaluate(() => window.__embedTest.heights.length);
  await page.evaluate(() => {
    const childWindow = window.__embedTest.frame.contentWindow;
    childWindow.dispatchEvent(new PageTransitionEvent('pagehide'));
    childWindow.dispatchEvent(new PageTransitionEvent('pageshow'));
  });
  await expect.poll(() => page.evaluate(() => window.__embedTest.heights.length)).toBeGreaterThan(stableCount);
  const replay = await page.evaluate(() => {
    const child = window.__embedTest.frame.contentDocument;
    const body = child.body;
    const style = getComputedStyle(body);
    return {
      height: window.__embedTest.heights.at(-1),
      expected: Math.ceil(Math.max(body.getBoundingClientRect().height, body.scrollHeight)
        + (parseFloat(style.marginTop) || 0) + (parseFloat(style.marginBottom) || 0)),
    };
  });
  expect(replay.height).toBe(replay.expected);
});

test('narrow embeds keep a minimum horizontal inset, wide ones stay untouched', async ({ page }) => {
  const child = '/fesicsExternal/milddle1BioGeo/01_stimulus_response_lab.html';
  const readInset = () => page.evaluate(() => {
    const style = getComputedStyle(window.__embedTest.frame.contentDocument.body);
    return { left: parseFloat(style.paddingLeft) || 0, right: parseFloat(style.paddingRight) || 0 };
  });

  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(`/tests/embed-resize-parent.html?child=${encodeURIComponent(child)}`);
  await expect.poll(async () => (await readInset()).left).toBeGreaterThanOrEqual(16);
  expect((await readInset()).right).toBeGreaterThanOrEqual(16);

  // 좁은 화면에서 보장한 여백이 넓은 화면으로 돌아가면 원래 스타일로 복귀해야 한다.
  await page.setViewportSize({ width: 1280, height: 900 });
  await expect.poll(() => page.evaluate(() => {
    const body = window.__embedTest.frame.contentDocument.body;
    return body.style.getPropertyValue('padding-left') === '' && body.style.getPropertyValue('padding-right') === '';
  })).toBe(true);
});
