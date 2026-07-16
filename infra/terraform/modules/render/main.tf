terraform {
  required_providers {
    render = {
      source  = "render-oss/render"
      version = "~> 1.8.0"
    }
  }
}

resource "render_web_service" "api" {
  name           = var.service_name
  plan           = "free"
  region         = "oregon"
  start_command  = "gunicorn main:app --host 0.0.0.0 --port 8000"
  root_directory = "apps/backend"

  runtime_source = {
    native_runtime = {
      auto_deploy   = true
      branch        = "main"
      build_command = "pip install -r requirements.txt"
      # AQUI ESTÁ A CORREÇÃO REAL DA STRING (COM / E COM $):
      repo_url      = "https://github.com/${var.github_repo}"
      runtime       = "python"
    }
  }

  env_vars = {
    "DATABASE_URL" = { value = var.database_url }
    "PORT"         = { value = "8000" }
  }
}
