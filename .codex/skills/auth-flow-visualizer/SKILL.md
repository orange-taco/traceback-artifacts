---
name: auth-flow-visualizer
description: "Create or update visual HTML guides for TRACEBACK system flows, AWS deployment setup, API contracts, and lifecycle states."
---

# TRACEBACK System Visualizer

Use this skill when documenting a TRACEBACK subsystem as a visual, reusable HTML
mini-site. It supports authentication, catalog/product management, commerce, and
future domains without reducing the explanation to a table or a prose-only page.

## Workflow

- The canonical guides and this skill live in `orange-taco/traceback-artifacts`,
  separate from the TRACEBACK backend and frontend. Inspect
  `orange-taco/traceback` or `orange-taco/traceback-client`, as appropriate,
  at a known revision before asserting current implementation or deployment state.
  In Codex Cloud, attach all three repositories to the same environment. The
  iPad itself does not need to clone them. If a relevant source repository is
  unavailable in the task, mark implementation claims unverified instead of guessing.
- Link source files to their GitHub URL and checked revision. Do not use
  relative paths that escape this documentation repository: the published
  site cannot resolve them.
- Create or update HTML artifacts under `docs/artifact/` in the repository.
  Use a descriptive filename such as `auth-flow.html` or `aws-ssm-access-guide.html`.
  Do not place generated artifacts inside `.codex/skills/`; that directory contains
  reusable skill instructions and resources. If an artifact is added or moved, update
  the relevant checkpoint or documentation links so readers can find it.
- Keep diagrams and interaction code in the HTML. Screenshots may live in
  `docs/artifact/images/`; verify their relative paths and include them in PDF
  output. Use inline `data:` images when a single portable HTML file is needed,
  accepting the larger HTML size and harder image replacement.
- Treat it as a small documentation site: keep a shared shell and domain
  navigation. The five TRACEBACK flow pages show the project topology and its
  actual configuration, environment boundaries, and verification state. Linked
  concept pages explain general mechanisms; long references hold procedures and
  source excerpts. Preserve existing source-reference sections when adding a domain.
- Keep `docs/artifact/index.html` as the single mobile entry point. Link each new
  guide from that index and give the guide a visible return link to the index.
  Group future topics there without requiring readers to save separate URLs.
- Make the explanation visual-first with SVG or CSS diagrams, lanes, arrows,
  highlights, and state transitions. Do not turn the main explanation into tables or
  prose cards.
- Add interaction when it clarifies behavior, such as domain tabs, branch selectors,
  step controls, focus highlighting, or expand/collapse details.
- Use restrained animation to communicate direction or state change, respect
  `prefers-reduced-motion`, and keep the initial frame understandable without input.
- Label ownership on every meaningful node: framework/library, TRACEBACK custom code,
  frontend, database, or external service. Show the actual method, endpoint, event,
  or state transition when known, and briefly explain what the node does.
- Mark short-circuit conditions, transaction boundaries, retries, and failure paths
  explicitly. Do not imply a callback or library hook runs unless the source proves it.
- Name the actor and target whenever a sentence mentions a server, key, port,
  request, response, inbound rule, outbound rule, or permission. For example,
  distinguish the reader's local computer from the remote EC2 instance, and
  distinguish an AWS login identity from the Linux user inside EC2. Explain a
  prerequisite term such as HTTP/HTTPS or a new connection before using it to
  explain stateful return traffic. A beginner should not need another source to
  identify who owns an object or which direction an arrow travels.
- Use semantic controls, visible labels, `aria-live` where state changes, text
  alternatives, keyboard operation, and responsive layout down to narrow widths.
- Provide a visible PDF save action. Its print view must include content hidden
  behind tabs or closed details, preserve diagrams and screenshots, and omit
  navigation controls; restore the interactive state after printing.

## Accuracy checks

