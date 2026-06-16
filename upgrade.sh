#!/usr/bin/env sh
set -e

# ── cores ──────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()   { printf "${GREEN}[ok]${NC}  %s\n" "$1"; }
info() { printf "${YELLOW}[..]${NC}  %s\n" "$1"; }
fail() { printf "${RED}[err]${NC} %s\n" "$1" >&2; exit 1; }

# ── pré-requisitos ─────────────────────────────────────────────────────────
command -v git    >/dev/null 2>&1 || fail "git não encontrado"
command -v docker >/dev/null 2>&1 || fail "docker não encontrado"
docker compose version >/dev/null 2>&1 || fail "docker compose (plugin v2) não encontrado"

# ── diretório do script ────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

[ -f ".env" ] || fail "arquivo .env não encontrado em $SCRIPT_DIR"

# ── git pull ───────────────────────────────────────────────────────────────
info "Buscando atualizações do repositório..."
git fetch --quiet
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse '@{u}' 2>/dev/null || echo "")

if [ -z "$REMOTE" ]; then
    info "Branch sem upstream configurado — pulando git pull"
elif [ "$LOCAL" = "$REMOTE" ]; then
    ok "Repositório já está atualizado ($(git rev-parse --short HEAD))"
else
    git pull --ff-only || fail "git pull falhou — resolva conflitos manualmente"
    ok "Código atualizado para $(git rev-parse --short HEAD)"
fi

# ── rebuild da imagem ──────────────────────────────────────────────────────
info "Reconstruindo imagem Docker..."
docker compose build --no-cache --quiet
ok "Imagem reconstruída"

# ── restart do serviço ─────────────────────────────────────────────────────
info "Reiniciando serviço (migrate + collectstatic + gunicorn)..."
docker compose up -d --remove-orphans
ok "Container iniciado"

# ── aguarda healthcheck básico ─────────────────────────────────────────────
info "Aguardando aplicação subir (máx. 30s)..."
i=0
while [ $i -lt 15 ]; do
    if docker compose ps | grep -q "Up"; then
        ok "Aplicação no ar"
        break
    fi
    i=$((i + 1))
    sleep 2
done

if ! docker compose ps | grep -q "Up"; then
    fail "Container não subiu em 30s — veja: docker compose logs"
fi

# ── limpeza de imagens antigas ─────────────────────────────────────────────
info "Removendo imagens Docker sem uso..."
docker image prune -f --quiet
ok "Imagens órfãs removidas"

# ── resumo ─────────────────────────────────────────────────────────────────
printf "\n"
ok "Upgrade concluído — $(date '+%d/%m/%Y %H:%M:%S')"
docker compose ps
