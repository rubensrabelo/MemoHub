module "neon_db" {
  source       = "./modules/neon"
  project_name = "memohub-prod-db" # Alterado para forçar a criação de um novo banco limpo
}

module "render_backend" {
  source            = "./modules/render"
  service_name      = "my-python-backend-api"
  database_url      = module.neon_db.connection_string
  github_repo       = var.github_repository 
}

module "vercel_frontend" {
  source       = "./modules/vercel"
  project_name = "my-vue-frontend-web"
  github_repo  = var.github_repository
  backend_url  = module.render_backend.service_url
}
