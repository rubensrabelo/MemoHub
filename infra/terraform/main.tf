module "neon_db" {
  source       = "./modules/neon"
  project_name = "prod-database-python"
}

module "render_backend" {
  source       = "./modules/render"
  service_name = "my-python-backend-api"
  github_repo  = var.github_repository
  database_url = module.neon_db.connection_string
}

module "vercel_frontend" {
  source       = "./modules/vercel"
  project_name = "my-vite-frontend-web"
  github_repo  = var.github_repository
  backend_url  = module.render_backend.service_url
}
