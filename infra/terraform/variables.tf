variable "neon_api_key" {
  type      = string
  sensitive = true
}

variable "render_api_key" {
  type      = string
  sensitive = true
}

variable "vercel_api_token" {
  type      = string
  sensitive = true
}

variable "github_repository" { type = string }

variable "render_owner_id" {
  type      = string
  sensitive = true
}

