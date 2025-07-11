# Use a more specific base image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.11-alpine

# Set working directory
WORKDIR /app

# Install system dependencies for Python packages and Node.js
RUN apk add --no-cache \
    nodejs \
    npm \
    build-base \
    libffi-dev \
    openssl-dev \
    python3-dev \
    gcc \
    musl-dev \
    linux-headers \
    nss \
    freetype \
    freetype-dev \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    cmake \
    pkgconfig \
    && rm -rf /var/cache/apk/*

# Copy package files first for better caching
COPY pyproject.toml uv.lock README.md ./
COPY package.json package-lock.json ./

# Install Python dependencies using uv
RUN uv sync

# Install Node.js dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Build Tailwind CSS
RUN npm run tailwind

# Create non-root user for security
RUN addgroup -g 1001 -S appuser && \
    adduser -u 1001 -S appuser -G appuser

# Change ownership of the app directory
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:5000/ || exit 1

# Run the application
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"] 