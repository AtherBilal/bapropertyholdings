# bapropertyholdings.com

BA Properties' public website. It was exported from Webflow on 2026-11-25 and now runs as a static site on GitHub Pages, so there's no Webflow subscription.

- **Source:** `index.html` + `css/`, `js/`, `images/`, `fonts/`. Every asset is local: nothing loads from Webflow's CDN. Google Fonts and the WebFont loader still come from Google.
- **Contact form:** posts to [FormSubmit](https://formsubmit.co) and arrives at `info@bapropertyholdings.com`. The very first submission sends a one-time activation email to that inbox, and nothing is delivered until someone clicks the link in it. The code is the `<script>` block at the bottom of `index.html`.
- **Content changes since the Webflow export:** Indianapolis, IN was added to "Currently we are operating in…".

## Deploy

GitHub Pages serves the `main` branch from the root. Push to `main` and it rebuilds in about 60 seconds.

```sh
git add -A && git commit -m "..." && git push
```

Preview locally: `python3 -m http.server 8765`, then open http://localhost:8765.

## Pointing the domain here (Namecheap)

The domain is registered at Namecheap. Today `www` is a CNAME to `proxy-ssl.webflow.com`, and the bare domain has no A record, so `bapropertyholdings.com` without `www` doesn't load at all.

**Don't touch the MX records** (Google Workspace email: `aspmx.l.google.com` and the others) or the `google-site-verification` TXT record.

1. Namecheap → Domain List → bapropertyholdings.com → **Advanced DNS**.
2. Change the `www` CNAME from `proxy-ssl.webflow.com.` to `atherbilal.github.io.`
3. Add four A records for host `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
4. Delete the `proxy-ssl.webflow.com` TXT record on `@`. It was Webflow's verification and is no longer needed.
5. Once `dig +short www.bapropertyholdings.com` shows `atherbilal.github.io` and `dig +short bapropertyholdings.com` shows the 185.199.x addresses, run:

```sh
gh api -X PUT repos/AtherBilal/bapropertyholdings/pages -f cname=www.bapropertyholdings.com
# after GitHub issues the certificate (a few minutes to an hour):
gh api -X PUT repos/AtherBilal/bapropertyholdings/pages -F https_enforced=true
```

Don't set the custom domain before DNS points here. Pages would redirect the github.io URL to a domain that still answers from Webflow.

6. Only cancel the Webflow site plan after the live domain serves this copy. Check by submitting the contact form once.
