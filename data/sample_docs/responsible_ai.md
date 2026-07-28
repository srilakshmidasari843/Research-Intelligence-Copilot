# Responsible AI for Document Assistants

Document assistants should expose their sources, protect sensitive data, and
communicate uncertainty. Citations allow users to inspect evidence instead of
blindly trusting a generated answer.

Access control should be enforced before retrieval so that a user cannot obtain
content from a document they are not authorized to view. Logs should avoid raw
confidential text and personally identifiable information.

Teams should monitor unsupported claims, retrieval failures, latency, cost, and
feedback. Security testing must include prompt injection inside uploaded
documents because retrieved content may contain malicious instructions.
