#!/bin/bash
kubectl delete deployment webapp-deployment
kubectl delete deployment learning-deployment
kubectl delete deployment frontend-deployment

kubectl delete service/webapp-svc
kubectl delete service/frontend-svc

kubectl delete pvc model-pv-claim
kubectl delete pv model-pv-volume

kubectl delete pvc data-pv-claim
kubectl delete pv data-pv-volume

# kubectl delete akric akri-udev-video && helm delete akri