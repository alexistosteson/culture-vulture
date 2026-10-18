Session name: Act-now alerts venue subscriptions

# Handoff — act-now alerts: venue email sign-ups (2026-10-18)

Folder: `bay-week` main checkout. No branch yet; nothing committed. This file is
untracked on `main` — commit it on the step-4 branch, not on `main`.

**The subscription mailbox's address is never written to any file — the
repository is public.** The owner gives it in chat. Sign-ups use
`<account>+<tag>@gmail.com`. If you need it, ask the owner for it.

## The owner's request (four steps, verbatim in substance)

1. Candidate table of venues with email lists — **done and approved, narrowed**
   (below).
2. Sign up in the built-in browser with the `+tag` address. **Pause before
   submitting each form** (owner taps Submit in the next-step box each time).
   Owner handles any CAPTCHA, account creation or password. If a form rejects
   the `+`, use the plain address and note it. **Using the owner's name is fine
   where a form requires one** (owner, 2026-10-18).
3. Confirm: use the Gmail connector to find each confirmation email. Open a
   confirmation link **only** if it comes from the sender just signed up with,
   and **show the owner first**. Click no other link in any email; never send or
   forward mail.
4. Record, on a branch: write `specs/act-now-alerts.md` as a short-form probe
   spec — subscribed sources (venue, tag, date subscribed; **never the
   address**). Update the BACKLOG.md "Act-now alerts" row: the Gmail connector
   can send mail, a third way to deliver alerts. Run `bash scripts/verify.sh`;
   merge to `main` if it exits 0.

## Owner rulings this session (2026-10-18)

- **Subscribe only where the weekly check is unreliable, plus rare one-off
  events** — not every venue. Unreliable = unreached in ≥2 of the 5 weekly
  reports that record unreached venues (14 Sep – 12 Oct), and not fixed since.
- **No daily page checks at all.** The job is surfacing an *announced* event's
  on-sale date ahead of time ("tickets for X on sale from date Y"), not checking
  pages after the fact. A daily check also can't reach a site that refuses the
  reader — frequency doesn't fix access. (Earlier draft proposed daily checks of
  DNA Lounge, The Midway and the opera costume-sale page; all withdrawn.)
- Stern Grove added (my suggestion, approved): its free tickets go by email lottery.

## The 12 approved sign-ups — progress

| # | Venue | Tag | Signup page | Status |
|---|---|---|---|---|
| 1 | 1015 Folsom | 1015 | https://1015.com/#signup | Done — page said "Thank you!" (phone left blank) |
| 2 | Chase Center | chase | footer form on https://www.chasecenter.com/ (email-only form, not the one asking zip) | Submitted — no on-page message; the request to its Insider sign-up service was sent. Check for an email |
| 3 | SFJAZZ | sfjazz | https://pages.wordfly.com/sfjazz/pages/Subscribe/ | Submitted — **needs confirmation link** from email (double opt-in) |
| 4 | Z Space | zspace | https://mailchi.mp/zspace/z-space-mailing-list | Done — "Success! You've been added" |
| 5 | Fort Mason Center | fortmason | https://fortmason.org/sign-up-for-our-e-news/ | Done — confirmed on page |
| 6 | ODC Theater | odc | https://odcdance.us9.list-manage.com/subscribe?u=6a1e1838ba5169edd3ea4131e&id=78593abf6e | Done — confirmed on page (name required; Performances + Events ticked) |
| 7 | SF Playhouse | sfplayhouse | https://www.sfplayhouse.org/join-our-email-list/ | Done — confirmed on page after the owner solved its robot check (failed twice first: the tick expires in ~2 minutes, so the owner should tick and press Subscribe straight away). Name given; News and Promotions ticked |
| 8 | Smuin Ballet | smuin | https://signup-usa.keela.co/email-sign-up-form | To do |
| 9 | BAMPFA | bampfa | https://bampfa.org/email-signup | To do |
| 10 | SF Opera | sfopera | https://www.sfopera.com/link/293c0c32fa884caf83011c1512595ae2.aspx | To do |
| 11 | Lick Observatory | lick | https://www.lickobservatory.org/support/mailing-list/ | To do — the list announces the summer on-sale date (mid-April, via Eventbrite) |
| 12 | Stern Grove Festival | sterngrove | form on https://www.sterngrove.org/ | To do |

