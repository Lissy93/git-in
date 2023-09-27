
## Introduction

One of the biggest barriers to entry for first-time and newer contributors is the Git and GitHub process. The aim of this repo is to provide an easy and safe space for you to get more comfortable with the contribution process. We welcome PRs from developers of all levels and experiences, and we've tried to make the process as straightforward as possible.

---

## How 

You've got two options: The easiest, and sometimes best for just small changes is to use the GitHub UI, or Codespaces - this is explained in [this step-by-step tutorial](https://github.com/Lissy93/git-into-open-source/blob/main/guides/submit-your-first-pr-ui.md).
In the longer term, and especially once you're working on larger changes, you'll want to have Git installed on your system, and make changes locally, again instructions for which are [outlined here](https://github.com/Lissy93/git-into-open-source/blob/main/guides/submit-your-first-pr-cli.md).

Prerequisites: You will need a GitHub account. If you're planning on making changes via the terminal, you'll also need Git installed, and an SSH key setup on your local system.
Some projects may also require certain tools and build systems to be installed, such as Node.js or Python.

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

The below are a list of contributing guidlines, that you must follow.

You must adhere 
