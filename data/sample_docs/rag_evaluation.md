# Evaluating Retrieval-Augmented Generation

A reliable RAG evaluation separates retrieval quality from answer quality.
Retrieval should be measured with labeled questions and expected source
documents. Common ranking metrics include Recall at K, Mean Reciprocal Rank,
and normalized Discounted Cumulative Gain.

Answer evaluation should measure faithfulness, relevance, completeness, and
citation correctness. A grounded answer must be supported by the retrieved
context. Human review remains valuable for nuanced questions, while automated
evaluators help teams run regression tests on every code change.

Teams should maintain a versioned evaluation dataset that includes answerable
questions, ambiguous questions, and questions that cannot be answered from the
knowledge base. The unanswerable set tests whether the system safely refuses to
invent information.
