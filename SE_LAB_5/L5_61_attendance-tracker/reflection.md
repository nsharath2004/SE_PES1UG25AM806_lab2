# Lab 5: Static Code Analysis — Reflection

## 1. What was the most significant code quality or security issue identified, and why?
The most critical security issue discovered was the disabled SSL/TLS certificate verification in `syncToErp` (`requests.post(..., verify=False)`, Bandit `B501` - High Severity). Disabling certificate checks allows adversaries to intercept and alter sensitive student attendance and ERP API credentials via Man-in-the-Middle (MITM) attacks. Another equally critical vulnerability was shell wildcard execution in `backupReports` (`subprocess.Popen(..., shell=True)`, Bandit `B609`), which permits arbitrary command/argument injection through unvalidated filenames.

## 2. How did the static analysis tools complement each other in evaluating the codebase?
Each tool focused on a distinct pillar of software quality:
- **Bandit** acted as a security vulnerability auditor, flagging dangerous configurations such as disabled TLS validation, insecure default protocols (`PROTOCOL_TLSv1`), wildcard subprocess executions, and calls missing network timeouts.
- **Flake8** served as a PEP 8 compliance and syntactic linter, swiftly flagging formatting errors, line lengths exceeding 79 characters, blank spacing violations, and unused imported modules.
- **Pylint** performed comprehensive code quality, design, and structural analysis. It detected critical semantic traps such as mutable default arguments (`register={}`), resource management issues (unclosed file handles without context managers), and redundant expressions.

Using all three in concert ensured that stylistic, structural, and security aspects were thoroughly addressed.

## 3. What challenges or limitations did you encounter while using static analysis tools?
- **False Positives & Strict Conventions:** Pylint flagged camelCase naming styles (`invalid-name`) on predefined assignment function interfaces (`addStudent`, `markAttendance`). Since downstream consumers might rely on these exact function signatures, fixing them required balancing strict naming standards with API compatibility.
- **Context Obliviousness:** Static tools analyze syntax and data-flow patterns without runtime execution context. For example, Bandit flags any use of `subprocess` as potentially dangerous even when commands are fixed constants, while Pylint cannot evaluate whether business logic (e.g., whether attendance calculation rules match institutional policies) is correct.
- **Platform Discrepancies:** Commands such as `tar` or file redirection behave differently across Windows PowerShell and Unix-like environments (e.g. UTF-16 vs UTF-8 encoding defaults when redirecting standard output).

## 4. How can static code analysis be incorporated into a standard software development lifecycle (SDLC)?
Static code analysis can be systematically integrated across key development phases:
1. **Pre-commit Hooks:** Enforce lightweight linters (Flake8 and Black) via `pre-commit` hooks locally so formatting defects and unused imports are caught before code is even committed to version control.
2. **Continuous Integration (CI) Pipelines:** Integrate automated Bandit and Pylint stages into GitHub Actions or GitLab CI. Pull requests can be configured to require a minimum Pylint threshold (e.g., $\ge 9.5$) and zero medium/high Bandit security findings before merging is permitted.
3. **IDE Integration:** Equip developers with in-editor static analysis extensions that provide real-time visual feedback while code is being written, reducing turnaround time and technical debt.
