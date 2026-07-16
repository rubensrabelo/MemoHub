resource "render_web_service" "api" {
  name          = var.service_name
  plan          = "free"
  region        = "oregon"
  start_command = "gunicorn main:app --host 0.0.0.0 --port 8000"

  runtime_source = {
    native_runtime = {
      auto_deploy   = true
      branch        = "main"
      build_command = "pip install -r requirements.txt"
      repo_url      = "https://github.com{var.github_repo}"
      runtime       = "python"
    }
  }

  env_vars = {
    "DATABASE_URL" = {
      value = var.database_url
    }
    "PORT" = {
      value = "8000"
    }
  }
}
