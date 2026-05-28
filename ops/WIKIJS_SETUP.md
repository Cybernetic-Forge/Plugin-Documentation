# Wiki.js First-Run Setup

Use this after the Docker stack is deployed and the site is reachable.

## 1. Complete the setup wizard

Open the deployed Wiki.js URL and finish the initial admin setup.

## 2. Configure Git storage

Official Wiki.js docs recommend a **dedicated Git repository** for storage sync. In this repo, that role is handled by the `wikijs-content` branch.

In **Administration > Storage**:

- enable the `Git` storage target
- set **Authentication Type** to `ssh`
- set **Repository URI** to your repository SSH URL
- set **Branch** to `wikijs-content`
- set **SSH Private Key Path** to `/wiki/data/ssh/wikijs-content`
- leave username and password empty
- set **Default Author Name** and **Default Author Email** to your preferred commit identity
- keep **Local Repository Path** at `./data/repo` unless you have a specific reason to change it
- set **Sync Direction** to **Pull** / one-way remote import
- set **Sync Schedule** to `5 minutes`

Apply the changes and wait for the Git storage module to become healthy.

## 3. Import the generated content

Still in the Git storage module screen:

- run **Import Everything**

That imports the generated pages from the `wikijs-content` branch into the Wiki.js database.

## 4. Navigation

Recommended Wiki.js navigation mode:

- **Custom Navigation** or **Site Tree**

The generated content includes:

- `/home`
- `/plugins`
- `/plugins/<plugin>`
- `/plugins/<plugin>/commands`
- `/plugins/<plugin>/configuration`
- `/plugins/<plugin>/api_information`

## 5. Theme

The Cybernetic-Forge theme is applied automatically by the Nginx proxy layer.

You do **not** need to paste CSS into the Wiki.js admin area unless you want extra instance-specific tweaks.

## 6. Content editing model

- Edit source markdown on `main`
- The `publish-wikijs-content.yml` workflow regenerates and force-publishes the dedicated content branch
- Wiki.js then pulls generated content from `wikijs-content`

Recommended approach:

- treat `main` as the authoritative documentation source
- treat `wikijs-content` as generated output
- use Wiki.js primarily for presentation, navigation, and search

If you edit pages directly in Wiki.js, manually copy those changes back into the source markdown before the next content publish run, otherwise the generated branch will overwrite them.
