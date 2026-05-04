# Security Policy

## Supported Versions

This package follows the **current Django LTS support window**. Security patches are released only for the latest version line that targets a Django LTS still under upstream support.

| Version  | Django LTS supported     | Status      |
|----------|--------------------------|-------------|
| 0.0.6+   | Django 4.2 LTS, 5.2 LTS  | Supported   |
| < 0.0.6  | Django 4.2 only          | End of life |

When Django releases a new LTS (e.g. 6.2 in April 2027), the support matrix above will widen. When an LTS reaches the end of its upstream extended-support window, this package drops support for it in the next minor release.

## Reporting a Vulnerability

**Please do not file a public GitHub issue for security vulnerabilities.** Public disclosure before a fix is available puts users at risk.

Report security issues privately via either of the following channels — GitHub Security Advisories is preferred because it tracks the entire coordinated-disclosure conversation in a private space attached to the repository.

1. **GitHub Security Advisory** (preferred): [open a private advisory](https://github.com/karthicraghupathi/django_rapyd_modernauth/security/advisories/new)
2. **Email**: <karthicr@gmail.com>

When you report, please include:

- A description of the issue and the impact you believe it has
- Steps to reproduce, or a proof-of-concept
- The version of `django-rapyd-modernauth` and Django you tested against

## What to Expect

- **Acknowledgement** within 7 days of the initial report
- **Status update** within 30 days, including either a planned fix timeline or an explanation of why the report does not warrant action
- **Coordinated disclosure** of 30–90 days from the initial report by default; we are open to adjusting this in either direction based on the severity of the issue and the complexity of the fix
- **Credit** in the release notes and any security advisory, if you wish to be named (you can also remain anonymous)

For non-security bugs and feature requests, please use the regular [issue tracker](https://github.com/karthicraghupathi/django_rapyd_modernauth/issues).
