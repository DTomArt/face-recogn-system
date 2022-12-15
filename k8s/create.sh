#!/bin/bash

# minikube mount /home/tartecki/face-recogn-system:/home/tartecki/face-recogn-system

# kubectl apply -f namespace.yaml
# kubectl config set-context --current --namespace=face-recogn

cd volumes

kubectl apply -f data-volume.yaml
kubectl apply -f data-claim.yaml

kubectl apply -f model-volume.yaml
kubectl apply -f model-claim.yaml

cd -

kubectl apply -f webapp-deployment.yaml
kubectl apply -f frontend-deployment.yaml
# kubectl apply -f learning-deployment.yaml

# helm install akri akri-helm-charts/akri   \
#     $AKRI_HELM_CRICTL_CONFIGURATION \
#     --set udev.discovery.enabled=true \
#     --set udev.configuration.enabled=true \
#     --set udev.configuration.name=akri-udev-video \
#     --set udev.configuration.discoveryDetails.udevRules[0]='KERNEL=="video[0-9]"' \
#     --set udev.configuration.brokerPod.image.repository="phajder/udev-k8s-video-broker" \
#     --set udev.configuration.brokerPod.image.tag="latest" \
#     --set udev.configuration.brokerProperties.FORMAT='MJPG' \
#     --set udev.configuration.brokerProperties.RESOLUTION_WIDTH=512 \
#     --set udev.configuration.brokerProperties.RESOLUTION_HEIGHT=512 \
#     --set udev.configuration.brokerProperties.FRAMES_PER_SECOND=90
