"""Dashboard local con agregados. No consulta ni predice registros individuales."""
from pathlib import Path
import argparse
import functools
import http.server
import json

ROOT = Path(__file__).resolve().parents[1]


def export_dashboard():
    data = json.loads((ROOT / "results/dashboard_groups.json").read_text(encoding="utf-8"))
    template = (Path(__file__).parent / "template.html").read_text(encoding="utf-8")
    target = Path(__file__).parent / "index.html"
    target.write_text(template.replace("__AGGREGATE_DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")), encoding="utf-8")
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8501)
    parser.add_argument("--export", action="store_true", help="Exportar HTML sin iniciar servidor")
    args = parser.parse_args()
    target = export_dashboard()
    if args.export:
        print(target)
        return
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(target.parent))
    print(f"Dashboard: http://127.0.0.1:{args.port}/", flush=True)
    with http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
