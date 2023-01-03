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

kubectl delete configmap cluster-configuration

kubectl delete role.rbac.authorization.k8s.io/pod-reader
kubectl delete serviceaccount/frontend-sa
kubectl delete clusterrole.rbac.authorization.k8s.io/frontend-role
kubectl delete clusterrolebinding.rbac.authorization.k8s.io/frontend-binding
