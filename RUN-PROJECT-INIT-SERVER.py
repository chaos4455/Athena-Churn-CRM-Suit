"""
╔══════════════════════════════════════════════════════════════╗
║         Athena CRM — Churn Management Suite                  ║
║         Project Runner — O2 Data                             ║
╚══════════════════════════════════════════════════════════════╝
Uso: python RUN-PROJECT-INIT-SERVER.py
"""

import subprocess
import threading
import sys
import os
import time
import signal
import shutil
from datetime import datetime
from collections import deque

# ── deps ──────────────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.rule import Rule
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich import box
    from rich.align import Align
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich", "-q"])
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.rule import Rule
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich import box
    from rich.align import Align

try:
    import colorama
    colorama.init(autoreset=True)
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "colorama", "-q"])
    import colorama
    colorama.init(autoreset=True)

# ── config ────────────────────────────────────────────────────
console      = Console()
BACKEND_DIR  = os.path.join("athena-crm", "backend")
FRONTEND_DIR = os.path.join("athena-crm", "frontend")
API_PORT     = 8000
FE_PORT      = 3000
API_URL      = f"http://localhost:{API_PORT}"
FE_URL       = f"http://localhost:{FE_PORT}"

_stop     = threading.Event()
_api_proc = None
_fe_proc  = None
_lock     = threading.Lock()

# ── log helpers ───────────────────────────────────────────────
def ts():
    return datetime.now().strftime("%H:%M:%S")

def _color_api(line: str) -> Text:
    t = Text(overflow="fold")
    lo = line.lower()
    if any(x in lo for x in ["error","exception","traceback","critical"]):
        t.append(line, "bold red")
    elif any(x in lo for x in ["warning","warn"]):
        t.append(line, "yellow")
    elif any(x in lo for x in ["started","running","uvicorn","startup","ready","application startup"]):
        t.append(line, "bold green")
    elif any(x in lo for x in ['" 200',' 201',' 204']):
        t.append(line, "cyan")
    elif any(x in lo for x in ['" 404',' 422',' 400']):
        t.append(line, "orange3")
    elif any(x in lo for x in ['" 500',' 503']):
        t.append(line, "bold red")
    elif any(x in lo for x in ['"get ','\"post ','\"patch ','\"delete ']):
        t.append(line, "bright_magenta")
    else:
        t.append(line, "white")
    return t

def _color_fe(line: str) -> Text:
    t = Text(overflow="fold")
    lo = line.lower()
    if "error" in lo:
        t.append(line, "bold red")
    elif any(x in lo for x in ["serving","started","listening","127.0.0.1"]):
        t.append(line, "bold green")
    else:
        t.append(line, "bright_blue")
    return t

def _should_show(line: str) -> bool:
    """Return True only for lines worth showing in the console."""
    if not line.strip():
        return False
    lo = line.lower()
    # Drop raw SQL fragments and SQLAlchemy engine internals
    skip_fragments = [
        "sqlalchemy.engine",
        "begin (implicit)",
        "rollback",
        "commit",
        "from cards",
        "from sellers",
        "from clients",
        "from actions",
        "from histories",
        "where cards.",
        "where sellers.",
        "where clients.",
        "where actions.",
        "limit ? offset ?",
        "generated in",
        "cached since",
        "select cards.",
        "select sellers.",
        "select clients.",
        "select actions.",
        "select distinct",
        "cards.id as",
        "sellers.id as",
        "clients.id as",
        "actions.id as",
        # Drop the structured duplicate of uvicorn HTTP lines
        # (keep "INFO:     127.0.0.1" but drop "| INFO     | ... | GET /...")
        "| sqlalchemy",
    ]
    for frag in skip_fragments:
        if frag in lo:
            return False

    # Drop structured logger duplicates of HTTP lines
    # Pattern: "2026-04-18 01:43:23 | INFO     | uvicorn..."
    import re
    if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \|', line):
        return False

    return True

