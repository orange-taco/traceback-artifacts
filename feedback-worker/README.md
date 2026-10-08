# Private feedback for TRACEBACK artifacts

The public guides stay at `https://orange-taco.github.io/traceback-artifacts/`.
This Worker provides a separate iPad-friendly feedback form. It writes JSON files
to a private GitHub repository after checking the signed-in GitHub account's
numeric ID. Saving feedback never starts Codex or edits a guide.

GitHub Pages and a private GitHub repository can stay on their free plans, and
the Worker can run within [Cloudflare's free request allowance](https://developers.cloudflare.com/workers/platform/pricing/)
for personal use. Cloudflare still needs its own account. This design does not
use the OpenAI API or add API billing; Codex Cloud tasks use the existing
ChatGPT plan and its limits.

## One-time setup

1. Create a **private** `oscar2272/traceback-feedback` repository with a `main`
   branch. Do not put it under the public `orange-taco/traceback-artifacts` repo.
2. In Cloudflare's free Workers plan, run `npm ci`, sign in with
   `npx wrangler login`, then run `npx wrangler deploy` here to obtain the Worker
   HTTPS URL. The `workers.dev` URL is suitable for this small personal form.
3. Register a private GitHub App owned by `oscar2272`. Set its website URL to
   the Worker origin and its callback to `<worker-origin>/oauth/callback`.
   Disable webhooks, grant only **Contents: Read and write** repository
   permission, and install it on **only** `traceback-feedback`. Record the
   App ID, Client ID, and installation ID. Generate a client secret and a private
   key. GitHub's [App setup documentation](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app)
   describes these settings.
4. Convert the downloaded private key to PKCS#8 if necessary:

   ```sh
   openssl pkcs8 -topk8 -nocrypt -in github-app.pem -out github-app-pkcs8.pem
   ```

   Add these **Worker secrets**, never repository files or browser code:

   ```sh
   npx wrangler secret put GITHUB_APP_CLIENT_ID
   npx wrangler secret put GITHUB_APP_CLIENT_SECRET
   npx wrangler secret put GITHUB_APP_ID
   npx wrangler secret put GITHUB_APP_INSTALLATION_ID
   npx wrangler secret put GITHUB_APP_PRIVATE_KEY < github-app-pkcs8.pem
   npx wrangler secret put SESSION_SECRET
   ```

   Use a fresh random value of at least 32 bytes for `SESSION_SECRET`. Keep the
   PEM files outside this repository and delete local copies when no longer
   needed. The Worker requests a short-lived installation token scoped to the
   feedback repository for each save. The login token is used only to identify
   the GitHub user and is discarded after the callback.
5. Set the **repository Actions variable** `FEEDBACK_WORKER_ORIGIN` in
   `orange-taco/traceback-artifacts` to the Worker HTTPS origin, with no path or
   trailing slash. Run the Pages workflow or merge a change to `main`. The
   workflow writes `site-config.json` with the exact deployed Git revision and
   Worker origin. The shared script shows the feedback link on each guide only
   when this config exists.
6. Add `oscar2272/traceback-feedback` as a fourth repository in the personal
   Codex Cloud environment and republish it. In a new Cloud task, ask Codex to
   read `feedback/<id>.json` in that repository. The user must separately ask
   Codex to revise an artifact and create a PR; saving never triggers a task.

## Data and access

The form records `document_url`, `section_id` (or null), `selected_text` (null),
`location`, `comment`, `document_revision`, `author.github_id`, `author.login`,
and `created_at`. The URL must be a guide on the public Pages origin; the
revision must be a 40-character commit ID. The server checks a signed,
HTTP-only session for the fixed numeric GitHub account ID `88140361`, same-origin
form submission, and a CSRF token. Other accounts receive HTTP 403 at login;
unauthenticated saves receive HTTP 401. There is no modify or run endpoint.

The login and feedback form live on the Worker origin. This full-page navigation
avoids third-party cookies between `github.io` and `workers.dev` in iPad Safari.
GitHub and OpenAI credentials are never placed in Pages files. GitHub App
credentials stay in Worker secrets. The private repository itself must remain
private; access to its files follows the GitHub permissions granted to its
collaborators and to the Codex Cloud connection.

## Verification

```sh
npm ci
npm test
npx wrangler deploy --dry-run
python3 ../scripts/verify_site.py
```

After deployment, verify on an iPad-size viewport that the feedback link opens
the form, the GitHub login returns to the same document, an `oscar2272` save
creates one private JSON file, and a different GitHub account gets HTTP 403.
Start a new Codex Cloud task and confirm it can read that file. No live login,
private write, or Cloud read is claimed until those checks actually succeed.
