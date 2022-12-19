#!/bin/bash

helm install akri akri-helm-charts/akri   \
    $AKRI_HELM_CRICTL_CONFIGURATION \
    -n face-recogn \
    --create-namespace \
    --set udev.discovery.enabled=true \
    --set udev.configuration.enabled=true \
    --set udev.configuration.name=akri-udev-video \
    --set udev.configuration.discoveryDetails.udevRules[0]='KERNEL=="video[0-9]"' \
    --set udev.configuration.brokerPod.image.repository="phajder/udev-k8s-video-broker" \
    --set udev.configuration.brokerPod.image.tag="latest" \
    --set udev.configuration.brokerProperties.FORMAT='MJPG' \
    --set udev.configuration.brokerProperties.RESOLUTION_WIDTH=512 \
    --set udev.configuration.brokerProperties.RESOLUTION_HEIGHT=512 \
    --set udev.configuration.brokerProperties.FRAMES_PER_SECOND=90

kubectl config set-context --current --namespace=face-recogn