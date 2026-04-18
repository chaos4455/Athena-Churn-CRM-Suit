"""
╔════════════════════════════════════════════════════════════════════════╗
║   Athena CRM — INJETOR B2B ENTERPRISE (Distribuição Perfeita)          ║
║   100% Faker | Push Direto | Narrativas em Timeline | Round-Robin      ║
╚════════════════════════════════════════════════════════════════════════╝
"""

import argparse
import random
import sys
import time
import itertools
from datetime import datetime, timedelta

import requests
from faker import Faker

try:
    from rich.console import Console
    from rich.panel import Panel  # <--- CORRIGIDO AQUI
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.table import Table
    from rich import box
    from rich.rule import Rule
    from rich.align import Align
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "rich", "-q"])
    from rich.console import Console
    from rich.panel import Panel  # <--- CORRIGIDO AQUI
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.table import Table
    from rich import box
    from rich.rule import Rule
    from rich.align import Align

console = Console()
fake = Faker("pt_BR")
run_hash = int(time.time() * 1000)

# ─────────────────────────────────────────────────────────────────
# Dicionários de Contexto B2B Avançado
# ─────────────────────────────────────────────────────────────────

BRANCHES = {
    "Filial Sul": ["RS", "SC", "PR"],
    "Filial Sudeste": ["SP", "RJ", "MG", "ES"],
    "Filial Norte/Nordeste/CO": ["AM", "PA", "CE", "BA", "MT", "GO", "DF", "PE", "MA"]
}
STATE_TO_BRANCH = {st: br for br, states in BRANCHES.items() for st in states}

INDUSTRY_DATA = {
    "Varejo": {"prod": ["ERP Omnichannel", "Módulo PDV Smart"], "cargo": "Diretor de Operações"},
    "Indústria": {"prod": ["ERP Industrial 4.0", "MES Chão de Fábrica"], "cargo": "Gerente de Planta"},
    "Tecnologia": {"prod": ["Infra Cloud Dedicada", "CyberSecurity API"], "cargo": "CTO"},
    "Saúde": {"prod": ["Prontuário Eletrônico", "Gestão de Leitos AI"], "cargo": "Diretor Médico"},
    "Agronegócio": {"prod": ["Rastreabilidade de Safra", "Telemetria de Frota"], "cargo": "Gestor de Agronegócio"},
    "Finanças": {"prod": ["Core Banking SaaS", "Motor Anti-Fraude"], "cargo": "CFO"}
}

COMPETITORS = ["Salesforce", "Totvs", "SAP", "Oracle", "Zendesk", "HubSpot", "Senior Sistemas"]

# ─────────────────────────────────────────────────────────────────
# Motor de Narrativas (Timeline de CRM)
# ─────────────────────────────────────────────────────────────────

def generate_timeline(product, cargo_cliente, seller_name, days_ago):
    """Cria uma linha do tempo de eventos do CRM para parecer que a conta vem se deteriorando"""
    concorrente = random.choice(COMPETITORS)
    
    d_minus_45 = (datetime.utcnow() - timedelta(days=days_ago + 30)).strftime("%d/%m/%Y")
    d_minus_15 = (datetime.utcnow() - timedelta(days=days_ago + 5)).strftime("%d/%m/%Y")
    d_today = datetime.utcnow().strftime("%d/%m/%Y")

    cenarios = [
        # Cenário 1: Concorrência agressiva e perda de sponsor
        f"📅 {d_minus_45} | 🤖 [SISTEMA] Alerta: Uso do módulo de {product} caiu 45%.\n"
        f"📅 {d_minus_15} | 📞 [CSM LOG] Reunião de QBR cancelada pelo cliente. O antigo {cargo_cliente} foi desligado.\n"
        f"📅 {d_today}  | 👤 [{seller_name.upper()}] Consegui contato com a nova gestão. Eles trouxeram uma consultoria da {concorrente} e estão avaliando quebra de contrato. Preciso de autorização para oferecer 30% de desconto na renovação.",
        
        # Cenário 2: Problemas técnicos crônicos
        f"📅 {d_minus_45} | 🚨 [ZENDESK API] Ticket P1 Aberto: 'Falha crítica na integração do {product}'.\n"
        f"📅 {d_minus_15} | 🚨 [ZENDESK API] SLA de resposta violado. Cliente ameaçou PROCON e setor jurídico.\n"
        f"📅 {d_today}  | 👤 [{seller_name.upper()}] O {cargo_cliente} me ligou furioso hoje cedo. Diz que a operação parou por 4 horas semana passada. Risco de churn financeiro IMINENTE.",
        
        # Cenário 3: Inadimplência e Redução de Budget
        f"📅 {d_minus_45} | 💰 [ERP AUTO] Fatura #9923 vencida. Régua de cobrança iniciada.\n"
        f"📅 {d_minus_15} | ✉️ [MARKETING] Cliente marcou e-mail de 'Novidades do {product}' como Spam.\n"
        f"📅 {d_today}  | 👤 [{seller_name.upper()}] Financeiro deles travou os pagamentos alegando corte de verba. O {cargo_cliente} pediu downgrade drástico para a versão mais básica, ou vão migrar para a {concorrente}."
    ]
    return random.choice(cenarios)


