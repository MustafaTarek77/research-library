# CPU benchmark — 29 October 2026

CPU inference is feasible for a small assignment demonstration. The measured
full-paper path took about **2 minutes 21 seconds**, including PDF conversion.
The small model produced valid metadata but the summary was generic. This is a
baseline result, not a general quality evaluation or a throughput guarantee.

## Setup

| Item | Value |
| --- | --- |
| CPU | AMD Ryzen 9 5900HX, 8 cores / 16 logical processors |
| Environment | WSL2, Python 3.12.3, approximately 9.7 GiB RAM available to WSL |
| Ollama | 0.34.0, isolated server on localhost:11435 |
| Model | qwen2.5:1.5b, Q4_K_M, approximately 986 MB download |
| Model digest | `65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b` |
| Inference | 8 threads, num_gpu=0, temperature=0, seed=42 |
| Context / output limit | 32,768 / 512 tokens |
| Input | Complete 13-page MapReduce paper, 56,512 Markdown characters |
| Actual prompt | 13,351 tokens, including instructions |

[Paper and source PDF](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/).
PDF conversion used PyMuPDF4LLM 0.0.27 with PyMuPDF 1.26.7.

## Measurements

| Stage or request | Wall time |
| --- | ---: |
| PDF conversion | 2.25 s |
| First inference, unloaded model and uncached paper | 138.74 s |
| Conversion + first inference | 140.99 s |
| Second inference, same cached paper | 9.82 s |
| Third inference, same cached paper | 9.81 s |

First-request server timing counters show approximately 2.81 s for model
loading, 127.01 s for reading the prompt, and 8.83 s for output generation.
Generation throughput was approximately 13.93 tokens/s; later requests measured
about 14.3 tokens/s. Small differences between component totals and wall time
come from server/client overhead.

The repeated requests reused **13,350 of 13,351 prompt tokens**. Their 10-second
times must not be presented as the expected time for a new paper. The first
request had zero cached prompt tokens. Model unloading does not clear the
operating system's filesystem cache, so this is not a cold-disk benchmark.

Ollama reported zero VRAM allocation on all three runs. It reported about
1.98 GiB of model/context allocation. A process sample during inference showed
about 2.01 GiB resident memory for the model process; this was a sample, not a
measured peak. Server logs confirmed a 32,768-token context and `truncated = 0`.

## Output review

- All three responses contained valid JSON and passed the required field/type
  checks on their first attempt. No validation retry was needed.
- All three extracted the exact paper title.
- Keywords were relevant to the paper. The category was the broad label
  `Computer Science`.
- The summaries accurately described the general purpose and distributed
  execution setting. The first was especially generic and omitted an explicit
  description of the map/reduce steps; later responses described them.
- Summaries were 59, 74, and 74 words, despite a prompt requesting 80–120 words.
  That length is a prompt preference, not an assignment requirement or a
  validation rule. Schema-constrained JSON does not guarantee content quality.
- This is one well-known paper. Review an unfamiliar paper before treating the
  model as a final quality choice. Temperature zero also did not produce
  identical cold and cached responses in this run.

## Recommendation and boundaries

Continue with the local architecture and use this model provisionally. Process
papers sequentially and prevent overlapping Airflow runs from competing for
CPU. Improve the summary prompt or reconsider the small model if later content
reviews are unsatisfactory. Colab is not needed to demonstrate the measured
workload.

This measurement does not include Airflow overhead or concurrent resource use,
SQLite writes, HTML rendering, Drive sync, Discord delivery, or model download.
It does not establish timing for scanned PDFs or papers beyond the context
window. Long-paper handling still needs an explicit design.

The original system Ollama service was verified inactive, with port 11434 no
longer listening, before inference. The isolated benchmark server used 11435.

## Reproduce and inspect

See [README setup instructions](../README.md). Run:

```bash
PYTHONPATH=src .venv/bin/python scripts/benchmark_cpu.py \
  data/benchmark-inputs/mapreduce.pdf --runs 3
```

The local [raw report](../benchmarks/cpu-mapreduce.json) contains input checksum,
model details, environment information, timing counters, cache counts, complete
generated metadata, and CPU allocation checks. Raw JSON and downloaded assets
are ignored by Git; this summary is suitable for the repository.
