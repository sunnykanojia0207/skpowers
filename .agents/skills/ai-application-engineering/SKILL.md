---
name: ai-application-engineering
description: Design, implement, test, and operate production AI features using LLM APIs, RAG, tool calls, structured output, and evaluations.
---
# AI Application Engineering

## Requirements and architecture
- Define the user problem and an observable quality target before selecting a model or framework.
- Separate deterministic business rules from probabilistic model behavior. Keep authorization, billing, and irreversible actions in ordinary application code with server-side checks.
- Compare hosted APIs and self-hosted models against quality, latency, cost, privacy, region, rate limits, and operational burden. Avoid selecting by benchmark alone.
- Isolate provider calls behind an interface; set explicit timeouts, retry policy, concurrency limits, and fallbacks. Make retries idempotent where possible.

## Prompt and tool safety
- Treat user content, retrieved documents, webpages, files, and tool outputs as untrusted data; prompt injection can arrive through any of them.
- Never put secrets, credentials, private system prompts, or privileged raw tool outputs into the model context unless strictly required and approved.
- Enforce tool allowlists, schema validation, authorization, and resource limits outside the model. The model's decision is not an authorization check.
- Require explicit human confirmation before financial, destructive, externally visible, or production-impacting actions.
- Use structured outputs/schema constraints where supported, validate every result, and handle refusals, truncation, malformed responses, and provider failures.

## Retrieval / RAG
- Define corpus permissions, chunking, metadata, update/delete behavior, and access-control filtering before retrieval implementation.
- Enforce document-level authorization before passing retrieved content to the model; don't rely only on a prompt saying “ignore unauthorized documents.”
- Include source references where answers need grounding. Measure retrieval relevance separately from answer quality.
- Protect against malicious instructions embedded in retrieved content, stale indexes, cross-tenant leakage, and accidental PII exposure.

## Evaluation and testing
- Build a versioned representative evaluation set before optimizing prompts/models. Include normal cases, edge cases, adversarial/prompt-injection cases, unsupported questions, and permission boundaries.
- Use deterministic tests for application logic and schema/tool contracts; use rubric-based or model-based evaluation only with defined thresholds and review of false positives/negatives.
- Track quality, groundedness, refusal correctness, p50/p95 latency, token usage, cost per successful task, and failure rates.
- Regression-test prompts, model versions, embedding changes, chunking, and retrieval settings before release.
- Never claim quality improvement from anecdotes alone; show evaluation results and caveats.

## Reliability and privacy
- Apply per-user and per-tenant quotas, rate limits, cost ceilings, cancellation/timeouts, and abuse detection.
- Log request IDs, model/version, latency, token/cost metrics, and outcome; redact or avoid logging sensitive prompt/response content by default.
- Define data retention and deletion behavior for prompts, embeddings, traces, and provider logs. Review vendor data policies before production.
- Provide clear UI states for processing, partial results, errors, and “I don't know.” Don't present probabilistic output as verified fact without suitable evidence.
- Keep secrets in the backend/environment secret manager. Never expose provider API keys to browser or mobile clients.
