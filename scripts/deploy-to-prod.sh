#!/bin/bash

# Attempt to delete staging container service. If there is no such service, verify that the deployment should proceed
echo "Deleting staging service"
results=$(aws lightsail get-container-services --service-name evandukeenterprises-staging 2>&1)
if echo "$results" | grep -q "NotFoundException"; then
  echo "The staging container service is missing. Should the deployment to production continue? Y/N"
  read -r answer
  if [ "$answer" != "Y" ]; then
    echo "Aborting deployment"
    return 1
  fi
fi

# Push images to service
echo "Pushing most recent app image to AWS production service"
aws lightsail push-container-image --service-name evandukeenterprises --label evanduke --image evanduke:latest
echo "Pushing most recent server image to AWS"
aws lightsail push-container-image --service-name evandukeenterprises --label nginx --image nginx:latest

# Deploy to Lightsail
echo "Creating deployment"
aws lightsail create-container-service-deployment --service-name evandukeenterprises \
--containers '{
    "app": {
        "image": ":evandukeenterprises.evanduke.latest"
    },
    "ingress": {
        "image": ":evandukeenterprises.nginx.latest",
        "ports": {"80": "HTTP"}
    }
}' \
--public-endpoint '{"containerName": "ingress", "containerPort": 80}'
