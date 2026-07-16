output "project_url" {
  value       = "https://${vercel_project.web.name}.vercel.app"
  description = "URL publica do Front-end gerada pela Vercel"
}
