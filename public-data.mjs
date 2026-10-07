export const repo='https://github.com/Agents-Foundry/employee-agent-platform';
export const docs='https://agents-foundry.github.io/employee-agent-platform-docs/';
export const wiki=repo+'/wiki';
export const baseline='46bfce6bb10c58a4b4f6cc5109e88eb39512c01b';
export {origin} from './site-config.mjs';
export const capabilities=[
 ['Identity','Implemented','Employee ownership, organization membership and server-side sessions bind work to a known actor.'],
 ['Model','Implemented','The model gateway runs Anthropic with organization-managed credentials and spending controls. Employee BYOK execution is not supported.'],
 ['Memory / Context','Implemented in part','Conversations and durable checkpoints preserve run context. Organization-wide knowledge retrieval is a future extension.'],
 ['Skills','Declarative catalog','Versioned skill and workflow definitions shape signed assignments. A separate executable skill-package runtime is a future extension.'],
 ['Tools','Implemented','Scoped tools request actions through a fail-closed gateway. Workspace changes, commands and external writes have distinct controls.'],
 ['MCPs','Future extension','MCP configuration is part of the capability model; an MCP client and tool execution are not available in the current runtime.'],
 ['Connectors','Implemented','Read Jira work items, create approved issues and publish approved draft GitHub pull requests within configured scopes.'],
 ['Browser','Implemented','Approved Playwright runs execute in a container sandbox through controlled egress and return screenshots, traces and reports.'],
 ['Git','Implemented','Scoped checkouts and private-repository credential leases support repository work. External publication requires approval.'],
 ['Shell','Implemented','Allow-listed scripts and locked dependency installs execute in a sandbox. Production deployment stays denied.'],
 ['Artifacts','Implemented','Local or S3-compatible storage retains evidence with integrity checks, controlled retrieval and retention.'],
 ['Policies','Implemented','Contextual rules allow, require approval or deny. Organization policy can tighten the platform decision; unknown actions fail closed.'],
 ['Secrets','Implemented','Vault-backed references resolve at use time. Organization-managed model keys and execution-only checkout leases keep credentials scoped.'],
 ['Approvals','Implemented','Expiring, payload-bound approvals pause work for a separate human decision. Approved work resumes under signed, single-use grants.'],
 ['Audit','Implemented','Decisions, approvals, run actions and write reconciliations retain an inspectable record. Metrics and traces expose operational signals.']
];
const engineering=(image,name,team,goal,skills,tools,activity)=>({image,name,team:'Engineering / '+team,state:'Supported engineering role',goal,skills,tools,permissions:'Assigned project and signed capabilities; constrained execution; no production deployment',activity,approval:'Human review before browser actions or external writes where assigned'});
const expansion=(image,name,team,goal,skills)=>({image,name,team,state:'Expansion role',goal,skills,tools:'Future role-specific integrations',permissions:'Designed around assigned context and controlled actions',activity:'Workforce expansion direction',approval:'Human ownership of consequential decisions'});
export const roles=[
 engineering('testo.avif','QA Engineer','QA','Turn release scope into tests and reviewable evidence.','QA planning, acceptance checks and defect drafts','Jira, Git, sandbox scripts, Playwright and artifacts','Task → plan → governed checks → evidence → reviewed draft'),
 engineering('fronto.avif','Frontend Engineer','Frontend','Implement interface changes within a defined repository scope.','Frontend implementation, accessibility and testing','Repository checkout, workspace changes, sandbox tests and artifacts','Task → inspect → implement → test → draft pull request'),
 engineering('backo.avif','Backend Engineer','Backend','Deliver service changes with explicit API boundaries.','Backend implementation and service testing','Git, workspace files, sandbox commands and artifacts','Task → inspect service → implement → test → reviewed draft'),
 engineering('stacko.avif','Code Reviewer','Review','Return actionable findings on assigned changes.','Change inspection, risk analysis and review reports','Scoped repository reads and artifacts','Task → inspect changes → evaluate → report findings'),
 engineering('automo.avif','Test Automation Engineer','Automation','Create repeatable tests with evidence.','Test implementation and bounded validation','Git, workspace files, sandbox scripts and artifacts','Task → implement tests → validate → return evidence'),
 expansion('producto.avif','Product Manager','Product / Planning','Turn customer context into defined scope.','Requirements synthesis and prioritization'),
 expansion('analytico.avif','Business Analyst','Product / Analysis','Connect requirements to delivery decisions.','Research synthesis and process analysis'),
 expansion('sello.avif','Sales Representative','Sales / Accounts','Prepare account context and outreach for review.','Account research and draft preparation'),
 expansion('opero.avif','Operations Manager','Operations / Workflows','Improve handoffs and repeatable workflows.','Workflow mapping and exception analysis')
];
export const workflow=[
 ['Read release context','Scoped connector','Read Jira stories and acceptance criteria through an approved organization connection.'],
 ['Inspect repository changes','Governed checkout','Inspect the assigned repository; private checkout uses brokered, execution-only credentials.'],
 ['Create a test strategy','Supported workflow','The QA role uses task context and the model gateway to plan bounded checks.'],
 ['Request browser execution','Approval required','Policy pauses the browser action for an expiring, payload-bound human approval.'],
 ['Record the decision','Human control','A separate administrator approves or rejects. Approved work resumes under a signed execution grant.'],
 ['Run isolated checks','Container execution','Allow-listed scripts and approved Playwright operations run behind sandbox and egress controls.'],
 ['Capture evidence and defects','Retained evidence','Screenshots, traces and reports are stored with integrity checks and controlled retrieval.'],
 ['Review external writes','Approval required','Issues and draft pull requests require review. Uncertain writes are held for administrator reconciliation.']
];
export const policy=[
 ['qa.plan','Create test plan','ALLOW','Supported planning action'],
 ['jira.read','Read Jira context','ALLOW','Scoped Jira adapter'],
 ['repository.read','Read repository','ALLOW','Scoped repository access'],
 ['qa.execute_playwright','Execute Playwright','REQUIRE_APPROVAL','Approved sandbox execution'],
 ['jira.issue.create','Create Jira issue','REQUIRE_APPROVAL','Approved Jira write'],
 ['repository.pull_request.create','Create pull request','REQUIRE_APPROVAL','Approved draft GitHub pull request'],
 ['production.deploy','Deploy to production','DENY','Denied to employee agents'],
 ['unknown.action','Unknown action','DENY','Fail-closed default']
];
export const progress=[
 ['Organization control plane','Implemented','Structure, memberships, roles, positions and employee assignments.'],
 ['Five engineering roles','Implemented','QA, Frontend, Backend, Code Reviewer and Test Automation share one runtime and seven blueprint versions.'],
 ['Runtime and model gateway','Implemented','Native kernel, organization-managed Anthropic, scoped tools, budgets and durable recovery.'],
 ['Governed execution','Implemented','Signed grants, constrained repository work, sandbox commands and approved browser operations.'],
 ['Connected work and evidence','Implemented','Jira, draft GitHub pull requests, private checkouts and integrity-checked artifacts.'],
 ['Secrets and tenant isolation','Implemented','PostgreSQL row-level security, Vault secret resolution and scoped credential leases.'],
 ['Operator controls','Implemented','Write reconciliation screen, dashboards, alerts and host validation.'],
 ['Controlled pilot evidence','Deployment checks','Guarded live smoke and release-specific readiness require fresh reports from the deployment.'],
 ['Workforce expansion','Future direction','Additional business roles, MCP execution and broader onboarding build on the shared foundation.']
];
