terraform {
  required_providers {
    neon = {
      source  = "kislerdm/neon"
      version = "~> 0.14.0"
    }
    render = {
      source  = "render-oss/render"
      version = "~> 1.8.0"
    }
    vercel = {
      source  = "vercel/vercel"
      version = "~> 5.4.1"
    }
  }
}

provider "neon" { api_key = var.neon_api_key }

provider "render" {
  api_key  = var.render_api_key
  owner_id = var.render_owner_id # Passado direto e reto sem blocos data
}

provider "vercel" { api_token = var.vercel_api_token }
