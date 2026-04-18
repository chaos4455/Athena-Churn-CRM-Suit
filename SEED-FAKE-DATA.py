"""
╔══════════════════════════════════════════════════════════════════╗
║   Athena CRM — Seed de Dados Falsos                              ║
║   Gera: Vendedores · Clientes · Cards de Churn via ETL           ║
║   Faker PT-BR · 3 Filiais · 27 Estados                           ║
║   Desenvolvido pela O2 Data                                       ║
╚══════════════════════════════════════════════════════════════════╝

Uso:
    python SEED-FAKE-DATA.py
    python SEED-FAKE-DATA.py --cycle 2025-02
    python SEED-FAKE-DATA.py --api http://localhost:8000
    python SEED-FAKE-DATA.py --clients-per-state 12
"""

import argparse
import random
import sys
import time
from datetime import datetime, timedelta

import requests
from faker import Faker

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import (
        Progress, SpinnerColumn, TextColumn,
        BarColumn, MofNCompleteColumn, TimeElapsedColumn,
    )
    from rich.table import Table
    from rich import box
    from rich.rule import Rule
    from rich.align import Align
    from rich.text import Text
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "rich", "-q"])
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import (
        Progress, SpinnerColumn, TextColumn,
        BarColumn, MofNCompleteColumn, TimeElapsedColumn,
    )
    from rich.table import Table
    from rich import box
    from rich.rule import Rule
    from rich.align import Align
    from rich.text import Text

console = Console()
fake    = Faker("pt_BR")
Faker.seed(2025)
random.seed(2025)

# ─────────────────────────────────────────────────────────────────
# Dados mestres
# ─────────────────────────────────────────────────────────────────

BRANCHES = {
    "Filial Sul": ["RS", "SC", "PR"],
    "Filial Sudeste": ["SP", "RJ", "MG", "ES"],
    "Filial Norte/Nordeste/CO": [
        "AM", "PA", "RR", "AP", "AC", "RO", "TO",
        "MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA",
        "MT", "MS", "GO", "DF",
    ],
}

STATE_TO_BRANCH: dict[str, str] = {}
for _branch, _states in BRANCHES.items():
    for _st in _states:
        STATE_TO_BRANCH[_st] = _branch

ALL_STATES = list(STATE_TO_BRANCH.keys())

SEGMENTS = [
    "Varejo", "Atacado", "Indústria", "Serviços", "Agronegócio",
    "Tecnologia", "Saúde", "Educação", "Construção", "Logística",
]

PRODUCTS = [
    "Licença de Software", "Contrato de Manutenção", "Assinatura Anual",
    "Pacote Premium", "Serviço Gerenciado", "Suporte Técnico",
    "Consultoria", "Treinamento", "Integração API", "Módulo Adicional",
]

CHURN_REASONS = [
    "Sem compras nos últimos 90 dias",
    "Queda de 60%+ no volume de pedidos",
    "Contrato próximo do vencimento sem renovação",
    "Reclamações recorrentes não resolvidas",
    "Concorrente identificado na conta",
    "Redução de budget reportada pelo cliente",
    "Chave de contato trocada sem aviso",
    "NPS abaixo de 6 nos últimos 2 ciclos",
    "Inadimplência recorrente",
    "Downgrade de plano solicitado",
]

# ─────────────────────────────────────────────────────────────────
# Helpers de geração
# ─────────────────────────────────────────────────────────────────

def rnd_ltv(segment: str) -> float:
    ranges = {
        "Varejo": (5_000, 80_000), "Atacado": (20_000, 300_000),
        "Indústria": (50_000, 800_000), "Serviços": (8_000, 120_000),
        "Agronegócio": (30_000, 500_000), "Tecnologia": (15_000, 250_000),
        "Saúde": (10_000, 180_000), "Educação": (5_000, 60_000),
        "Construção": (40_000, 600_000), "Logística": (25_000, 350_000),
    }
    lo, hi = ranges.get(segment, (5_000, 100_000))
    return round(random.uniform(lo, hi), 2)


