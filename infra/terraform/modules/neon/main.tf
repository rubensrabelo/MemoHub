terraform {
  required_providers {
    neon = {
      source  = "kislerdm/neon"
      version = "~> 0.14.0"
    }
  }
}

resource "neon_project" "db" {
  name      = var.project_name
  history_retention_seconds = 21600
}
