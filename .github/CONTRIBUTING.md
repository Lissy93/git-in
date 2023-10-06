
## Introduction

One of the biggest barriers to entry for first-time and newer contributors is the Git and GitHub process. The aim of this repo is to provide an easy and safe space for you to get more comfortable with the contribution process. We welcome PRs from developers of all levels and experiences, and we've tried to make the process as straightforward as possible.

| ⚠️ <ins>Important</ins>: Before submitting your pull request, please ensure you're following [these Guidelines](#guidelines)! |
|--|

---

## How 

You've got two options: The easiest, and sometimes best for just small changes is to use the GitHub UI, or Codespaces - this is explained in [this step-by-step tutorial](https://github.com/Lissy93/git-into-open-source/blob/main/guides/submit-your-first-pr-ui.md).
In the longer term, and especially once you're working on larger changes, you'll want to have Git installed on your system, and make changes locally, again instructions for which are [outlined here](https://github.com/Lissy93/git-into-open-source/blob/main/guides/submit-your-first-pr-cli.md).

Prerequisites: You will need a GitHub account. If you're planning on making changes via the terminal, you'll also need Git installed, and an SSH key setup on your local system.
For a step-by-step guide, see [setting up Git, GitHub, SSH](https://github.com/Lissy93/git-into-open-source/blob/main/guides/local-git-setup.md)

---

## Areas for Contribution

Not sure what to add or work on? Here's 10 ideas to get you started!

### Add your Name!

This is probably the easiest place to start for first-time contributors. On the readme, there's a list of names and comments from developers, and you can add yours in there too! 

It's important to note that you don't put this in the readme directly, but rather edit the [`git-in-here.yml`](https://github.com/Lissy93/git-into-open-source/blob/main/git-in-here.yml) file instead (there's a template at the top), this is then fetches some additional info from the GitHub API (like your name, picture and stargazer status) and inserts it into the readme using [this workflow](https://github.com/Lissy93/git-into-open-source/blob/main/.github/workflows/insert-comments.yml) running on GitHub Actions.

### Guides

I'm working on putting together a series of guides, aimed at helping new developers get up to speed with Git, and get into Open Source.

These can be found in the [`/guides`](https://github.com/Lissy93/git-into-open-source/tree/main/guides) directory, and any contributions would be much appreciated! If you're adding a new guide, it also needs to be listed in the [`resources.yml`](https://github.com/Lissy93/git-into-open-source/blob/main/resources.yml) file, for it to be shown on the website and in the readme.

### Resources

The readme and website also list to some helpful external resources, as there's no point reinventing the wheel when there are already some excellent guides and tools out there.

If you know of any sites that are not already listed, which you think could be helpful, you can add these into the [`resources.yml`](https://github.com/Lissy93/git-into-open-source/blob/main/resources.yml) file (under the `resources` section), and they'll be automatically inserted into the readme (using [this workflow](https://github.com/Lissy93/git-into-open-source/blob/main/.github/workflows/insert-resources.yml)).

Keep in mind - I would ideally like to keep the resources list short, with only the best tools and websites listed, so if you're adding something ensure it meets this criteria, and provide justification.

### Website

We've also got a simple static site, that makes it easier to read some of the guides; it's hosted on GitHub Pages, at [lissy93.github.io/git-into-open-source](https://lissy93.github.io/git-into-open-source/)

It's built using [Astro](https://astro.build/), so is very easy to get up to speed with quickly. The source, as well as setup docs can be found in the [`web/`](https://github.com/Lissy93/git-into-open-source/tree/main/web) directory.

### Scripting

The repo is held together with a set of pretty simple Python scripts that insert the user-contributed content in the readme, and make it available via the website.

These can be found in the [`/lib`](https://github.com/Lissy93/git-into-open-source/tree/main/lib) directory.

If you're a Python developer, you'll see that there's plenty of room for improvement here! Whether it's refactoring, writing tests, fixing a bug, adding a feature or anything else - PRs here are very much welcome!

### Docs

Have you noticed anything not right in the readme or any of the other docs here? Whether it's correcting spelling / grammar, improving instructions or fixing formatting - pull requests are always appreciated!

### Translations

// TODO: I need to first add the architecture for this!

### Something Else?

I'm up for reviewing pull requests for other areas of this repository, not listed above. If you're unsure if your intended contribution would be a good fit or not, feel free to open an issue first, and we can chat about it :)

### Not a coder?

There's plenty of other ways you can support open source projects! 

- Open an issue to report a bug
- Write a tutorial or blog post
- Leaving constructive feedback
- Reviewing open pull requests
- Contributing to docs
- Adding international translations
- Helping with testing
- Assisting with UI, UX or asset design
- Sponsoring the project or author
- Sharing the project within your network

### Still nothing?

There's plenty of other repositories on GitHub looking for contributors! Whatever your skill set or level, there will surly be the perfect project for your first few open source contributions. Take a look at this guide: [Finding Projects to Contribute to](https://github.com/Lissy93/git-into-open-source/blob/main/guides/finding-projects-to-contribute-to.md)

---

## Guidelines

> ‼️ Please familiarise yourself with this checklist **before** submitting your pull request.<br>
> ❌ PRs which <ins>do not follow these guidelines</ins>, or that are <ins>low-effort</ins> will <ins>**not be merged**</ins>.<br>
> ⭕ These requirements are in place in order to keep the content in this repo high quality :)

When submitting a pull request, you must:
- Complete the PR template appropriately
- Agree to follow the Code of Conduct
- Not submit low-effort or AI-generated content

When adding your name and response to [`git-in-here.yml`](https://github.com/Lissy93/git-into-open-source/blob/main/git-in-here.yml),
you must ensure that:
- Your addition must be appended to the end of the file
- The file must end in a single blank line
- The username must match YOUR GitHub username
- The question must exist in the list
- The response should be between 64 and 512 characters
- The response should be wrapped onto the next line if it's over 100 chars
- The response must not be spammy, low effort or AI-generated (important!)
- The response must be in English, with correct spelling and grammar

Top tips for adding a great response:
- **Be imaginative!** Ensure your response is something that will engage, educate, or delight those who read it in the future ![important](https://img.shields.io/badge/Important!-F6094E)
  - Great advice, insightful thoughts, jokes and fun facts are all awesome
- **Markdown is supported!** So you can include links and basic formatting
  - Feel free to link to your projects, website or helpful (SFW) resources
  - Hyperlinks (`[text to display](https://example.com)`), new lines (`<br />`) as well as `**bold**` and `_italic_` all work
- **Get a gold star by your name!** Drop a star on this repo, and you'll automatically get a star next to your response

When adding a resource to [`resources.yml`](https://github.com/Lissy93/git-into-open-source/blob/main/resources.yml),
you must:
- Not submit blog posts or articles, unless they provide considerable value to the reader
- Not submit anything which is duplicate content, or very similar to an existing resource
- Disclose any association you may have to that website
- Provide a short sentence of justification in your PR, explaining why it should be included

When submitting additions or changes to the guides in [`guides/`](https://github.com/Lissy93/git-into-open-source/tree/main/guides),
you must:
- Ensure all new information is, to the best of your knowledge accurate and correct
- Spell and grammar check your new additions, and ensure that any included links are functional
- Not provide links to content you own, manage or are affiliated with, without disclosing your association when submitting the pull request
- If you're adding a new guide, don't forget to also list it in the resources file, so it can be indexed

When submitting changes to the website in [`web/`](https://github.com/Lissy93/git-into-open-source/tree/main/web),
you must:
- Ensure the application is still fully deployable
- Ensure there are no regressions / no new bugs introduced
- Ensure all lint checks, tests and build scripts still pass

When submitting changes to the website in [`lib/`](https://github.com/Lissy93/git-into-open-source/tree/main/lib),
you must:
- Ensure that all scripts still run as expected
- Ensure there are no regressions / no new bugs introduced
- Ensure all lint checks, tests and build scripts still pass

There's a few no-go zones, where changes will be overridden by the dynamically inserted content. Therefore:
- When editing markdown, do not manually submit any content between the `<!-- xx-start -->` and `<!-- xx-end -->` tags - this is auto-generated, and so will be overridden!
- Don't edit the markdown within the `web/` directory, as this is generated using the content from `/guides`, and metadata from `resources.yml`
- Only submit pull requests to the repo on GitHub (lissy93/git-into-open-source), as our Codeberg mirror is one-way, so changes will be overridden
