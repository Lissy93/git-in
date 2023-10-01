# Security Policy

## Supported Versions

We currently support the latest version of our repository for security updates.
As the repository mainly consists of static files and scripts, only the latest state is considered for patches.

## Reporting a Vulnerability

Your security is paramount to us. If you discover any security-related issues or vulnerabilities, we encourage you to report them responsibly.

Please do not report exploitable security vulnerabilities through public GitHub issues.

### How to Report

- **Email**: Send your findings to security@mail.alicia.omg.lol. Please provide as much information as possible about the vulnerability, steps to reproduce, and its potential impact.
- **Expect a Confirmation**: We will acknowledge receipt of your vulnerability report within 48 hours.
- **Discussion**: After initial triage, we'll engage in further discussion with you about the issue, if necessary.
- **Disclosure**: Once we've assessed the issue, we'll work on a fix. We appreciate your discretion, and we will strive to address and deploy fixes in a timely manner. We will also give credit for the reported vulnerability as per your preference.

## Scope

We're especially interested in vulnerabilities in:

- **Data Integrity**: Manipulations or unintended uses of the data in git-in-here.yml and resources.yml.
- **Scripts in /lib/**: Any issues that could lead to data corruption, leak, or other security concerns.
- **Static Website in /web/**: Vulnerabilities that might expose user data, lead to misinformation, or can manipulate the content displayed.
- **Guides in /guides/**: Though these are mainly markdown files, any misuse that could lead to confusion or misinformation is crucial.

While these are our primary areas of interest, any security-related concerns in other parts of the repository are also welcome.
Safe Harbor

We aim to encourage the responsible disclosure of security vulnerabilities. We will not take legal action against individuals who provide such reports. We consider ethical hacking activities conducted consistent with this policy a "permitted" action.
