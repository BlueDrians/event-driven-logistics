variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "Deployment region"
  type        = string
  default     = "asia-southeast2"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "budget_amount" {
  description = "Monthly budget guardrail in billing currency"
  type        = number
  default     = 50
}

variable "billing_account" {
  description = "Billing account ID for budget creation"
  type        = string
  default     = ""
}
