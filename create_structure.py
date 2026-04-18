"""
Athena CRM - Churn Management Suite
Script para criar a estrutura completa do projeto (arquivos vazios)
Desenvolvido pela O2 Data
"""

import os

# Estrutura completa do projeto
STRUCTURE = {
    "athena-crm": {
        # ── Backend ──────────────────────────────────────────────
        "backend": {
            "app": {
                # Domain Layer
                "domain": {
                    "entities": {
                        "__init__.py": "",
                        "client.py": "",
                        "card.py": "",
                        "action.py": "",
                        "history.py": "",
                        "seller.py": "",
                    },
                    "value_objects": {
                        "__init__.py": "",
                        "churn_status.py": "",
                        "card_stage.py": "",
                        "action_type.py": "",
                    },
                    "repositories": {
                        "__init__.py": "",
                        "client_repository.py": "",
                        "card_repository.py": "",
                        "action_repository.py": "",
                        "history_repository.py": "",
                        "seller_repository.py": "",
                    },
                    "services": {
                        "__init__.py": "",
                        "churn_service.py": "",
                        "dashboard_service.py": "",
                        "performance_service.py": "",
                    },
                    "__init__.py": "",
                },
                # Application Layer
                "application": {
                    "use_cases": {
                        "cards": {
                            "__init__.py": "",
                            "create_card.py": "",
                            "update_card.py": "",
                            "delete_card.py": "",
                            "list_cards.py": "",
                            "get_card.py": "",
                            "move_card_stage.py": "",
                        },
                        "clients": {
                            "__init__.py": "",
                            "list_clients.py": "",
                            "get_client.py": "",
                            "search_clients.py": "",
                            "get_client_history.py": "",
                        },
                        "actions": {
                            "__init__.py": "",
                            "register_action.py": "",
                            "list_actions.py": "",
                            "update_action.py": "",
                        },
                        "dashboard": {
                            "__init__.py": "",
                            "get_dashboard_indicators.py": "",
                            "get_performance_metrics.py": "",
                        },
                        "etl": {
                            "__init__.py": "",
                            "ingest_clients.py": "",
                            "ingest_cards.py": "",
                        },
                        "__init__.py": "",
                    },
                    "dtos": {
                        "__init__.py": "",
                        "card_dto.py": "",
                        "client_dto.py": "",
                        "action_dto.py": "",
                        "dashboard_dto.py": "",
                        "etl_dto.py": "",
                    },
                    "__init__.py": "",
                },
                # Infrastructure Layer
                "infrastructure": {
                    "database": {
                        "__init__.py": "",
                        "connection.py": "",
                        "models.py": "",
                        "migrations": {
                            "__init__.py": "",
                            "001_initial.py": "",
                        },
                    },
                    "repositories": {
                        "__init__.py": "",
                        "sqlite_client_repository.py": "",
                        "sqlite_card_repository.py": "",
                        "sqlite_action_repository.py": "",
                        "sqlite_history_repository.py": "",
                        "sqlite_seller_repository.py": "",
                    },
                    "security": {
                        "__init__.py": "",
                        "jwt_handler.py": "",
                        "dependencies.py": "",
                    },
                    "__init__.py": "",
                },
                # Interface Layer (API)
                "api": {
                    "v1": {
                        "routers": {
                            "__init__.py": "",
                            "cards.py": "",
                            "clients.py": "",
                            "actions.py": "",
                            "dashboard.py": "",
                            "performance.py": "",
                            "etl.py": "",
                            "sellers.py": "",
                        },
                        "schemas": {
                            "__init__.py": "",
                            "card_schema.py": "",
                            "client_schema.py": "",
                            "action_schema.py": "",
                            "dashboard_schema.py": "",
                            "etl_schema.py": "",
                            "seller_schema.py": "",
                            "common.py": "",
                        },
                        "__init__.py": "",
                    },
                    "__init__.py": "",
                },
                # Core / Config
                "core": {
                    "__init__.py": "",
                    "config.py": "",
                    "exceptions.py": "",
                    "logging.py": "",
                },
                "__init__.py": "",
                "main.py": "",
            },
            # Tests
            "tests": {
                "__init__.py": "",
                "unit": {
                    "__init__.py": "",
                    "domain": {
                        "__init__.py": "",
                        "test_card.py": "",
                        "test_client.py": "",
                        "test_churn_service.py": "",
                    },
                    "application": {
                        "__init__.py": "",
                        "test_create_card.py": "",
                        "test_dashboard.py": "",
                    },
                },
                "integration": {
                    "__init__.py": "",
                    "test_cards_api.py": "",
                    "test_clients_api.py": "",
                    "test_etl_api.py": "",
                },
                "conftest.py": "",
            },
            "requirements.txt": "",
            "requirements-dev.txt": "",
            ".env.example": "",
            "Makefile": "",
            "pytest.ini": "",
        },

        # ── Frontend ─────────────────────────────────────────────
        "frontend": {
            "assets": {
                "css": {
                    "variables.css": "",
                    "reset.css": "",
                    "components.css": "",
                    "layout.css": "",
                    "dark-theme.css": "",
                    "animations.css": "",
                    "responsive.css": "",
                },
                "js": {
                    "core": {
                        "api.js": "",
                        "router.js": "",
                        "state.js": "",
                        "theme.js": "",
                        "utils.js": "",
                        "auth.js": "",
                    },
                    "components": {
                        "sidebar.js": "",
                        "header.js": "",
                        "footer.js": "",
                        "modal.js": "",
                        "toast.js": "",
                        "kanban.js": "",
                        "card.js": "",
                        "charts.js": "",
                        "table.js": "",
                        "search.js": "",
                    },
                    "pages": {
                        "dashboard.js": "",
                        "performance.js": "",
                        "actions.js": "",
                        "clients.js": "",
                        "client-detail.js": "",
                    },
                    "app.js": "",
                },
                "icons": {},
                "fonts": {},
            },
            "pages": {
                "dashboard.html": "",
                "performance.html": "",
                "actions.html": "",
                "clients.html": "",
                "client-detail.html": "",
            },
            "index.html": "",
        },

        # ── Docs ─────────────────────────────────────────────────
        "docs": {
            "architecture.md": "",
            "api-guide.md": "",
            "etl-guide.md": "",
            "design-system.md": "",
        },

        # ── Root files ───────────────────────────────────────────
        ".gitignore": "",
        "README.md": "",
        "docker-compose.yml": "",
    }
}


def create_structure(base_path: str, structure: dict):
    """Cria recursivamente a estrutura de pastas e arquivos."""
    for name, content in structure.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            # É uma pasta
            os.makedirs(path, exist_ok=True)
            print(f"  📁  {path}")
            create_structure(path, content)
        else:
            # É um arquivo
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  📄  {path}")


def main():
    print("=" * 60)
    print("  Athena CRM - Churn Management Suite")
    print("  Criando estrutura do projeto...")
    print("  Desenvolvido pela O2 Data")
    print("=" * 60)

    base = "."
    create_structure(base, STRUCTURE)

    print()
    print("=" * 60)
    print("  ✅  Estrutura criada com sucesso!")
    print("=" * 60)
    print()
    print("  Próximos passos:")
    print("  1. cd athena-crm/backend")
    print("  2. pip install -r requirements.txt")
    print("  3. uvicorn app.main:app --reload")
    print()


if __name__ == "__main__":
    main()
