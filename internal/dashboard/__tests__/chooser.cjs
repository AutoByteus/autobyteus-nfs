// Actual embedded chooser, real directory HTTP; only response delivery is held.
// Reproduces API-F001 without a VM, sudo, storage mutation or timing luck.
const assert = require('node:assert/strict');
const { join } = require('node:path');
module.exports = async function chooser(page, home, method, eventually) {
  const input = page.locator('#directory-path');
  const choose = page.locator('#choose-directory');
  let release, held = false, delivered = false, intercepted = false;
  const gate = new Promise(resolve => { release = resolve; });
  const pattern = '**/api/directories';
  const route = async route => {
    if (route.request().method() !== method || intercepted) return route.continue();
    intercepted = true;
    // Keep the actual Go response and status; pause delivery, not its contents.
    const response = await route.fetch();
    held = true;
    await gate;
    await route.fulfill({ response });
    delivered = true;
  };
  await page.route(pattern, route);
  try {
    await page.locator('#browse').click();
    await input.waitFor({ state: 'visible' });
    await eventually(() => assert.ok(held, `${method} response not held`));
    assert.equal(await input.isEnabled(), true, 'manual path remains editable while listing');
    const path = join(home, 'visible-folder'), split = Math.floor(path.length / 2);
    // Actual keyboard editing begins BEFORE background response completion.
    await input.focus(); await page.keyboard.press('Meta+A');
    await page.keyboard.type(path.slice(0, split));
    release();
    await eventually(() => assert.ok(delivered));
    await eventually(async () => assert.ok((await page.locator('#directory-message').textContent()).includes('Choose this directory')));
    assert.equal(await input.inputValue(), path.slice(0, split), 'background listing replaced the active draft');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'directory-path');
    await page.keyboard.type(path.slice(split));
    assert.equal(await input.inputValue(), path, 'later keys must append to the draft, not the listing path');
    assert.equal(await choose.isEnabled(), false, 'unlisted draft must not silently choose previous listing');

    // Same settled-keyboard control as API07; explicit List submits the exact edit.
    await input.focus(); await page.keyboard.press('Meta+A'); await page.keyboard.type(path);
    assert.equal(await input.inputValue(), path);
    await page.keyboard.press('Enter');
    await eventually(async () => assert.equal(await choose.isEnabled(), true));
    assert.equal(await input.inputValue(), path);
    await page.locator('#directory-parent').click();
    await eventually(async () => { assert.equal(await choose.isEnabled(), true); assert.equal(await input.inputValue(), home); });
    const names = await page.locator('#directory-list').innerText();
    assert.ok(names.includes('visible-folder')); assert.ok(!names.includes('private-file'));
    await page.locator('#directory-list button').filter({ hasText: 'visible-folder' }).click();
    await eventually(async () => { assert.equal(await choose.isEnabled(), true); assert.equal(await input.inputValue(), path); });
    await choose.click(); assert.equal(await page.locator('#source').inputValue(), path);

    // Reopening seeds from the selected source. A failed explicit listing retains
    // its text for correction; editing it never enables an unrelated selection.
    await page.locator('#browse').click();
    await eventually(async () => { assert.equal(await choose.isEnabled(), true); assert.equal(await input.inputValue(), path); });
    const missing = join(home, 'not-created');
    await input.fill(missing); await page.keyboard.press('Enter');
    await eventually(async () => assert.ok((await page.locator('#directory-message').textContent()).includes('no such file')));
    assert.equal(await input.inputValue(), missing); assert.equal(await choose.isEnabled(), false);
    await input.fill(home); assert.equal(await choose.isEnabled(), false);
    await page.keyboard.press('Enter');
    await eventually(async () => assert.equal(await choose.isEnabled(), true));
    // Leave the chooser open for actual rendered-result inspection/screenshot.
    assert.equal(await input.inputValue(), home);
    return { method, draft: 'preserved across response', settled: 'preserved', explicitList: 'Pass', parent: 'Pass', child: 'Pass', selection: 'Pass', failedList: 'Pass' };
  } finally {
    release(); await page.unroute(pattern, route);
  }
};
