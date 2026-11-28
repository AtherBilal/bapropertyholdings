#!/usr/bin/env python3
"""Build stl-portfolio/index.html from _metrics.json (booking-system payouts) + _data/listings.json."""
import json, os, html
H = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(H, "_metrics.json")))
L = {l["img"][0].split("/")[-1]: l for l in json.load(open(os.path.join(H, "..", "_data", "listings.json")))}
UNITS = [  # unit key, photo prefix, display name, area, monthly rent
 ("Crow D", "crow-unit-d", "Crow Unit D", "Soulard", 1750),
 ("Crow B", "crow-unit-b", "Crow Unit B", "Soulard", 1750),
 ("Crow A", "crow-unit-a", "Crow Unit A", "Soulard", 1750),
 ("Crow C", "crow-unit-c", "Crow Unit C", "Soulard", 1750),
 ("2E", "2e-the-heart-of-mardi-gras-sou", "Soulard 2E", "Soulard", 1365),
 ("2W", "2w-chill-soulard-condo-across-", "Soulard 2W", "Soulard", 1365),
 ("Greenest", "greenest-the-grove-s-greenest-", "Grove's Greenest Pad", "The Grove", 1400),
 ("Groovy", "groovy-groovy-in-the-grove-5-m", "Groovy in the Grove", "The Grove", 1400),
]
def listing(prefix): return next(v for k, v in L.items() if k.startswith(prefix))
money = lambda v: f"${v:,.0f}"
k = lambda v: (f"${v/1000:,.0f}k" if v >= 100000 else f"${v/1000:,.1f}k")
U = M["units"]
tot = {f: sum(U[u][f] for u, *_ in UNITS) for f in ["payout", "nights", "stays", "cleaning", "rent", "utilities", "contribution"]}
revs = sum(listing(p)["reviews"] for _, p, *_ in UNITS)
rating = sum(listing(p)["reviews"] * listing(p)["rating"] for _, p, *_ in UNITS) / revs
occ = tot["nights"] / (len(UNITS) * 365)
rent_month = sum(r for *_, r in UNITS)

rows, cards = [], []
for key, pre, name, area, rent in UNITS:
    u, l = U[key], listing(pre)
    rows.append(f"<tr><th scope=row>{name}<span>{area} · {l['bedrooms']} bd</span></th><td>{money(u['payout'])}</td><td>{u['nights']/365:.0%}</td><td>{u['stays']}</td><td>{money(u['payout']/u['nights'])}</td><td>{money(rent)}</td><td>{money(u['cleaning'])}</td><td>{money(u['utilities'])}</td><td class=b>{money(u['contribution'])}</td></tr>")
    imgs = "".join(f'<img src="/new/img/{pre}-0{i}.jpg" alt="{html.escape(name)} photo {i}" loading="lazy">' for i in (1, 2, 3))
    cards.append(f"""<article class=unit>
  <div class=pics>{imgs}</div>
  <div class=ub>
    <p class=area>{area}</p><h3>{name}</h3>
    <p class=spec>{l['bedrooms']} bedroom{'s' if l['bedrooms']>1 else ''} · sleeps {l['sleeps']} · <b>{l['rating']:.2f}★</b> from {l['reviews']} reviews</p>
    <dl><div><dt>12-mo payout</dt><dd>{k(u['payout'])}</dd></div><div><dt>Nights booked</dt><dd>{u['nights']/365:.0%}</dd></div><div><dt>Payout / night</dt><dd>{money(u['payout']/u['nights'])}</dd></div><div><dt>Rent</dt><dd>{money(rent)}/mo</dd></div></dl>
    <a href="{l['airbnb']}" target=_blank rel=noopener>View the live Airbnb listing →</a>
  </div>
</article>""")

months = list(M["monthly"].items())
mtable = "".join(f"<tr><td>{m}</td><td>{money(v)}</td></tr>" for m, v in months)
tpl = open(os.path.join(H, "template.html")).read()
out = (tpl.replace("{{UNITS_N}}", str(len(UNITS))).replace("{{PAYOUT}}", k(tot["payout"])).replace("{{OCC}}", f"{occ:.0%}")
       .replace("{{REVIEWS}}", f"{revs:,}").replace("{{RATING}}", f"{rating:.2f}").replace("{{CONTRIB}}", k(tot["contribution"]))
       .replace("{{ROWS}}", "\n".join(rows)).replace("{{CARDS}}", "\n".join(cards)).replace("{{MTABLE}}", mtable)
       .replace("{{MONTHLY_JSON}}", json.dumps(months)).replace("{{RENT_MONTH}}", str(rent_month))
       .replace("{{TOT_ROW}}", f"<tr class=tot><th scope=row>Portfolio</th><td>{money(tot['payout'])}</td><td>{occ:.0%}</td><td>{tot['stays']:,}</td><td>{money(tot['payout']/tot['nights'])}</td><td>{money(rent_month)}</td><td>{money(tot['cleaning'])}</td><td>{money(tot['utilities'])}</td><td class=b>{money(tot['contribution'])}</td></tr>"))
open(os.path.join(H, "index.html"), "w").write(out)
print("built", tot, round(rating, 2), revs, f"{occ:.1%}", rent_month)
