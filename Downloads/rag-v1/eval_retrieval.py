import json
import sys
from pathlib import Path

from rag_core import RagError, ask, corpus_names, load_settings, retrieve


def norm(s: str) -> str:
    return " ".join(s.split()).lower()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    use_llm = "--llm" in sys.argv
    top_k = int(args[0]) if args else 5
    questions = json.loads(Path("eval/questions.json").read_text(encoding="utf-8"))
    docs = corpus_names()
    settings = load_settings()

    rows = []
    for q in questions:
        try:
            chunks = retrieve(q["question"], docs, top_k)
        except RagError as e:
            print("Cannot retrieve:", e.message)
            return
        rank = None
        if q["answerable"] and q.get("evidence"):
            needle = norm(q["evidence"])
            for i, c in enumerate(chunks):
                if needle in norm(c["text"]):
                    rank = i + 1
                    break
        row = {
            "id": q["id"],
            "question": q["question"],
            "answerable": q["answerable"],
            "hit": (rank is not None) if q["answerable"] else None,
            "rank": rank,
            "top_distance": chunks[0]["distance"] if chunks else None,
        }
        if use_llm:
            try:
                out = ask(q["question"], docs, top_k)
                row["llm_status"] = out["status"]
                row["llm_answer"] = out["answer"]
            except RagError as e:
                row["llm_status"] = "error:" + e.code
        rows.append(row)

    answerable = [r for r in rows if r["answerable"]]
    unanswerable = [r for r in rows if not r["answerable"]]
    hits = [r for r in answerable if r["hit"]]
    summary = {
        "chunk_size": settings.chunk_size,
        "overlap_percent": settings.overlap_percent,
        "top_k": top_k,
        "answerable_questions": len(answerable),
        "hit_at_k": len(hits) / len(answerable) if answerable else None,
        "mrr": sum(1 / r["rank"] for r in hits) / len(answerable) if answerable else None,
        "unanswerable_questions": len(unanswerable),
    }
    if use_llm and unanswerable:
        ok = [r for r in unanswerable if r.get("llm_status") == "not_found"]
        summary["unanswerable_correctly_not_found"] = len(ok) / len(unanswerable)

    print(json.dumps(summary, indent=2))
    for r in rows:
        if r["answerable"]:
            verdict = f"HIT rank {r['rank']}" if r["hit"] else "MISS"
        else:
            verdict = "unanswerable"
        extra = f"  llm={r.get('llm_status')}" if use_llm else ""
        print(f"{r['id']}\t{verdict}\t{r['top_distance']:.3f}\t{r['question']}{extra}")

    name = f"results-c{settings.chunk_size}-o{settings.overlap_percent}-k{top_k}{'-llm' if use_llm else ''}.json"
    Path("eval").mkdir(exist_ok=True)
    Path("eval", name).write_text(json.dumps({"summary": summary, "rows": rows}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()