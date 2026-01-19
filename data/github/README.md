# Statistics of my Github projects

How many, categories, files?

title (repository name), created, size, main language, category, files, folders, commits. This goes to the `/data/github/repos.csv/`.

## Update this statistics-diary repository

### Trigger

When the `quartz` repository has a successful run, the `deploy.yml` will be executed by GitHub Actions. It has three stages, the build and deploy are originally from the description for GitHub Pages hosting: [https://quartz.jzhao.xyz/hosting](https://quartz.jzhao.xyz/hosting). It will not be overwritten when updating quartz, since it is not found in the original repository: [https://github.com/jackyzha0/quartz/tree/v4/.github/workflows](https://github.com/jackyzha0/quartz/tree/v4/.github/workflows)

Curreently I have 6 workflows, 4 from the repository copy, one build by me with instructoins above and another one from the dependabot:

- Docker build & push image (docker-build-push.yaml) 61x, usually skipped
- Deploy Quartz site to GitHub Pages (deploy.yml) 53x
    - build (35 seconds)
    - deploy (11 seconds)
    - trigger (3 seconds)
- Upload Preview Deployment (deploy-preview.yaml) 26x
- Build and Test (ci.yaml) 83
- Build Preview Deployment (build-preview.yaml) 26x
- Dependabot Updates ... 50x

The extra job (after build and deploy) for the trigger step is:

``` yaml
  trigger:
    needs: deploy
    runs-on: ubuntu-latest
    steps:
      - name: Run build
        run: echo "Build in Quartz completed!"

      - name: Trigger statistics-diary workflow
        if: ${{ success() }}   # ✅ correct syntax
        run: |
          curl -X POST \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer ${{ secrets.REPO_B_TOKEN }}" \
            https://api.github.com/repos/kreier/statistics-diary/dispatches \
            -d '{"event_type":"trigger-from-repo-quartz"}'
```

### Update process

The event **trigger-from-repo-quartz** is recieved by the `.github/workflows/update.yml` Action that has just one job, update. But it has several steps:

- Checkout repository
- Set up Python
- Run update script
    - python/update_version.py
- Commit and push changes
    - git add data/iteration.json data/version.txt

I have 2 Github Action workflows:

- pages-build-deployment (no file, it's the Github Pages automatic runner)
- Update Version (update.yml)

For the automatic update only the `update.yml` is relevant. I can trigger it manually, and should probably rename it to Update Statistics. Almost all relevant data is found in this file - and to be changed. Trigger stays the same.
