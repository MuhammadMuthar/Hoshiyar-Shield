# Pakistan financial and digital fraud: source ledger

**No external numeric claim is approved for the pitch yet.** Source retrieval
was blocked on 10 October 2026 (PKT): requests to the official and news
websites below failed with `Tunnel connection failed: 403 Forbidden` through
the environment's configured HTTPS proxy. No publication, publication date,
figure or quotation was retrieved. TLS verification was not disabled.

`VERIFIED` means that the original publication was retrieved and its figure,
publication date and exact wording were checked. It does not mean that a
reported complaint was independently proved to be fraud. `UNVERIFIED` entries
must stay out of the pitch, UI, slide deck and marketing copy.

## Research leads — not citations

These are publishers to investigate when source access is available. The URLs
are discovery homepages, **not original report URLs**; they must be replaced
with the specific publication before any row can become `VERIFIED`. No claim
or quotation has been filled from memory.

| # | Claim (exact figure) | Publisher | Date published | URL | Exact quote | Status |
|---|---|---|---|---|---|---|
| 1 | No figure verified. Look for a defined reporting period and separate digital-payment fraud cases from transaction volumes. | State Bank of Pakistan | Not established | https://www.sbp.org.pk/ | Not available; source retrieval blocked. | UNVERIFIED |
| 2 | No figure verified. Look for complaints about scam calls/messages and distinguish complaints from blocked numbers and confirmed victims. | Pakistan Telecommunication Authority | Not established | https://www.pta.gov.pk/ | Not available; source retrieval blocked. | UNVERIFIED |
| 3 | No figure verified. Look for financial-fraud complaint counts and distinguish them from all cybercrime complaints, inquiries, cases and convictions. | Federal Investigation Agency | Not established | https://www.fia.gov.pk/ | Not available; source retrieval blocked. | UNVERIFIED |
| 4 | No figure verified. Look for dated financial-fraud complaint or loss figures; check agency coverage and avoid adding totals that overlap FIA reporting. | National Cyber Crime Investigation Agency | Not established | https://www.nccia.gov.pk/ | Not available; source retrieval blocked. | UNVERIFIED |
| 5 | No figure verified. Seek reporting that links to the underlying official report or attributes a precise figure to a named agency and period. | Dawn | Not established | https://www.dawn.com/ | Not available; source retrieval blocked. | UNVERIFIED |

## Requirements before using a figure

- Retrieve the original article or report, record its publication date, and
  quote the complete relevant sentence or table cells. For a PDF, include its
  report title, page number and table heading alongside the exact quote.
- Preserve the source's unit and scope: complaints, unique complainants,
  investigations, confirmed incidents, losses, recoveries and blocked numbers
  are different measures. State the reporting period and geographic coverage.
- Separate all cybercrime from financial fraud. A complaint count alone does
  not establish the number of victims, proven cases, national prevalence or
  money lost. Digital-payment growth alone is not a fraud statistic.
- Retain the original currency and qualification of any loss estimate. Do not
  extrapolate a monthly figure, add overlapping reports, round a figure up or
  infer that the app would prevent the reported losses.
- Use source-backed figures only to describe the reported problem. They do not
  validate this app's accuracy, effectiveness, adoption or safety guarantees.

## Recheck status

The failed requests used Python's standard-library `urllib.request.urlopen`
with normal TLS verification and the configured proxy. The same tunnel error
occurred for the five publisher hosts above and for `www.google.com` during
source discovery. This establishes a retrieval blocker in this environment;
it does not establish that the publishers' websites are down or that a
particular statistic is false. No source bodies were downloaded.

When access is available, complete three to five specific source rows using
the table contract in [`COLLABORATION.md` §5.4](./COLLABORATION.md#54-sources-docssourcesmd).
Until then, omit numeric problem-scale claims from the pitch.

The environment configuration draft now includes these five research hosts:
`www.sbp.org.pk`, `www.pta.gov.pk`, `www.fia.gov.pk`, `www.nccia.gov.pk` and
`www.dawn.com`. Existing package-manager network presets were preserved.
Draft saving does not enable access in the running machine. Review and save
the network changes in environment settings, then publish the environment;
retry source retrieval after the updated policy is applied. Publication and
successful retrieval have not been verified here.
