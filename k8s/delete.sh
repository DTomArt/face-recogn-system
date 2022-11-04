#!/bin/bash
kubectl delete deployment webapp-deployment
kubectl delete deployment learning-deployment

kubectl delete pvc model-pv-claim
kubectl delete pv model-pv-volume

kubectl delete pvc data-pv-claim
kubectl delete pv data-pv-volume