- Verify every node, edge, state, and transition against the current source before rendering.
- Include endpoint, source ownership, and the relevant source path when that removes ambiguity.
- Do not invent framework behavior, business rules, or future domain behavior. Mark
  planned sections as planned instead of filling them with assumptions.
- Keep detailed source paths in a compact reference area or accessible text, while
  keeping the diagram readable.

## Required artifact standard

Apply this standard whenever creating or updating an HTML artifact
under `docs/artifact/`. Do not consider the artifact complete until a new reader
can answer these questions from the page itself:

1. What is the end-to-end flow? Show it first with a labeled visual and explain
   the arrows, participants, and boundaries in plain language.
2. Where can the reader learn the underlying terms, practical options, and
   tradeoffs? A TRACEBACK flow page may link to a separate concept guide;
   the concept guide presents the general model before the project example.
3. Which option does TRACEBACK use, and why? Tie the decision to the actual
   code, configuration, and operational constraints.
4. Where is it implemented? Place relevant source/configuration excerpts next
   to their explanation, with a link to the current file. Explain who consumes
   each value and at what stage; do not leave a code dump without a purpose.
5. What works now, what is configured but untested, and what is still pending?
   Label these states explicitly, including security and deployment boundaries.

Keep the visual and its detailed explanation close enough to read together.
Treat repository code as evidence of TRACEBACK's implementation, not evidence
that the choice is universal or optimal. For layered decisions, compare each
independent layer in order (for example, browser session vs token, account-flow
library, then templated pages vs headless API; or email protocol, delivery
provider, then synchronous vs queued sending). Name at least one credible
alternative at each real decision point, its tradeoff, and the reason the
current project chose its path. Do not invent an alternative merely to fill a
template.
Use screenshots only when they add verifiable setup context; diagrams may explain
the general path. Verify the source and observed setup before asserting a current
state. An attractive page that omits a required answer is unfinished.

## AWS initial setup learning set

Maintain five project-configuration pages in order: `flow-1-system.html`,
`flow-2-access.html`, `flow-3-deploy.html`, `flow-4-address.html`, and
`flow-5-dns.html`. They show the full TRACEBACK configuration and connection
paths, including Client→Vercel and Server→AWS, actual environment-variable
locations, development/production boundaries, and explicit verification state.
Do not shorten actual configuration into a summary or move it out of the five
pages. Keep the existing long guides as
linked concept and implementation references: `traceback-system-guide.html`,
`1-aws-ssm-ssh-learning-guide.html`, `2-dev-server-first-deployment.html`,
`3-development-ip-domain-guide.html`, and `4-dns-resolution-map.html`. Preserve
their existing URLs and fragment IDs. Use `concept-access.html`,
`concept-deploy.html`, `concept-address.html`, `concept-dns.html`,
`concept-auth.html`, and `concept-email.html` for short, topic-specific
explanations between the five project maps and the long references. Move general
networking and computing theory there while keeping concrete settings in the
project pages.

The index also links the authentication study path:
`auth-session-allauth-guide.html` compares session/token, account-flow tools,
and allauth presentation modes; `email-smtp-ses-guide.html` compares mail
transport, delivery provider, and send timing. Keep both paths connected to
the system guide and the deployment guide where server configuration matters.

- On a project-flow page, start with the actual TRACEBACK participants and
  explain which connections are code-defined, previously observed, or live-tested.
  Link unfamiliar terms to the companion concept guide. In a concept guide, start
  with the general mechanism, explain terms and alternatives, then use TRACEBACK
  as a dated example. Keep current-state and general claims visibly distinct.
- Before splitting a long guide into sections or tabs, draw one end-to-end map
  that includes its main path, meaningful alternate paths, and where those paths
  rejoin. Label which part each later section enlarges. At section boundaries,
  say why the next section follows and how it changes the same flow. Put a new
  term such as bastion at its actual branch in the map before analyzing it;
  otherwise the reader has no reason to care about that branch.
