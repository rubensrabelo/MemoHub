resource "neon_project" "db" {
  name      = var.project_name
  region_id = "aws-us-east-1"
}
