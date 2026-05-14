# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Cria o ambiente virtual e instala as dependências
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt


# ── Stage 2: Runtime ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# CORREÇÃO 1: Copia a pasta /venv do builder para o runtime
COPY --from=builder /venv /venv

# CORREÇÃO 2: Adiciona o /venv/bin ao PATH para o Docker achar o uvicorn
ENV PATH="/venv/bin:$PATH"

# CORREÇÃO 3: Descomenta para garantir que o código exista na imagem
COPY . .

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

#HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
#    CMD curl -f http://localhost:8000/health || exit 1

#CMD ["uvicorn app.main:app --reload"]
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
CMD ["sh", "-c", "alembic upgrade head && python -m app.core.seed && uvicorn app.main:app --host 0.0.0.0 --port 8000"]