- Choose the learning depth from the task and the intended reader. For a
  beginner or study guide, let a reader understand the whole flow from the
  picture and short captions first, then reveal terminology, mechanisms,
  tradeoffs, and source code. An experienced-reader summary may be compact, but
  keep the diagram and deeper explanation accessible. Ask the user about level
  only when it cannot be inferred; TRACEBACK's study and startup guides default
  to beginner-friendly maps with optional depth.
- Give the visual a short plain-language explanation, then put longer reasoning,
  exceptions, and code in accessible expand/collapse sections. Ensure closed
  details are included when printing to PDF. Put the detail beside the step it
  explains instead of collecting all explanation at the end.
- Anticipate a beginner's next question at each conceptual jump (for example,
  how a service connects, which identity authorizes it, and why a port is or is
  not needed). Answer it next to the relevant diagram in plain language.
- Before writing a glossary, draw a concept map for every cluster of related
  terms. Show containment (which resource is inside which), sequence (what must
  exist or happen first), and independent controls (for example route table vs
  security group vs IAM). Label arrows by their meaning; do not use one arrow
  for both containment and network traffic. A term pair such as “EC2 · instance”
  must say whether it is a service-to-resource relationship or two alternatives.
- Run a beginner-question audit after drafting each section: ask “why is this
  needed?”, “who owns/uses it?”, “what is it inside or attached to?”, “what
  happens before and after?”, “how is it different from the adjacent term?”,
  and “what fails if it is absent?”. Answer the likely questions near the map,
  then leave a glossary only for quick recall. Review every guide in the
  learning set for the same isolated-definition problem when changing one.
- In a setup recipe, label shared prerequisites and standard commands separately
  from one project's provider, profile, resource IDs, or convenience shortcuts.
  Never imply a project-specific alias is a built-in cloud command or a required
  industry-wide step.
- For every code block, label it as an exact repository excerpt, executable
  example, schematic pseudocode, or observed console value. Exact excerpts must
  identify the source file and real line numbers, offer a source link, and put
  the relevant explanation beside the code when space permits. Verify every
  copied line and line range against the current source; refresh stale copies
  instead of leaving plausible but outdated examples. Never assign repository
  line numbers to a generated command or console-only setting.
- For a guide that may be read on mobile or outside the checkout, make exact
  source links land on the relevant lines in the repository viewer. Keep the
  displayed source revision identifiable so later edits do not silently change
  what the linked line numbers mean.
- Show setup dependencies in the order a first-time deployer must complete them.
  Place the status of each TRACEBACK step on that flow, including the first
  missing step that blocks a live request. Explain DNS, inbound routing, TLS
  certificate issuance/renewal, reverse proxy, runtime environment variables,
  database access, deployment, and frontend verification at their actual points
  in the path; do not collect omissions only in a final checklist.
- Define even basic terms at first use or in a nearby beginner glossary, while
  keeping general networking terms distinct from AWS product names.
- Next to the relevant visual, compare practical setup options, their tradeoffs,
  TRACEBACK's choice, and the reason for it. Put applicable configuration or
  source excerpts beside their explanation, with links to the current files.
  Explain who reads each setting and when, especially for environment files.
- Give enough console or terminal steps for a new AWS user to reproduce the
  setup. Distinguish a general procedure from values observed in this account.
- Mark each important setting as **configured and verified**, **configured but
  not yet tested**, or **still to do**. Show the current inbound, outbound,
  route-table, subnet, IAM, DNS, and runtime state where relevant. Name remaining
  checks such as NACL rules, narrow egress, HTTPS, and EC2-to-RDS connectivity
  instead of implying the initial deployment is complete.
- Recheck live-state claims or date them, and compare code excerpts with the
  current repository. Review screenshots before publishing: record visible
  account/resource identifiers and remove secrets or personal data. Show console
  screenshots large enough to read or give a direct full-resolution link; do not
  shrink dense settings pages into a two-column thumbnail grid.
