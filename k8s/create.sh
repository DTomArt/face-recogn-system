#!/bin/bash

# minikube mount /home/tartecki/face-recogn-system:/home/tartecki/face-recogn-system

# kubectl apply -f namespace.yaml
# kubectl config set-context --current --namespace=face-recogn

kubectl apply -f configuration.yaml

cd volumes

kubectl apply -f data-volume.yaml
kubectl apply -f data-claim.yaml

kubectl apply -f model-volume.yaml
kubectl apply -f model-claim.yaml

cd -

kubectl apply -f webapp-deployment.yaml
kubectl apply -f frontend-deployment.yaml
# kubectl apply -f learning-deployment.yaml