# ─────────────────────────────────────────────────────────────────
# API Client (APENAS POST)
# ─────────────────────────────────────────────────────────────────

class AthenaAPI:
    def __init__(self, base: str):
        self.v1 = base.rstrip("/") + "/api/v1"
        self.s = requests.Session()

    def post(self, path: str, payload) -> dict:
        url = self.v1 + path
        r = self.s.post(url, json=payload, timeout=30)
        if not r.ok:
            raise RuntimeError(f"Erro POST {path}: {r.status_code} - {r.text[:150]}")
        return r.json()

# ─────────────────────────────────────────────────────────────────
# Execução Principal
# ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", default="http://localhost:8000")
    parser.add_argument("--cycle", default=datetime.utcnow().strftime("%Y-%m"))
    parser.add_argument("--cards-per-state", type=int, default=12, dest="cps") 
    args = parser.parse_args()

    api = AthenaAPI(args.api)
    console.clear()
    console.print(Align.center(
        Panel.fit("[bold bright_cyan]🧠 ATHENA CRM: INJETOR DE DADOS ENTERPRISE[/]\n"
                  "[dim]Distribuição Round-Robin • Linha do Tempo B2B • Force Push[/]", 
                  border_style="bright_cyan")
    ))
    console.print()

    # ==========================================
    # 1. CRIAR VENDEDORES
    # ==========================================
    console.print("[bold yellow]1. Recrutando Vendedores...[/]")
    sellers_payload = []
    for branch, states in BRANCHES.items():
        for _ in range(4): # 4 vendedores por filial = 12 no total
            uid = random.randint(1000, 99999)
            sellers_payload.append({
                "name": f"{fake.first_name()} {fake.last_name()}",
                "email": f"exec_{uid}_{run_hash}@crmo2.com",
                "role": "seller",
                "branch": branch,
                "state": random.choice(states)
            })

    created_sellers = []
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as prog:
        t1 = prog.add_task("Enviando POST de Vendedores...", total=len(sellers_payload))
        for s in sellers_payload:
            try:
                res = api.post("/sellers/", s)
                created_sellers.append(res)
            except Exception as e:
                console.print(f"[red]Erro Vendedor:[/] {e}")
            prog.advance(t1)

    if not created_sellers:
        console.print("[bold red]Nenhum vendedor criado. Abortando.[/]"); sys.exit(1)

    # Organizar vendedores por filial para o Round-Robin
    sellers_by_branch = {b: [] for b in BRANCHES}
    for s in created_sellers:
        if s.get("branch") in sellers_by_branch:
            sellers_by_branch[s["branch"]].append(s)

    # Criar Iteradores Infinitos (Round-Robin) para distribuir clientes de forma 100% igual
    robin_iterators = {br: itertools.cycle(sells) for br, sells in sellers_by_branch.items() if sells}

    # Estrutura para contar quem recebeu o que (prova real no final)
    distribution_tracker = {s["id"]: {"name": s["name"], "branch": s["branch"], "cards": 0} for s in created_sellers}

    # ==========================================
    # 2. GERAR CLIENTES (DISTRIBUIÇÃO PERFEITA)
    # ==========================================
    console.print("\n[bold yellow]2. Forjando Contas Enterprise e Atribuindo Vendedores...[/]")
    clients_payload = []
    
    for state, branch in STATE_TO_BRANCH.items():
        if branch not in robin_iterators: continue
        
        for _ in range(args.cps):
            # PEGA O PRÓXIMO VENDEDOR DA FILIAL (Garante distribuição igualitária)
            assigned_seller = next(robin_iterators[branch])
            
            segment = random.choice(list(INDUSTRY_DATA.keys()))
            mrr = random.uniform(2_500, 15_000)
            avg_ticket = round(mrr, 2)
            ltv = round(mrr * random.randint(12, 48), 2)
            score = round(random.uniform(72.0, 99.0), 1)
            
            ext_id = f"CLI-{state}-{random.randint(1000,9999)}-{run_hash}"
            company = f"{fake.company()} {random.choice(['S/A', 'Group', 'Logística', 'Tecnologia'])}"
            
            clients_payload.append({
                "external_id": ext_id,
                "name": company,
                "ltv": ltv,
                "avg_ticket": avg_ticket,
                "last_purchase_date": (datetime.utcnow() - timedelta(days=random.randint(45, 120))).strftime("%Y-%m-%dT%H:%M:%S"),
                "churn_risk_score": score,
                "seller_id": assigned_seller["id"], # ATRIBUIÇÃO AQUI
                "branch": branch,
                "state": state,
                "_segment": segment,
                "_seller_name": assigned_seller["name"]
            })

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as prog:
        t2 = prog.add_task("Enviando POST de Clientes ETL...", total=1)
        try: api.post("/etl/clients", clients_payload)
        except Exception as e: console.print(f"[red]Erro Clientes:[/] {e}")
        prog.advance(t2)

    # ==========================================
    # 3. GERAR CARDS (TIMELINE RICA)
    # ==========================================
    console.print("\n[bold yellow]3. Escrevendo Histórico de Churn e Injetando Cards...[/]")
    cards_payload = []
    
    for client in clients_payload:
        segment = client.pop("_segment")
        seller_name = client.pop("_seller_name")
        
        prod_data = INDUSTRY_DATA[segment]
        product = random.choice(prod_data["prod"])
        cargo = prod_data["cargo"]
        
        var = round(client["avg_ticket"] * random.uniform(2, 6), 2)
        timeline = generate_timeline(product, cargo, seller_name, days_ago=random.randint(2, 10))
        
        full_desc = (
            f"🎯 PRODUTO EM RISCO: {product} (Nicho: {segment})\n"
            f"💵 MRR AFETADO: R$ {client['avg_ticket']:,.2f}\n"
            f"📊 CHURN SCORE: {client['churn_risk_score']:.1f}/100\n"
            f"{'='*60}\n"
            f"📋 TIMELINE DO CRM:\n\n{timeline}"
        )

        cards_payload.append({
            "client_external_id": client["external_id"],
            "seller_id": client["seller_id"], # CARD AMARRADO AO VENDEDOR CORRETO
            "title": f"Risco Crítico: {client['name'].split(' ')[0]}",
            "description": full_desc,
            "value_at_risk": var,
            "branch": client["branch"],
            "state": client["state"],
            "cycle_id": args.cycle,
        })
        
        # Computa no tracker para a prova real
        distribution_tracker[client["seller_id"]]["cards"] += 1

    batches = [cards_payload[i:i+50] for i in range(0, len(cards_payload), 50)]
    cards_sucesso = 0
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), console=console) as prog:
        t3 = prog.add_task(f"Injetando {len(cards_payload)} Cards via ETL...", total=len(batches))
        for batch in batches:
            try:
                r = api.post("/etl/cards", batch)
                cards_sucesso += r.get("created", len(batch))
            except Exception as e:
                console.print(f"[red]Erro Cards:[/] {e}")
            prog.advance(t3)

    # ==========================================
    # RESUMO E PROVA DE DISTRIBUIÇÃO
    # ==========================================
    console.print()
    console.print(Rule(f"[bold green]✅ {cards_sucesso} CARDS CRIADOS COM SUCESSO![/]", style="green"))
    console.print("\n[bold cyan]📊 PROVA DE DISTRIBUIÇÃO ROUND-ROBIN (Cards por Vendedor)[/]")
    
    t = Table(box=box.SIMPLE_HEAVY, header_style="bold bright_cyan")
    t.add_column("Vendedor / Executivo")
    t.add_column("Filial")
    t.add_column("Cards Atribuídos", justify="right", style="bold green")
    
    for s_id, stats in distribution_tracker.items():
        t.add_row(stats["name"], stats["branch"], str(stats["cards"]))
        
    console.print(Align.center(t))
    console.print()
    console.print(Align.center("[dim]Confira o painel para ler as Timelines completas nos Cards:[/]\n[bold white]http://localhost:3000/pages/dashboard.html[/]"))

if __name__ == "__main__":
    main()