**Browser gotchas met so far:** Mailchimp forms (ODC, SF Playhouse, Fort Mason)
open their result in a new tab, which the browser pane blocks — set the form's
target to `_self` (and for SF Playhouse, submit the form element directly) to
keep it in the same tab. Mailchimp may reject a submit without first/last name
even when not marked required, then show a "Confirm Humanity" CAPTCHA for the
owner. Decline cookie banners. Before asking the owner to act in the browser,
check the pane is displayed; if hidden, show it (`show_pane` preview).

## Why each is on the list (for the spec)

| Venue | Reason |
|---|---|
| 1015 Folsom, Chase Center | Unreached 5 of 5 weeks (calendars render client-side) |
| SFJAZZ | Partial every week — sfjazz.org refuses the reader; mirror = main hall only |
| Z Space, Fort Mason, ODC, SF Playhouse | Unreached 3 weeks |
| Smuin, BAMPFA | Unreached 2 weeks |
| SF Opera | Costume sale (sold out a day after on-sale); calendar also down once |
| Lick Observatory | Summer concerts sell out in minutes |
| Stern Grove | Free summer tickets by email lottery |

**Left off, and why (also for the spec):**
- No email list: **DNA Lounge** (unreached 5/5) and **The Midway** (2/5). Not a
  daily check (see ruling). DNA Lounge's calendar opens to anything presenting
  as a normal browser — fixing how the weekly run reads it is a separate task.
  The Midway blocks all automated reading; stays on the ticketing sweep.
- **SFJAZZ** likewise opened normally in the built-in browser on 2026-10-18,
  though the weekly run's reader is refused — same class as DNA Lounge.
- Fixed since 9 Oct: Kilowatt (DICE reader), 924 Gilman (ticketing page).
- Not a reading problem: Roxie (read twice), A.C.T. (publishes no curtain times).
- Read fine via mirrors: Freight & Salvage, Fillmore, Regency, etc.
- Paid memberships give presales at Lick (Friends of Lick: one week early),
  SFJAZZ, SF Opera, BAMPFA, SF Playhouse — owner's call, outside this job.

## Outcome (end of session, 2026-10-18)

All 12 sign-ups submitted; SFJAZZ and BAMPFA confirmation links opened with the
owner's approval. Stern Grove's confirmation email had not arrived. The record is
`specs/act-now-alerts.md`; the backlog row is updated. The table above is the
session's working log and is superseded by the spec.

## Next session

Delivery was decided after the sign-ups (owner, 18 October): the Gmail connector
emails the owner, and the agent decides when — see the Delivery section of
`specs/act-now-alerts.md`. The next job is building the reader that sorts the
subscription mailbox daily and sends that email. Before building it:

1. Establish how sending can be **limited to the owner's one address**, enforced
   rather than instructed — the same agent reads untrusted mail. Neither the
   owner's address nor the mailbox's goes in any file here.
2. Settle the reminder near the on-sale date, not only on the day it is announced.
3. Check that Stern Grove's confirmation email arrived; open its link only after
   showing the owner.
4. Hammer Theatre: **signed up 18 October** by the owner in their own browser, tag `hammer`. Its confirmation email had not arrived by the end of the session — check for it beside Stern Grove's.

Done later on 18 October, after the sign-ups: the South Bay / Peninsula coverage
report (`reports/2026-10-18-south-bay-peninsula-coverage.md`), and on the owner's
decision 14 company season pages added to `config/sources.yml` and Stanford,
Foster City and Half Moon Bay added to the Peninsula in `config/brief.yml`. The
new entries show as "declared, no listing" warnings until the next weekly run
reads them — expected, not a fault. The Mountain View Center needs no email
sign-up: its main resident, TheatreWorks, is now read directly.
