FROM node:22-slim AS base

WORKDIR /app

COPY package.json pnpm-lock.yaml* ./

RUN corepack enable && corepack prepare pnpm@latest --activate \
    && pnpm install --no-frozen-lockfile --ignore-scripts

COPY . .

RUN pnpm build

EXPOSE 3000

CMD ["pnpm", "start"]
