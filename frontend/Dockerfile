FROM node:20-alpine
WORKDIR /app/frontend
COPY package.json ./
COPY package-lock.json ./
RUN rm -rf node_modules package-lock.json && npm install --legacy-peer-deps || npm install --force
COPY . .
CMD ["npx", "vite", "--host", "0.0.0.0", "--port", "3000"]
