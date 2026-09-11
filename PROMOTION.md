# Manual review, promotion and synchronization

This project uses two repositories in one GitHub fork network:

| Repository | Role | Public site |
| --- | --- | --- |
| [`Esperimental/blog-staging`](https://github.com/Esperimental/blog-staging) | Development source and preview environment | https://esperimental.github.io/blog-staging/ |
| [`Esperimental/blog`](https://github.com/Esperimental/blog) | Production fork containing only reviewed revisions | https://esperimental.github.io/blog/ |

`blog` is technically a GitHub fork of `blog-staging`. That topology is intentional. Git history—not copied files—is the transport between environments.

No workflow, webhook, scheduled task, or **Sync fork** button promotes staging automatically.

## Invariants

1. Normal work is committed only to `blog-staging/main`.
2. Between releases, staging may be one or many commits ahead of production.
3. Production must not contain independent changes that are absent from staging.
4. Immediately after a completed promotion and synchronization, both `main` refs must point to the same commit. Their Git trees must therefore also be identical.
5. A difference is acceptable only while reviewed development is pending or while the final post-merge fast-forward is being completed.
6. Never copy a snapshot, manually duplicate files, cherry-pick, squash, or rebase between these repositories. Preserve their shared commit graph.

“The trees should not diverge” means they must not acquire separate lines of work. Staging being linearly ahead during development is expected.

## Development and staging review

1. Fetch both repositories and record the exact `blog-staging/main` and `blog/main` commit SHAs.
2. Before changing anything, verify that production is the same commit as staging or an ancestor of staging.
3. Commit changes to `blog-staging/main`. Multiple development commits are fine.
4. Confirm the staging GitHub Actions build and Pages deployment succeeded for the exact candidate commit.
5. Inspect the published staging home page and every affected page.
6. Check content, images, links, navigation, responsive overflow, accessibility basics, and the browser console when relevant.
7. Compare production with the reviewed staging commit and summarize exactly what would be promoted.

Do not open or merge a production pull request if production has changes that are not already in staging.

## Manual promotion

1. In `Esperimental/blog`, open a cross-repository pull request with:
   - base repository: `Esperimental/blog`
   - base branch: `main`
   - head repository: `Esperimental/blog-staging`
   - compare branch: `main`
2. Put the reviewed staging commit SHA and review findings in the pull request description.
3. Re-check the pull request diff and required Actions.
4. Make a deliberate go/no-go decision. Nothing merges merely because checks passed.
5. If approved, use **Create a merge commit**. Do not use squash merge or rebase merge; those rewrite the relationship needed for a clean fast-forward.
6. Record the resulting production merge commit SHA.

## Complete the synchronization

A GitHub merge commit belongs to production first. Because that commit has the reviewed staging tip as a parent, staging can then be fast-forwarded to it without changing any files:

```sh
git clone https://github.com/Esperimental/blog-staging.git
cd blog-staging
git remote add production https://github.com/Esperimental/blog.git
git fetch origin production
git switch main
git merge --ff-only production/main
git push origin main
```

The equivalent GitHub API operation is allowed only after verifying that the production merge commit is a descendant of the current staging tip. It must be a non-forced ref update.

Finally:

1. Verify `blog-staging/main` and `blog/main` have the same commit SHA.
2. Verify both Actions runs succeeded.
3. Inspect the production site.
4. Treat that shared commit as the new baseline for development.

This final fast-forward is part of promotion, not an optional cleanup.

## If the repositories diverge

Stop normal development and do not promote.

- If production is ahead only because a just-approved merge has not yet been synchronized, fast-forward staging as described above.
- If someone committed directly to production, merge production back into staging using Git, resolve conflicts deliberately, and run the complete staging build and visual review again.
- If both sides contain independent commits, create a reconciliation branch, merge the histories there, resolve conflicts, review its published result in staging, and only then resume the normal promotion flow.
- Never repair divergence by overwriting one repository with the other or by force-moving a branch.

## Repository-specific values

The source tree stays identical. Environment differences such as the Pages base path and source-repository link are injected by the GitHub Actions workflow from `${{ github.repository }}`. Do not hardcode `blog` or `blog-staging` into shared templates or content when the value is environment-specific.