def rnd_ticket(ltv: float, months: int) -> float:
    base = ltv / max(months, 1)
    return round(base * random.uniform(0.6, 1.4), 2)


def calc_churn_score(last_days: int, ltv: float, avg_ticket: float) -> float:
    score = 0.0
    if last_days > 120:   score += 40
    elif last_days > 90:  score += 30
    elif last_days > 60:  score += 20
    elif last_days > 45:  score += 10
    if ltv < 10_000:      score += 15
    elif ltv < 30_000:    score += 8
    if avg_ticket < ltv * 0.03: score += 15
    score += random.uniform(-5, 15)
    return round(min(max(score, 0), 100), 1)


def calc_value_at_risk(ltv: float, avg_ticket: float, score: float) -> float:
    base = avg_ticket * random.uniform(2, 6)
    return round(base * (1 + score / 100 * 1.5), 2)


# ─────────────────────────────────────────────────────────────────
# API client — sem engolir erros
# ─────────────────────────────────────────────────────────────────

class AthenaAPI:
    def __init__(self, base: str):
        self.base = base.rstrip("/")
        self.v1   = self.base + "/api/v1"
        self.s    = requests.Session()
        self.s.headers.update({"Content-Type": "application/json"})

    def health(self) -> bool:
        try:
            r = self.s.get(f"{self.base}/health", timeout=5)
            return r.status_code == 200
        except Exception:
            return False

    def post(self, path: str, payload) -> dict:
        url = self.v1 + path
        r   = self.s.post(url, json=payload, timeout=30)
        if not r.ok:
            raise RuntimeError(f"POST {path} → {r.status_code}: {r.text[:200]}")
        return r.json()

    def get(self, path: str) -> list | dict:
        url = self.v1 + path
        r   = self.s.get(url, timeout=10)
        if not r.ok:
            raise RuntimeError(f"GET {path} → {r.status_code}: {r.text[:200]}")
        return r.json()

    def create_seller(self, payload: dict) -> dict:
        return self.post("/sellers/", payload)

    def get_sellers(self) -> list:
        return self.get("/sellers/")

    def ingest_clients(self, payload: list) -> dict:
        return self.post("/etl/clients", payload)

    def ingest_cards(self, payload: list) -> dict:
        return self.post("/etl/cards", payload)


# ─────────────────────────────────────────────────────────────────
# Geradores
# ─────────────────────────────────────────────────────────────────

def build_sellers() -> list[dict]:
    sellers = []
    # Admin geral
    sellers.append({
        "name": "Admin O2 Data", "email": "admin@o2data.com.br",
        "role": "admin", "branch": None, "state": None,
    })
    for branch, states in BRANCHES.items():
        # 1 gerente por filial
        sellers.append({
            "name":   fake.name(),
            "email":  fake.unique.email(),
            "role":   "manager",
            "branch": branch,
            "state":  states[0],
        })
        # 3 vendedores por filial
        for _ in range(3):
            sellers.append({
                "name":   fake.name(),
                "email":  fake.unique.email(),
                "role":   "seller",
                "branch": branch,
                "state":  random.choice(states),
            })
    return sellers


def build_clients(sellers_by_branch: dict[str, list], n_per_state: int) -> list[dict]:
    clients = []
    for state, branch in STATE_TO_BRANCH.items():
        branch_sellers = sellers_by_branch.get(branch, [])
        if not branch_sellers:
            continue
        for _ in range(n_per_state):
            segment      = random.choice(SEGMENTS)
            months       = random.randint(6, 60)
            last_days    = random.randint(15, 180)
            last_dt      = datetime.utcnow() - timedelta(days=last_days)
            ltv          = rnd_ltv(segment)
            avg_ticket   = rnd_ticket(ltv, months)
            score        = calc_churn_score(last_days, ltv, avg_ticket)
            seller       = random.choice(branch_sellers)
            clients.append({
                "external_id":        f"CLI-{state}-{fake.unique.numerify('######')}",
                "name":               fake.company(),
                "ltv":                ltv,
                "avg_ticket":         avg_ticket,
                "last_purchase_date": last_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                "churn_risk_score":   score,
                "seller_id":          seller["id"],
                "branch":             branch,
                "state":              state,
            })
    return clients


