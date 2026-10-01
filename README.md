# Agents Foundry website

The standalone public website for Agents Foundry, including twelve static pages, all 55 employee bot illustrations, interactive organization and policy explorers, the QA walkthrough, and light/dark themes.

Website: https://agents-foundry.github.io/employee-agent-website/

Product implementation: https://github.com/Agents-Foundry/employee-agent-platform

## Local development

Install Node.js 24 or newer, then:

```sh
npm ci
npm run dev
```

Open http://127.0.0.1:5173/employee-agent-website/.

```sh
npm run check
```

This builds the site and checks routes, assets, metadata, anchors, role catalog, dialogs, organization/workflow/policy controls, theme/motion settings, and contact drafts. No product checkout, product API or Sites plugin is required.

## Edit the website

- `public-pages.mjs`: page content and route definitions.
- `public-components.mjs`: shared page sections and diagrams.
- `public-data.mjs`, `catalog.json`, `role-outputs.json`: capability descriptions and employee catalog.
- `public/public.css`: responsive design and themes.
- `public/public.js`: interactive controls.
- `public/assets/`: original bot images, logo and local font.
- `public-build.mjs`: static generator; output goes to ignored `dist/`.

The public access page does not collect credentials. Contact prepares a local email draft; the visitor sends it using their chosen email service. Current and planned product capabilities remain labeled. `tests/policy-contract.json` records the verified product policy contract; update it alongside any changes to policy descriptions.

## GitHub Pages

The `Deploy website to GitHub Pages` workflow checks pull requests and automatically publishes successful builds from `main`. The publishing source in repository Settings → Pages is **GitHub Actions**. Deployments use the `github-pages` environment.

For manual deployment, open Actions → Deploy website to GitHub Pages → Run workflow.

`SITE_URL` controls the canonical URL and repository path. The workflow uses the configured Pages URL, so both project Pages and a future custom domain work. For local root hosting, set `SITE_URL=http://localhost:5173` before running `npm run dev`. For another host, set its full URL (including a subdirectory if needed) when building.

The generated site includes all static routes, an XML sitemap, robots.txt, a 404 page and `.nojekyll`. It contains no runtime secrets or backend.

## Source and license

Extracted from the published Agents Foundry website, source revision `d58a5a3c91b28dfef5655411c4d54b3e09b27f21`. The original Sites checkout and the authenticated product application are maintained separately. This repository owns the GitHub Pages copy and its build configuration.

MIT license; see [LICENSE](LICENSE).
