terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
    }
  }
}

provider "docker" {}

resource "docker_image" "flask_image" {
  name = "flask-cicd-app"
}

resource "docker_container" "flask_container" {
  name  = "flask_container"
  image = docker_image.flask_image.name

  ports {
    internal = 5000
    external = 5000
  }
}