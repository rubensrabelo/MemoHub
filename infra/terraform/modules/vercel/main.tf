terraform {
  required_providers {
    vercel = {
      source  = "vercel/vercel"
      version = "~> 1.0"
    }
  }
}

resource "vercel_project" "web" {
  name      = var.project_name
  framework = "vue"
  root_directory = "apps/frontend"

  git_repository = {
    type = "github"
    repo = var.github_repo
  }
}

resource "vercel_project_environment_variable" "api" {
  project_id = vercel_project.web.id
  key        = "VITE_API_URL"
  value      = "${var.backend_url}/api/v1"
  target     = ["production", "preview"]
  sensitive  = false
}
