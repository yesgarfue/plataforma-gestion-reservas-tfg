from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class MetricsReporter:
    def __init__(self, matrix_path: Path):
        self.matrix = yaml.safe_load(matrix_path.read_text(encoding="utf-8"))

    def summarize(self, target: str, results: list[dict[str, Any]]) -> dict[str, Any]:
        by_id = {row["test_id"]: row for row in results}
        executed = [r for r in results if r["status"] in {"passed", "failed"}]
        passed = [r for r in executed if r["status"] == "passed"]
        blocked = [r for r in results if r["status"] == "blocked"]
        skipped = [r for r in results if r["status"] == "skipped"]

        m7 = (len(passed) / len(executed) * 100) if executed else 0.0

        req_rows = []
        implemented = 0
        evaluable = 0
        for req_id, req in self.matrix["requirements"].items():
            test_ids = req["tests"]
            relevant = [by_id[t] for t in test_ids if t in by_id and by_id[t]["status"] != "skipped"]
            if not relevant:
                status = "no_evaluable"
            elif all(r["status"] == "passed" for r in relevant):
                status = "implemented"
                implemented += 1
                evaluable += 1
            elif any(r["status"] in {"passed", "failed"} for r in relevant):
                status = "partial_or_failed"
                evaluable += 1
            else:
                status = "blocked"
            req_rows.append(
                {
                    "requirement": req_id,
                    "title": req["title"],
                    "status": status,
                    "tests": test_ids,
                }
            )

        m6 = (implemented / evaluable * 100) if evaluable else 0.0
        operativity = self._operativity(by_id)

        return {
            "target": target,
            "counts": {
                "total": len(results),
                "executed": len(executed),
                "passed": len(passed),
                "failed": len([r for r in executed if r["status"] == "failed"]),
                "blocked": len(blocked),
                "skipped": len(skipped),
            },
            "metrics": {
                "M6_implementation_rate": round(m6, 2),
                "M7_pass_rate": round(m7, 2),
                "M_operatividad": operativity,
            },
            "requirements": req_rows,
            "results": results,
        }

    def _operativity(self, by_id: dict[str, dict[str, Any]]) -> int:
        startup_ids = ["T-CAT-01"]
        minimum_flow = ["T-AUTH-01", "T-CAT-01", "T-CAT-03", "T-CART-01", "T-RES-01"]
        if any(by_id.get(test_id, {}).get("status") == "passed" for test_id in minimum_flow):
            if all(by_id.get(test_id, {}).get("status") == "passed" for test_id in minimum_flow):
                return 2
            return 1
        if any(by_id.get(test_id, {}).get("status") == "passed" for test_id in startup_ids):
            return 1
        return 0
