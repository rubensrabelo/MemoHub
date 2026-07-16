output "connection_string" {
  value       = neon_project.db.connection_string
  description = "URL de conexao gerada pelo Neon para o banco de dados"
}