def _print_log_line(prefix: str, stamp: str, line: str, color_fn):
    """Print a single log line incrementally — no clear, no redraw."""
    if not _should_show(line):
        return
    colored = color_fn(line)
    out = Text(overflow="fold")
    out.append(f"{prefix} ", "dim")
    out.append(f"[{stamp}] ", "dim")
    out.append_text(colored)
    with _lock:
        console.print(out)

# ── stream readers ────────────────────────────────────────────
def _read(proc, prefix, color_fn):
    for stream in (proc.stdout, proc.stderr):
        threading.Thread(
            target=_drain, args=(stream, prefix, color_fn), daemon=True
        ).start()

def _drain(stream, prefix, color_fn):
    try:
        for raw in iter(stream.readline, b""):
            if _stop.is_set():
                break
            line = raw.decode("utf-8", errors="replace").rstrip()
            if line:
                _print_log_line(prefix, ts(), line, color_fn)
    except Exception:
        pass

# ── process launchers ─────────────────────────────────────────
def start_api():
    global _api_proc
    _print_log_line("�", ts(), "Iniciando FastAPI (uvicorn)...", _color_api)
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", str(API_PORT),
        "--log-level", "info",
    ]
    _api_proc = subprocess.Popen(
        cmd, cwd=BACKEND_DIR,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    _read(_api_proc, "🔥", _color_api)

def start_frontend():
    global _fe_proc
    _print_log_line("🌐", ts(), "Iniciando servidor frontend (http.server)...", _color_fe)
    cmd = [sys.executable, "-m", "http.server", str(FE_PORT)]
    _fe_proc = subprocess.Popen(
        cmd, cwd=FRONTEND_DIR,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    _read(_fe_proc, "🌐", _color_fe)

# ── static header printed once ────────────────────────────────
def _print_header():
    api_alive = _api_proc is not None and _api_proc.poll() is None
    fe_alive  = _fe_proc  is not None and _fe_proc.poll()  is None

    console.print(
        Panel(
            f"[bold bright_magenta]🧠  Athena CRM[/]  [dim]·  Churn Management Suite[/]  "
            f"[dim cyan]{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}[/]",
            border_style="bright_magenta",
            box=box.ROUNDED,
            padding=(0, 2),
        )
    )

    t = Table(box=box.SIMPLE_HEAVY, expand=True, header_style="bold bright_magenta")
    t.add_column("Serviço",  style="bold white",  min_width=26)
    t.add_column("Status",   justify="center",    min_width=12)
    t.add_column("URL",      style="cyan",        min_width=34)
    t.add_column("PID",      justify="right",     min_width=7)

    t.add_row(
        "🔥  FastAPI  (Backend)",
        Text("● ONLINE",  "bold green") if api_alive else Text("● OFFLINE","bold red"),
        f"{API_URL}/docs",
        str(_api_proc.pid) if _api_proc else "—",
    )
    t.add_row(
        "🌐  Frontend (HTTP Server)",
        Text("● ONLINE",  "bold green") if fe_alive  else Text("● OFFLINE","bold red"),
        FE_URL,
        str(_fe_proc.pid) if _fe_proc else "—",
    )
    t.add_row("📖  Swagger Docs", Text("● DOCS","bold blue"),  f"{API_URL}/docs",   "—")
    t.add_row("📘  ReDoc",        Text("● DOCS","bold blue"),  f"{API_URL}/redoc",  "—")
    t.add_row("💚  Health",       Text("● WATCH","bold cyan"), f"{API_URL}/health", "—")

    console.print(
        Panel(t, title="[bold white]⚙️  Serviços[/]",
              border_style="bright_magenta", box=box.ROUNDED)
    )

    console.print(
        Panel(
            "[bold red]  Ctrl+C  [/][dim] para encerrar todos os serviços   [/]"
            "[bold bright_magenta]  O2 Data  [/][dim]  Athena CRM v1.0.0  [/]",
            border_style="dim", box=box.ROUNDED, padding=(0, 2),
        )
    )

    console.print()
    console.print(Rule("[dim]Logs em tempo real — novas linhas aparecem abaixo[/]", style="dim"))
    console.print()

# ── splash ────────────────────────────────────────────────────
def splash():
    os.system("cls" if os.name == "nt" else "clear")
    console.print()
    console.print(Align.center(
        Panel.fit(
            "[bold bright_magenta]\n"
            "  ╔═══════════════════════════════════════════╗\n"
            "  ║   🧠   A T H E N A   C R M               ║\n"
            "  ║        Churn Management Suite             ║\n"
            "  ╚═══════════════════════════════════════════╝\n"
            "[/][dim]         Desenvolvido pela  [bold white]O2 Data[/][dim]          [/]",
            border_style="bright_magenta",
            box=box.DOUBLE,
            padding=(1, 4),
        )
    ))
    console.print()

    steps = [
        ("🔍", "Verificando estrutura do projeto..."),
        ("📦", "Checando dependências..."),
        ("🗄️ ", "Preparando banco de dados SQLite..."),
        ("🚀", "Iniciando servidor FastAPI..."),
        ("🌐", "Iniciando servidor Frontend..."),
        ("✅", "Tudo pronto!"),
    ]
    with Progress(
        SpinnerColumn(spinner_name="dots", style="bright_magenta"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(bar_width=28, style="bright_magenta", complete_style="green"),
        TimeElapsedColumn(),
        console=console, transient=True,
    ) as prog:
        task = prog.add_task("Inicializando...", total=len(steps))
        for icon, desc in steps:
            prog.update(task, description=f"{icon}  {desc}")
            time.sleep(0.4)
            prog.advance(task)

    console.print()

# ── shutdown ──────────────────────────────────────────────────
def shutdown(sig=None, frame=None):
    _stop.set()
    console.print()
    console.print(Rule("[bold red]⛔  Encerrando serviços...[/]", style="red"))
    for proc, name in [(_api_proc, "FastAPI"), (_fe_proc, "Frontend")]:
        if proc and proc.poll() is None:
            console.print(f"  [yellow]⏹  Parando {name} (PID {proc.pid})...[/]")
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
            console.print(f"  [green]✅  {name} encerrado.[/]")
    console.print()
    console.print(Align.center(
        Panel(
            "[bold bright_magenta]Athena CRM encerrado com sucesso.\n"
            "[dim]Até logo! — O2 Data[/]",
            border_style="bright_magenta", box=box.ROUNDED, padding=(1, 4),
        )
    ))
    console.print()
    sys.exit(0)

signal.signal(signal.SIGINT,  shutdown)
signal.signal(signal.SIGTERM, shutdown)

# ── main ──────────────────────────────────────────────────────
def main():
    splash()

    if not os.path.isdir(BACKEND_DIR):
        console.print(f"[bold red]❌  Backend não encontrado: {BACKEND_DIR}[/]")
        sys.exit(1)
    if not os.path.isdir(FRONTEND_DIR):
        console.print(f"[bold red]❌  Frontend não encontrado: {FRONTEND_DIR}[/]")
        sys.exit(1)

    start_api()
    time.sleep(1.0)
    start_frontend()
    time.sleep(0.6)

    # Print static header + status table once
    _print_header()

    # ── Keep alive — no redraw, just watch for API crash ──────
    while not _stop.is_set():
        time.sleep(2.0)

        # Auto-restart if API died
        if _api_proc and _api_proc.poll() is not None and not _stop.is_set():
            console.print()
            console.print(Rule("[bold yellow]⚠️  FastAPI caiu — reiniciando em 3s...[/]", style="yellow"))
            time.sleep(3)
            start_api()
            console.print(f"  [bold green]✅  FastAPI reiniciado (PID {_api_proc.pid})[/]")


if __name__ == "__main__":
    main()
