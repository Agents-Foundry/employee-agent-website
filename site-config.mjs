const url=new URL(process.env.SITE_URL || 'https://agents-foundry.github.io/employee-agent-website/');
if(!['https:','http:'].includes(url.protocol)||url.search||url.hash)throw new Error('SITE_URL must be an HTTP(S) site URL without a query or fragment.');
export const origin=url.href.replace(/\/$/,'');
export const basePath=url.pathname.replace(/\/$/,'');
export const prefixLinks=html=>html.replace(/\b(href|src)="\/(?!\/)/g,`$1="${basePath}/`);
