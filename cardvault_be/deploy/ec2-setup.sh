#!/usr/bin/env bash
set -euo pipefail

echo "==> Installing Docker..."
if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sudo sh
  sudo usermod -aG docker "$USER"
  echo "Docker installed. You may need to log out and back in for group changes."
fi

echo "==> Enabling Docker on boot..."
sudo systemctl enable docker
sudo systemctl start docker

echo "==> Installing git and curl..."
sudo apt-get update
sudo apt-get install -y git curl

echo "==> Done."
echo ""
echo "Next steps:"
echo "  1. git clone <your-repo> && cd cardvault_be"
echo "  2. cp .env.example .env && nano .env"
echo "  3. docker compose up -d --build"
echo "  4. curl http://localhost:8000/health/ready"