def build_cards(
    at_risk: list[dict],
    sellers_by_branch: dict[str, list],
    cycle_id: str,
) -> list[dict]:
    cards = []
    for client in at_risk:
        branch  = client["branch"]
        sellers = sellers_by_branch.get(branch, [])
        if not sellers:
            continue
        seller  = random.choice(sellers)
        reason  = random.choice(CHURN_REASONS)
        product = random.choice(PRODUCTS)
        var     = calc_value_at_risk(client["ltv"], client["avg_ticket"], client["churn_risk_score"])
        last_dt = datetime.fromisoformat(client["last_purchase_date"])
        days_ago = (datetime.utcnow() - last_dt).days
        cards.append({
            "client_external_id": client["external_id"],
            "seller_id":          seller["id"],
            "title":              f"Risco de Churn — {product}",
            "description": (
                f"Motivo: {reason}. "
                f"Score: {client['churn_risk_score']:.1f}/100. "
                f"Última compra há {days_ago} dias. "
                f"LTV: R$ {client['ltv']:,.2f}. "
                f"Ticket médio: R$ {client['avg_ticket']:,.2f}."
            ),
            "value_at_risk": var,
            "branch":        branch,
            "state":         client["state"],
            "cycle_id":      cycle_id,
        })
    return cards


# ─────────────────────────────────────────────────────────────────
# Splash
# ─────────────────────────────────────────────────────────────────

def splash():
    console.clear()
    console.print()
    console.print(Align.center(Panel.fit(
        "[bold bright_magenta]\n"
        "  ╔══════════════════════════════════════════════╗\n"
        "  ║   🧠   A T H E N A   C R M                  ║\n"
        "  ║        Seed de Dados Falsos                  ║\n"
        "  ║        Faker PT-BR · 3 Filiais · 27 UFs      ║\n"
        "  ╚══════════════════════════════════════════════╝\n"
        "[/][dim]           Desenvolvido pela  [bold white]O2 Data[/][dim]            [/]",
        border_style="bright_magenta", box=box.DOUBLE, padding=(1, 4),
    )))
    console.print()


# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api",   default="http://localhost:8000")
    parser.add_argument("--cycle", default=datetime.utcnow().strftime("%Y-%m"))
    parser.add_argument("--clients-per-state", type=int, default=8, dest="cps")
    args = parser.parse_args()

    splash()

    api = AthenaAPI(args.api)

    # ── Health ────────────────────────────────────────────────────
    console.print(f"  Conectando em [cyan]{args.api}[/] ...")
    if not api.health():
        console.print(f"\n  [bold red]❌  API offline em {args.api}[/]")
        console.print("  [dim]Suba o servidor primeiro:[/]  [cyan]python RUN-PROJECT-INIT-SERVER.py[/]\n")
        sys.exit(1)
    console.print("  [bold green]✅  API online[/]\n")

    # ════════════════════════════════════════════════════════════
    # PASSO 1 — Vendedores
    # ════════════════════════════════════════════════════════════
    console.print(Rule("[bold bright_magenta]1 / 3 — Vendedores[/]", style="bright_magenta"))
    sellers_payload = build_sellers()
    console.print(f"  Criando [bold]{len(sellers_payload)}[/] vendedores...")

    created_sellers: list[dict] = []
    errors_s = 0
    with Progress(
        SpinnerColumn(style="bright_magenta"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(style="bright_magenta", complete_style="green"),
        MofNCompleteColumn(), TimeElapsedColumn(),
        console=console,
    ) as prog:
        task = prog.add_task("Criando vendedores...", total=len(sellers_payload))
        for s in sellers_payload:
            try:
                result = api.create_seller(s)
                created_sellers.append(result)
            except RuntimeError as e:
                err_str = str(e)
                if "409" in err_str or "already" in err_str.lower() or "registered" in err_str.lower():
                    pass  # já existe — ok
                else:
                    errors_s += 1
                    console.print(f"  [red]ERR seller {s['email']}: {err_str[:80]}[/]")
            prog.advance(task)

    # Busca todos os sellers existentes
    try:
        all_sellers = api.get_sellers()
    except Exception as e:
        console.print(f"  [red]Erro ao buscar sellers: {e}[/]")
        all_sellers = created_sellers

    if not all_sellers:
        console.print("  [bold red]❌  Nenhum vendedor disponível. Abortando.[/]")
        sys.exit(1)

    # Organiza por filial
    sellers_by_branch: dict[str, list] = {b: [] for b in BRANCHES}
    for s in all_sellers:
        br = s.get("branch")
        if br and br in sellers_by_branch:
            sellers_by_branch[br].append(s)

    # Fallback: se alguma filial ficou sem vendedor, usa qualquer um
    any_seller = all_sellers[0]
    for br in sellers_by_branch:
        if not sellers_by_branch[br]:
            sellers_by_branch[br] = [any_seller]
            console.print(f"  [yellow]⚠  Filial '{br}' sem vendedor — usando fallback[/]")

    # Tabela resumo
    t = Table(box=box.SIMPLE_HEAVY, header_style="bold bright_magenta")
    t.add_column("Nome",   style="bold white", max_width=28)
    t.add_column("Role",   justify="center")
    t.add_column("Filial", style="cyan",       max_width=30)
    t.add_column("Estado", justify="center")
    for s in all_sellers:
        role_color = {"admin": "bold red", "manager": "bold yellow", "seller": "green"}.get(s.get("role", "seller"), "white")
        t.add_row(
            s["name"],
            f"[{role_color}]{s.get('role','—')}[/]",
            s.get("branch") or "—",
            s.get("state")  or "—",
        )
    console.print(t)
    console.print(f"  [bold green]✅  {len(all_sellers)} vendedores prontos[/]\n")

    # ════════════════════════════════════════════════════════════
    # PASSO 2 — Clientes
    # ════════════════════════════════════════════════════════════
    console.print(Rule("[bold bright_magenta]2 / 3 — Clientes[/]", style="bright_magenta"))
    clients_payload = build_clients(sellers_by_branch, args.cps)
    console.print(f"  Gerados [bold]{len(clients_payload)}[/] clientes ({args.cps}/estado × {len(ALL_STATES)} estados)\n")

    BATCH = 50
    batches = [clients_payload[i:i+BATCH] for i in range(0, len(clients_payload), BATCH)]
    total_c_created = total_c_updated = 0

    with Progress(
        SpinnerColumn(style="bright_magenta"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(style="bright_magenta", complete_style="green"),
        MofNCompleteColumn(), TimeElapsedColumn(),
        console=console,
    ) as prog:
        task = prog.add_task("Injetando clientes...", total=len(batches))
        for batch in batches:
            try:
                r = api.ingest_clients(batch)
                total_c_created += r.get("created", 0)
                total_c_updated += r.get("updated", 0)
                for err in r.get("errors", [])[:2]:
                    console.print(f"  [yellow]⚠  {err}[/]")
            except RuntimeError as e:
                console.print(f"  [red]❌  Lote clientes falhou: {e}[/]")
            prog.advance(task)

    at_risk = [c for c in clients_payload if c["churn_risk_score"] >= 60]

    # Tabela por filial
    t2 = Table(box=box.SIMPLE_HEAVY, header_style="bold bright_magenta")
    t2.add_column("Filial",    style="bold white")
    t2.add_column("Estados",   justify="center", style="cyan")
    t2.add_column("Clientes",  justify="right",  style="green")
    t2.add_column("Em Risco",  justify="right",  style="red")
    t2.add_column("Score Méd", justify="right",  style="yellow")
    for branch, states in BRANCHES.items():
        bc    = [c for c in clients_payload if c["branch"] == branch]
        risk  = [c for c in bc if c["churn_risk_score"] >= 60]
        avg_s = sum(c["churn_risk_score"] for c in bc) / len(bc) if bc else 0
        t2.add_row(branch, str(len(states)), str(len(bc)), str(len(risk)), f"{avg_s:.1f}")
    console.print(t2)
    console.print(f"  [bold green]✅  {total_c_created} criados · {total_c_updated} atualizados[/]")
    console.print(f"  [bold red]⚠   {len(at_risk)} clientes em zona de churn (score ≥ 60)[/]\n")

    # ════════════════════════════════════════════════════════════
    # PASSO 3 — Cards de Churn
    # ════════════════════════════════════════════════════════════
    console.print(Rule("[bold bright_magenta]3 / 3 — Cards de Churn[/]", style="bright_magenta"))
    console.print(f"  Ciclo: [bold cyan]{args.cycle}[/]")
    console.print(f"  Gerando cards para [bold red]{len(at_risk)}[/] clientes em risco...\n")

    cards_payload = build_cards(at_risk, sellers_by_branch, args.cycle)
    card_batches  = [cards_payload[i:i+BATCH] for i in range(0, len(cards_payload), BATCH)]
    cards_created = cards_archived = 0

    with Progress(
        SpinnerColumn(style="bright_magenta"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(style="bright_magenta", complete_style="green"),
        MofNCompleteColumn(), TimeElapsedColumn(),
        console=console,
    ) as prog:
        task = prog.add_task("Injetando cards...", total=max(len(card_batches), 1))
        for batch in card_batches:
            try:
                r = api.ingest_cards(batch)
                cards_created  += r.get("created",  0)
                cards_archived += r.get("archived", 0)
                for err in r.get("errors", [])[:2]:
                    console.print(f"  [yellow]⚠  {err}[/]")
            except RuntimeError as e:
                console.print(f"  [red]❌  Lote cards falhou: {e}[/]")
            prog.advance(task)

    # Tabela por filial
    t3 = Table(box=box.SIMPLE_HEAVY, header_style="bold bright_magenta")
    t3.add_column("Filial",         style="bold white")
    t3.add_column("Cards",          justify="right", style="green")
    t3.add_column("Valor em Risco", justify="right", style="red")
    t3.add_column("Score Médio",    justify="right", style="yellow")
    for branch in BRANCHES:
        bc   = [c for c in cards_payload if c["branch"] == branch]
        risk = [cl for cl in at_risk if cl["branch"] == branch]
        var  = sum(c["value_at_risk"] for c in bc)
        avg  = sum(cl["churn_risk_score"] for cl in risk) / len(risk) if risk else 0
        t3.add_row(branch, str(len(bc)), f"R$ {var:,.2f}", f"{avg:.1f}")
    console.print(t3)

    # ════════════════════════════════════════════════════════════
    # Resumo final
    # ════════════════════════════════════════════════════════════
    console.print()
    console.print(Rule("[bold green]✅  Seed concluído![/]", style="green"))
    console.print()

    summary = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    summary.add_column(style="dim")
    summary.add_column(style="bold white")
    summary.add_row("Ciclo injetado",    f"[cyan]{args.cycle}[/]")
    summary.add_row("Vendedores",        f"[green]{len(all_sellers)}[/]")
    summary.add_row("Clientes (total)",  f"[green]{len(clients_payload)}[/]")
    summary.add_row("Clientes em risco", f"[red]{len(at_risk)}[/]")
    summary.add_row("Cards criados",     f"[green]{cards_created}[/]")
    summary.add_row("Cards arquivados",  f"[yellow]{cards_archived}[/]")
    summary.add_row("Estados cobertos",  f"[cyan]{len(ALL_STATES)}[/]")
    summary.add_row("Filiais",           f"[cyan]{len(BRANCHES)}[/]")
    console.print(Align.center(summary))
    console.print()
    console.print(Align.center(
        f"[dim]Dashboard:[/] [bold cyan]http://localhost:3000/pages/dashboard.html[/]"
    ))
    console.print()


if __name__ == "__main__":
    main()
