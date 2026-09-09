# Security policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.9.x   | Yes       |
| 0.8.x   | Yes       |
| < 0.8   | No        |

## Reporting a vulnerability

If you discover a security vulnerability in `reachq`, report it privately through
[GitHub Security Advisories](https://github.com/sachncs/reachq/security/advisories/new).
You can also email the maintainer at `sachncs@gmail.com`. **Please do not report
security vulnerabilities through public GitHub issues.**

When you report, include:

1. A description of the vulnerability.
2. Steps to reproduce the issue.
3. The potential impact.
4. A suggested fix, if you have one.

### Response expectations

- **Acknowledgement**: within 48 hours of your report.
- **Assessment**: within 5 business days.
- **Fix**: a patch release within 14 days for critical vulnerabilities.
- **Disclosure**: we coordinate the public disclosure timing with you.

### Scope

This policy covers:

- The `reachq` Python package.
- The GitHub repository and its CI/CD pipeline.
- The documentation site and example code.

It does not cover vulnerabilities in third-party dependencies (report those to
the upstream maintainer), issues that require physical access to the user's
machine, or social-engineering attacks.

## Security best practices

When you use `reachq` in production:

1. **Pin dependencies**. Use `requirements.txt` or a lockfile to pin exact versions.
2. **Use virtual environments**. Isolate project dependencies.
3. **Run untrusted input with limits**. Large graphs can consume significant memory and time; set limits before processing untrusted input.
4. **Validate inputs**. While `reachq` accepts arbitrary graphs, validate the input data before passing it in.
5. **Monitor dependencies**. Use `pip-audit`, GitHub Dependabot, or an equivalent tool.

## Dependency security

We use GitHub Dependabot to monitor known vulnerabilities in our dependencies.
If you find a vulnerability in a dependency:

1. Check whether a patched version exists.
2. Update the version in `pyproject.toml`.
3. Test the change.
4. Open a pull request with the fix.

## Code security

This library is computational. There are no network-facing components, but
note:

- **Memory usage**: large graphs consume significant memory. Set limits before processing untrusted input.
- **Computation time**: some algorithms have super-linear complexity. Set timeouts before processing untrusted input.
- **Numerical precision**: floating-point operations in shortest-path algorithms may have precision limits for very large or very small inputs.