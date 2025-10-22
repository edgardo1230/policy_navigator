# Use official Node.js image
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

RUN npm install typescript
# Build Next.js app
RUN npm run build

# Expose port 8080 for Cloud Run
ENV PORT=8080
EXPOSE 8080

CMD ["npm", "start"]