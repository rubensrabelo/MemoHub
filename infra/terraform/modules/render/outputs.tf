output "service_url" {
  value       = render_web_service.api.url
  description = "URL publica gerada pelo Render para a API"
}
