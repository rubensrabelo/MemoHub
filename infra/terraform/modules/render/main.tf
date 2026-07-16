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
  root_directory = "apps/backend"

  runtime_source = {
    docker = {
      auto_deploy     = true
      branch          = "main"
      repo_url        = "https://github.com/${var.github_repo}"
      dockerfile_path = "Dockerfile"
    }
  }

  env_vars = {
    "DATABASE_URL" = { value = var.database_url }
    "PORT"         = { value = "8000" }
  }
}
