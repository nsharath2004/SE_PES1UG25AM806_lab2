# Issues Identified and Resolved (Static Code Analysis)

This document details the issues discovered by **Bandit**, **Pylint**, and **Flake8** during the static code analysis of `attendance_tracker.py`, along with their classifications and the fix approaches applied.

## Summary Table

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Insecure SSL Certificate Verification (`B501`) | Security (High) | 60 | `requests.post()` invoked with `verify=False`, disabling TLS/SSL certificate verification and exposing traffic to man-in-the-middle (MITM) attacks. | Enabled full certificate validation by changing `verify=False` to `verify=True`. |
| Wildcard Injection via Shell Subprocess (`B609`, `B602`, `B607`) | Security (High / Low) | 64 | `subprocess.Popen("tar -czf reports_backup.tgz *.csv", shell=True)` executes shell with wildcard arguments vulnerable to argument and command injection. | Replaced shell command with native Python standard library module `tarfile` (`tarfile.open`), creating the compressed archive without subprocess or shell execution. |
| Missing HTTP Request Timeout (`B113`, `W3101`) | Security / Reliability (Medium) | 60 | `requests.post()` invoked without an explicit `timeout` parameter, allowing hung network connections to block the process indefinitely. | Added an explicit `timeout=10` parameter to the request invocation. |
| Insecure Legacy SSL Protocol Default (`B503`) | Security (Medium) | 66 | `legacyChannel` defaulted to deprecated and insecure `ssl.PROTOCOL_TLSv1`. | Updated default protocol version to secure modern TLS (`ssl.PROTOCOL_TLS_CLIENT`). |
| Insecure `shell=True` Parameter Passing (`B604`) | Security (Medium) | 73 | `scheduleReminders()` called `runJob("send_sms --shortage", shell=True)`, invoking subprocesses through system shell unnecessarily. | Set `shell=False` and safely tokenized command strings with `shlex.split()`. |
| Dangerous Mutable Default Argument (`W0102`) | Bug / Code Smell (Warning) | 18 | `register={}` shared a single mutable dictionary instance across all function invocations where the argument was omitted. | Changed default parameter to `register=None` and initialized `target_register = attendance_register if register is None else register` to maintain state properly. |
| Unclosed File Resource & Missing Encoding (`R1732`, `W1514`) | Reliability / Style (Refactor/Warning) | 50–55 | File opened using `f = open(path, "w")` without context manager (`with`) or explicit encoding specification. | Replaced with `with open(path, "w", newline="", encoding="utf-8") as f:`. |
| Unused Imports (`W0611`, `F401`) | Cleanliness (Warning/Error) | 1, 4, 6 | Modules `os`, `json`, and `datetime.datetime` were imported but never used anywhere in the file. | Removed all unused imports. |
| PEP 8 Formatting & Style Violations (`E302`, `E501`, `E712`, `E305`) | Style / PEP 8 | 15–96 | Missing 2 blank lines between top-level functions, lines exceeding 79 characters, and anti-pattern boolean comparisons like `== False`. | Re-formatted code according to PEP 8 standards with appropriate spacing, wrapped lines under 79 characters, and simplified conditional expressions. |
| Missing Documentation (`C0114`, `C0116`) | Code Quality (Convention) | 1, 15–75 | Module and functions lacked descriptive docstrings explaining their parameters and purpose. | Added comprehensive PEP 257 docstrings for the module and all functions. |
