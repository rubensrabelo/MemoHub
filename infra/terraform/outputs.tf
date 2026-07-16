output "render_backend_url" {
  value       = module.render_backend.service_url
  description = "A URL publica da API gerada pelo Render"
}

output "vercel_frontend_url" {
  value       = module.vercel_frontend.project_url
  description = "A URL publica do Front-end gerada pela Vercel"
}