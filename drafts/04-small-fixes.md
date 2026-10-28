# Small fixes (each checked against the live docs on 2026-10-28)

## Broken link on the onboarding page
**Page:** https://linear.app/docs/joining-your-team-on-linear
"Our favorite shortcut is **Peek**" links to `https://linear.app/docs/peek`, which returns 404. This is
the page new members are sent to on their first day. Link to the Peek section of the keyboard-shortcuts
page instead, or restore the page.

## "Canceled" vs "cancelled"
The API's state type is always `canceled`. The docs use "canceled" 37 times on 23 pages and "cancelled"
6 times on 6 pages; three pages use both. Reported in #1116 (closed as completed, April 2026), still
present. Change "cancelled" to "canceled" on:

| Page | Sentence |
|---|---|
| /docs/customer-requests | "…completed or cancelled." |
| /docs/front | "…when it's completed, cancelled or a comment is made." |
| /docs/projects | "…recently created, then cancelled and completed." |
| /docs/salesforce | "…has been completed or cancelled." |
| /docs/delete-archive-issues | "(completed or cancelled category)" |
| /docs/figma | "…hide completed or cancelled issues…" |
