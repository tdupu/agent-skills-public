# Preparing a GitHub form in Chrome for the human

Only when the human asks, and only with text the human approved. Fill, verify, hand
over; the human edits and clicks.

- Issue-form textareas and the PR body are React-controlled. Observed 2026-10-18: raw
  paste and URL query parameters did not register in issue-form textareas. Set each
  value with the native setter and fire `input` and `change`:

  ```js
  const el = document.querySelector('<selector>');
  const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement : HTMLInputElement;
  Object.getOwnPropertyDescriptor(proto.prototype, 'value').set.call(el, text);
  el.dispatchEvent(new Event('input', { bubbles: true }));
  el.dispatchEvent(new Event('change', { bubbles: true }));
  ```

- No Enter in single-line inputs (it can submit).
- Read every value back from the page and compare it with the approved text.
- Then stop touching the tab.
- Never click submit or Create, sign in, enter secrets or 2FA codes, fill anti-bot
  fields, or open settings pages.
