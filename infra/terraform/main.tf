module "neon_db" {
  source       = "./modules/neon"
  project_name = "memohub-prod-db"
}

module "render_backend" {
  source            = "./modules/render"
  service_name      = "my-python-backend-api"
  github_repo       = var.github_repository
  database_url      = split("?", replace(module.neon_db.connection_string, "postgres://", "postgresql+asyncpg://"))[0]
}

module "vercel_frontend" {
  source       = "./modules/vercel"
  project_name = "my-vue-frontend-web"
  github_repo  = var.github_repository
  backend_url  = module.render_backend.service_url
}
