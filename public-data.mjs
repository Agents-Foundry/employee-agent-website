export const repo='https://github.com/Agents-Foundry/employee-agent-platform';
export {origin} from './site-config.mjs';
export const capabilities=[
 ['Identity','Implemented','An employee and organization own the assignment. Server-side sessions and membership checks establish the actor.'],
 ['Model','Metadata available','BYOK and organization-managed preferences are recorded. Live model calls and a model gateway are planned.'],
 ['Memory / Context','Implemented in part','Conversations persist centrally. Retrieval over organizational knowledge is a future capability.'],
 ['Skills','Architecture target','Versioned role skills would describe repeatable work and its evaluation criteria.'],
 ['Tools','Architecture target','A governed tool runtime would validate each action before dispatch. Current policy decisions are implemented.'],
 ['MCPs','Architecture target','An MCP runtime would expose approved external capabilities within an employee’s permissions.'],
 ['Connectors','Planned','Jira and Bitbucket adapters would supply bounded work-item and repository context.'],
 ['Browser','Planned','Isolated Playwright execution would produce evidence after the required human approval.'],
 ['Git','Planned','Bounded repository workspaces would separate source inspection from controlled external writes.'],
 ['Shell','Architecture target','Scoped commands would run inside a restricted execution workspace, not inside the control plane.'],
 ['Artifacts','Planned','Reports, screenshots and traces would carry retention rules and controlled downloads.'],
 ['Policies','Implemented','Known actions receive ALLOW, REQUIRE_APPROVAL or DENY. Unknown actions are denied.'],
 ['Secrets','Metadata available','The current store holds opaque references and key-mode metadata. Vault-backed secret delivery is planned.'],
 ['Approvals','Implemented','Administrators record decisions and reasons. An approved QA run becomes READY; execution is a separate milestone.'],
 ['Audit','Implemented','Workflow and lifecycle events are appended in the application. This is not a claim of tamper-proof external audit storage.']
];
export const roles=[
 {image:'testo.avif',name:'QA Engineer',team:'Engineering / QA',state:'Available locally',goal:'Turn acceptance criteria into a reviewable test strategy.',skills:'QA planning and scoped acceptance checks',tools:'Policy evaluation, conversations, approval requests',permissions:'Planning allowed; browser execution requires approval; production deploy denied',activity:'Task → plan → approval decision → READY or REJECTED',approval:'Administrator review before browser execution'},
 {image:'fronto.avif',name:'Frontend Engineer',team:'Engineering / Frontend',state:'Planned role',goal:'Translate product scope into reviewed interface changes.',skills:'Interface design and accessibility review',tools:'Proposed repository, browser and artifact capabilities',permissions:'Proposed project scope with reviewed writes',activity:'No live activity. This role is a product concept.',approval:'Proposed review of repository changes'},
 {image:'backo.avif',name:'Backend Engineer',team:'Engineering / Backend',state:'Planned role',goal:'Develop service changes with explicit API boundaries.',skills:'API design and test strategy',tools:'Proposed Git, shell and service-test capabilities',permissions:'Proposed repository and environment scope',activity:'No live activity. This role is a product concept.',approval:'Proposed review of code publication'},
 {image:'devopsy.avif',name:'DevOps Engineer',team:'Engineering / DevOps',state:'Planned role',goal:'Prepare repeatable delivery plans with release gates.',skills:'Pipeline planning and operational review',tools:'Proposed infrastructure and repository connectors',permissions:'Proposed environment-specific controls',activity:'No live activity. This role is a product concept.',approval:'Proposed human release decisions'},
 {image:'producto.avif',name:'Product Manager',team:'Product / Planning',state:'Planned role',goal:'Turn customer context into a defined product scope.',skills:'Requirements synthesis and prioritization',tools:'Proposed knowledge and work-item connectors',permissions:'Proposed access to assigned product context',activity:'No live activity. This role is a product concept.',approval:'Proposed human approval of priorities'},
 {image:'analytico.avif',name:'Business Analyst',team:'Product / Analysis',state:'Planned role',goal:'Connect business requirements to delivery decisions.',skills:'Research synthesis and process analysis',tools:'Proposed knowledge and reporting capabilities',permissions:'Proposed scoped context access',activity:'No live activity. This role is a product concept.',approval:'Proposed review of recommendations'},
 {image:'sello.avif',name:'Sales Representative',team:'Sales / Accounts',state:'Planned role',goal:'Prepare account context and outreach for review.',skills:'Account research and draft preparation',tools:'Proposed CRM and knowledge connectors',permissions:'Proposed account scope; outbound writes controlled',activity:'No live activity. This role is a product concept.',approval:'Proposed review before sending outreach'},
 {image:'opero.avif',name:'Operations Manager',team:'Operations / Workflows',state:'Planned role',goal:'Identify handoffs and improve repeatable workflows.',skills:'Workflow mapping and exception analysis',tools:'Proposed enterprise connectors and artifacts',permissions:'Proposed workflow-specific permissions',activity:'No live activity. This role is a product concept.',approval:'Proposed review of operational changes'}
];
export const workflow=[
 ['Read release context','Planned connector','Jira stories and release scope would enter through an approved connector.'],
 ['Inspect repository changes','Planned connector','Bitbucket context would connect changed code to acceptance criteria.'],
 ['Create a test strategy','Implemented locally','The current QA flow produces a structured plan from a submitted task.'],
 ['Request browser execution','Approval required','The policy engine holds Playwright execution for an administrator decision.'],
 ['Record the decision','Implemented locally','Approval records a reason and sets the run to READY; rejection sets it to REJECTED.'],
 ['Run isolated checks','Planned execution','A future worker would consume approved work and execute Playwright tests.'],
 ['Capture evidence and defects','Planned artifacts','Traces, screenshots and reports would support reviewable defect drafts.'],
 ['Review external writes','Policy defined','Jira issue creation and pull-request creation require approval. Their execution adapters are planned.']
];
export const policy=[
 ['qa.plan','Create test plan','ALLOW','Implemented planning flow'],
 ['jira.read','Read Jira context','ALLOW','Connector planned'],
 ['repository.read','Read repository','ALLOW','Connector planned'],
 ['qa.execute_playwright','Execute Playwright','REQUIRE_APPROVAL','Execution planned'],
 ['jira.issue.create','Create Jira issue','REQUIRE_APPROVAL','Connector planned'],
 ['repository.pull_request.create','Create pull request','REQUIRE_APPROVAL','Execution planned'],
 ['production.deploy','Deploy to production','DENY','Denied to the QA employee'],
 ['unknown.action','Unknown action','DENY','Fail-closed default']
];
export const progress=[
 ['Organization control plane','Implemented','Departments, teams, membership, job roles and positions.'],
 ['Identity and onboarding','Implemented','Password activation and membership flows; Google sign-in requires tenant configuration.'],
 ['QA catalog and manifests','Implemented','Versioned questionnaires, administrator provisioning and signed assignments.'],
 ['Policy, approvals and audit','Implemented','Deterministic decisions, recorded reasons and application lifecycle events.'],
 ['Runtime protocol and worker','Architecture target','Approval-to-execution contracts and isolated workers remain to be delivered.'],
 ['Model, skills, tools and MCP','Architecture target','Reusable capability runtimes, live model calls and promotion workflows.'],
 ['Git, shell, browser and artifacts','Planned','Ephemeral execution and evidence collection.'],
 ['Jira and Bitbucket','Planned','Read-only context first, then governed external writes.'],
 ['Vault and database isolation','Planned','Vault integration, key rotation and database-level tenant isolation.']
];
