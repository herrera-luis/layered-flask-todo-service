
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.64, <= 3.65"
    }
  }
  backend "azurerm" {
    resource_group_name  = "corp-infrastructure-services"
    storage_account_name = "flaskservice"
    container_name       = "flask-service"
    key                  = "terraform.flask_service.tfstate"
  }
}

provider "azurerm" {
  features {}
  skip_provider_registration = true
}

locals {
  group_name   = "corp-infrastructure-services"
  network_name = "corp-infrastructure"
  location     = "eastus"
  environment  = "dev"
  service_name = "flask-service"
  database     = "todo"
}

data "terraform_remote_state" "network" {
  backend = "azurerm"
  config = {
    resource_group_name  = "corp-infrastructure"
    storage_account_name = "corpinfrastorage"
    container_name       = "terraform-states"
    key                  = "terraform.network.tfstate"
  }
}


resource "azurerm_service_plan" "this" {
  name                = "${local.service_name}-plan"
  location            = local.location
  resource_group_name = local.group_name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "todo_app" {
  name                      = "${local.service_name}-${local.environment}"
  location                  = local.location
  resource_group_name       = local.group_name
  service_plan_id           = azurerm_service_plan.this.id
  virtual_network_subnet_id = data.terraform_remote_state.network.outputs.network.dev_networking.public_subnet_id
  site_config {
    application_stack {
      python_version = "3.9"
    }
    app_command_line = "cd layered-flask-todo-service-0.0.3 && pip install -r requirements.txt && python run.py"
    always_on = false
  }
  

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE" = "https://github.com/herrera-luis/layered-flask-todo-service/archive/refs/tags/v0.0.3.zip"
    "DATABASE_URL"             = "postgresql://${var.db_username}:${var.db_password}@database/${local.database}"
    "HOST"                     = "0.0.0.0"
    "PORT"                     = "80"
    "LOG_DIR"                  = "/home"
  }

  depends_on = [
    azurerm_container_group.db_migrator
  ]

  tags = {
    service     = local.service_name
    environment = local.environment
  }

}

resource "azurerm_container_group" "db_migrator" {
  name                = "${local.service_name}-${local.environment}-migrations"
  location            = local.location
  resource_group_name = local.group_name
  ip_address_type     = "Private"
  subnet_ids          = [data.terraform_remote_state.network.outputs.network.dev_networking.private_subnet_id]
  os_type             = "Linux"

  container {
    name   = "flask-db-migrations"
    image  = "herreraluis/layered-flask-todo-service:latest"
    cpu    = "1"
    memory = "1.5"
    ports {
      port     = 5000
      protocol = "TCP"
    }

    commands = [
      "sh",
      "-c",
      "flask db upgrade"
    ]

    environment_variables = {
      DATABASE_URL = "postgresql://${var.db_username}:${var.db_password}@database/${local.database}"
      FLASK_APP    = "/usr/src/app/run-db-migrations.py" 
    }
  }

  tags = {
    service     = local.service_name
    environment = local.environment
  }
}