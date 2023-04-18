#!/bin/bash

# Build images
echo "Building app image"
docker build . -t evanduke -f Dockerfile-app-prod
echo "Building nginx image"
docker build . -t nginx -f Dockerfile-nginx

# Tag images
echo "Tagging app image"
docker tag evanduke:latest evanduke:latest
echo "Tagging nginx image"
docker tag nginx:latest nginx:latest

staging="evandukeenterprises-staging"

# Create staging service (requires that the user logged into AWS CLI beforehand)
echo "Attempt to create staging container service"
results=$(aws lightsail create-container-service --service-name $staging --power nano --scale 1 2>&1)
if echo "$results" | grep -q "already exists"; then
  echo "Staging container service already exists."
elif echo "$results" | grep -q "https://$staging"; then
  echo "Staging container service created"
else
  echo "$results"
  exit 1
fi

# Push images to service
echo "Pushing app image to AWS"
aws lightsail push-container-image --service-name $staging --label evanduke --image evanduke:latest
echo "Pushing server image to AWS"
aws lightsail push-container-image --service-name $staging --label nginx --image nginx:latest

# Deploy to Lightsail
echo "Creating deployment"
aws lightsail create-container-service-deployment --service-name evandukeenterprises-staging \
--containers '{
    "app": {
        "image": ":evandukeenterprises-staging.evanduke.latest"
    },
    "ingress": {
        "image": ":evandukeenterprises-staging.nginx.latest",
        "ports": {"80": "HTTP"}
    }
}' \
--public-endpoint '{"containerName": "ingress", "containerPort": 80}'
