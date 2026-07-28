# MLOps for RAG Applications

Production RAG systems need versioning for source documents, chunking
configuration, embedding models, prompts, and evaluation datasets. A change to
any of these components can affect response quality.

Continuous integration should run unit tests and retrieval regression tests.
Deployment pipelines should promote immutable application images across
environments. Monitoring should cover latency, errors, retrieval quality,
answer faithfulness, token consumption, and cost.

Rollback requires preserving the prior application image and the compatible
index version. Observability should connect a user request to retrieval results
and generation output without exposing sensitive document content.
