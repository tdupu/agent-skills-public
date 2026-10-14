---
name: browser
description: Tested JavaScript techniques for driving Research.gov and UVMClick in Chrome (claude-in-chrome tools). Read before acting on either site.
---

# Driving Research.gov and UVMClick

Tested 2026-10-05 with the claude-in-chrome tools. The PI signs in;
never type a password. Read pages with `get_page_text`; act with
`find` + `computer` clicks, or with the JavaScript below.

## Research.gov (Ember single-page app)

**Setting a text field** so Ember sees the change. Plain `.value =` is
ignored. Use the native setter and fire the events:

```js
const set=(el,v)=>{const s=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;
  s.call(el,v);['input','change','blur'].forEach(e=>el.dispatchEvent(new Event(e,{bubbles:true})))};
```

**Finding budget fields.** Their aria-labels contain " - " and odd
spacing, so normalize before matching:
`label.replace(/[\s\-]/g,'')`.

**The indirect-cost base must be typed for real.** Use `computer`
`left_click` on the field, then `type`; setting it by script leaves the
total stale.

**Budget years.** Add years 2 and 3 by copying year 1, then edit them.
Save after each year. The first save sometimes returns a system error;
retry once.

**Links that don't navigate** (e.g. "Manage Personnel"): read the
link's `href` and `navigate` to it.

**Session expiry** lands on an NSF password page. Stop and ask the PI
to sign in.

## UVMClick (Huron Grants SmartForms)

**Pop-ups are blocked.** "Add", "[Edit]" and activity buttons call
`window.open`. Override it so the target opens in the same tab:

```js
window.open=function(u){location.href=u;return window;};
```

Some edits still open in a new tab. Look for it with `tabs_context`.

**In-page dialogs are iframes** ("Submit a Document", "Add Personnel
Cost", "Add General Cost"). Reach their fields with
`[...document.querySelectorAll('iframe')].find(f=>{try{return f.contentDocument.querySelector('select,input')}catch(e){}}).contentDocument`.
Click their OK through that document; coordinate clicks on the OK
button can hang the renderer.

**Uploading into a "Drag and drop files" zone.** First load the files
into a temporary input:

```js
const i=document.createElement('input');i.type='file';i.multiple=true;i.id='_tmpUp';document.body.appendChild(i);
```

Give it an aria-label, find its `ref`, and fill it with `file_upload`.
Then drop the files onto the zone's table:

```js
const zones=[...document.querySelectorAll('span,div')].filter(e=>e.childElementCount===0&&/Drag and drop files/i.test(e.textContent));
const dt=new DataTransfer();[...document.getElementById('_tmpUp').files].forEach(f=>dt.items.add(f));
['dragenter','dragover','drop'].forEach(t=>zones[K].closest('table').dispatchEvent(new DragEvent(t,{bubbles:true,cancelable:true,dataTransfer:dt})));
```

Here `K` is the zone's index, so match it to the section label first.

**Uploading into a single-file dialog** ("Upload" button). If
`file_upload` landed on `_tmpUp`, move the file across:
`iframeInput.files = dt.files` plus a `change` event. Then click OK.

**Radio groups.** `input[type=radio][value=no]`, filtered to visible
ones (`offsetParent`), then `.click()`.

**Grid editors** (Personnel Costs, General Costs). Click Edit, set the
inputs, then click the grid's own **Save** button before Continue.
Continue alone discards the grid edits.

**The PI may click too.** If the page moved on its own, re-read it
before acting.

## Gmail attachments

Updating a draft through the Gmail API with no `attachments` strips the
existing ones. To change recipients on a draft that has attachments,
open the draft in Gmail and click the chip's ×. To attach files, give
the compose window's `input[type=file]` an aria-label, find it, and call
`file_upload` (the limit is 10 MB per call).
