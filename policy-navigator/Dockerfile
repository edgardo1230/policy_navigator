FROM python:3.11-slim
WORKDIR /code

# Create a non-root user
RUN adduser --disabled-password --gecos "" myuser

# Change ownership of /code to myuser
RUN chown -R myuser:myuser /code

# Switch to the non-root user
USER myuser

ENV PATH="/home/myuser/.local/bin:${PATH}"

# Install flit and use "--deps all" in command for all dependencies.
RUN pip install flit


# Install additional dependencies like reasoning-engines.
COPY deps/google_cloud_aiplatform-1.75.dev20241211+reasoning.engines-py2.py3-none-any.whl /code/
RUN pip install /code/google_cloud_aiplatform-1.75.dev20241211+reasoning.engines-py2.py3-none-any.whl

# Copy main app code and dependencies
COPY app/ /code/app/
COPY deps/ /code/deps/
COPY tests/ /code/tests/
COPY README.md /code/README.md
COPY pyproject.toml /code/pyproject.toml
COPY requirements.txt /code/requirements.txt

# Copy .env file for agent engine configuration
COPY app/.env /code/app/.env

# Set all required environment variables for agent engine
ENV GOOGLE_CLOUD_PROJECT=qwiklabs-gcp-01-f81085004973
ENV LOCATION=global
ENV COLLECTION_ID=default_collection
ENV POLICY_NAVIGATOR_COMPLIANCE_APP=policy-navigator_1761057129935
ENV POLICY_NAVIGATOR_CLINICAL_GUIDELINES_APP=policy-navigator_1761057129935
ENV POLICY_NAVIGATOR_HR_APP=policy-navigator_1761057129935

EXPOSE 8000 8501

# Entrypoint for ADK agent engine deployment
CMD ["uv", "run", "adk", "web", ".", "--port", "8501", "--reload_agents"]