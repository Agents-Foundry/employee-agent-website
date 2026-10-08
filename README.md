# Agents Foundry website

The standalone public website for Agents Foundry, including sixteen static pages, all 55 employee bot illustrations, interactive organization and policy explorers, the QA walkthrough, and light/dark themes.

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
- `commerce-pages.mjs`: Pricing, Community, Docs and Contact Us pages; current MIT Community availability and indicative managed service plans.
- `public-components.mjs`: shared page sections and diagrams.
- `public-data.mjs`, `catalog.json`, `role-outputs.json`: capability descriptions and employee catalog.
- `public/public.css`: responsive design and themes.
- `public/modern.css`: framed sections, illustrated feature grid, dimensional cards and desktop sticky storytelling.
- `public/commerce.css`: responsive edition cards, feature comparison and resource/documentation layouts.
- `public/depth.css`, `public/depth.js`: CSS 3D hero geometry, dimensional typography/materials and bounded pointer perspective.
- `public/public.js`: interactive controls.
- `public/assets/`: original bot images, logo and local font.
- `video/`: explainer storyboard, narration and animation source; see its README to regenerate the film.
- `public-build.mjs`: static generator; output goes to ignored `dist/`.

The public access page does not collect credentials. Contact prepares a local email draft; the visitor sends it using their chosen email service. Current and planned product capabilities remain labeled. `tests/policy-contract.json` records the verified product policy contract; update it alongside any changes to policy descriptions.

The homepage includes a 1080p, 30 fps character film with the original website bot artwork animated on deformable meshes in a 3D environment. It includes a human teammate, moving cameras, narration, an original quiet soundtrack, English captions, a transcript and an MP4 download. It describes the 5–10 minute guided onboarding target for a configured organization, using the implemented QA assignment flow. The video uses native controls and does not autoplay or preload its full media file.

Scroll reveals progressively enhance visible content using IntersectionObserver. Without JavaScript, with reduced motion, or after choosing Pause motion, content stays readable. The sticky operating-model cards become a normal vertical sequence on smaller screens. No animation library or remote asset dependency is required.

The 3D layer uses CSS geometry and the existing bot art. Mouse perspective is limited to desktop fine pointers, resets on exit/scroll/focus, and stops with Pause motion or reduced motion. Touch screens retain static depth without pointer tilt; the hero shapes stay decorative and hidden from assistive technology.

Visual references: [lookfor](https://lookfor.ai/), [Atlas](https://youratlas.com/), [Elimentary](https://www.elimentary.com/) and [Nolana](https://nolana.com/). The redesign uses framed scenes, layered gradients and visual feature cards as inspiration; illustrations, copy and product diagrams remain specific to Agents Foundry.

## GitHub Pages

The `Deploy website to GitHub Pages` workflow checks pull requests and automatically publishes successful builds from `main`. The publishing source in repository Settings → Pages is **GitHub Actions**. Deployments use the `github-pages` environment.

For manual deployment, open Actions → Deploy website to GitHub Pages → Run workflow.

`SITE_URL` controls the canonical URL and repository path. The workflow uses the configured Pages URL, so both project Pages and a future custom domain work. For local root hosting, set `SITE_URL=http://localhost:5173` before running `npm run dev`. For another host, set its full URL (including a subdirectory if needed) when building.

The generated site includes all static routes, an XML sitemap, robots.txt, a 404 page and `.nojekyll`. It contains no runtime secrets or backend.

## Community and managed service pages

The edition presentation takes structural inspiration from [AG Grid pricing](https://www.ag-grid.com/license-pricing/): clear plan cards, capability comparison, FAQs and separate support routes. Agents Foundry keeps its own visual identity and MIT core; it does not adopt AG Grid's per-developer software licensing model.

`/pricing/` presents free self-hosted Community and indicative Developer ($29/month), Team ($299/month), Organization ($999/month), custom Enterprise and a proposed scoped pilot. Managed pricing and capacity are early-access proposals, not a functioning purchase/subscription system. Model provider fees are separate. Requests lead to a plan-specific local inquiry draft; there is no checkout or automatic provisioning.

`/community/` links setup, issues, contributions and releases. `/docs/` filters public Community and managed/organizational guides, including the existing technical docs and wiki. `/contact/` prepares a reviewed draft with optional organization context without sending or storing it on a server. The public website continues to hide the recipient's email from visible contact content.

## Source and license

Extracted from the published Agents Foundry website, source revision `d58a5a3c91b28dfef5655411c4d54b3e09b27f21`. The original Sites checkout and the authenticated product application are maintained separately. This repository owns the GitHub Pages copy and its build configuration.

MIT license; see [LICENSE](LICENSE).

## Product content baseline — 7 October 2026

Website copy is reviewed against platform commit `46bfce6bb10c58a4b4f6cc5109e88eb39512c01b`. It describes five engineering roles, seven blueprint versions, the native runtime/model gateway, signed sandbox execution, connectors, PostgreSQL RLS, Vault, evidence and operational controls. The 55 bot illustrations remain the broader workforce catalog; current engineering roles and expansion roles are distinguished. The public diagrams and dashboards are explanatory, not live deployment telemetry.

The website links to the published [technical docs](https://agents-foundry.github.io/employee-agent-platform-docs/), [wiki](https://github.com/Agents-Foundry/employee-agent-platform/wiki) and latest pilot environment checklist. A passing website build does not qualify a pilot; live validation and guarded smoke reports are required for the deployed product.
