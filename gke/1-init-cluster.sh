#!/usr/bin/env bash

# upstream source:
# https://github.com/jonbcampos/kubernetes-series/tree/master/helm/scripts/startup.sh
# blog post:
# https://medium.com/google-cloud/install-secure-helm-in-gke-254d520061f7

echo "preparing..."
export GCLOUD_PROJECT=$(gcloud config get-value project)
export INSTANCE_REGION=us-west1
export INSTANCE_ZONE=us-west1-a
export CLUSTER_NAME=${GCLOUD_PROJECT}-cluster
export CONTAINER_NAME=${GCLOUD_PROJECT}-container

echo "setup"
gcloud config set compute/zone ${INSTANCE_ZONE}

echo "enable services"
gcloud services enable compute.googleapis.com
gcloud services enable container.googleapis.com

echo "creating container engine cluster"
gcloud container clusters create ${CLUSTER_NAME} \
    --preemptible \
    --zone ${INSTANCE_ZONE} \
    --scopes cloud-platform \
    --enable-autorepair \
    --enable-autoupgrade \
    --enable-autoscaling --min-nodes 1 --max-nodes 4 \
    --num-nodes 2

echo "confirm cluster is running"
gcloud container clusters list

echo "get credentials"
gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${INSTANCE_ZONE}

echo "confirm connection to cluster"
kubectl cluster-info

echo "create cluster administrator"
kubectl create clusterrolebinding cluster-admin-binding \
    --clusterrole=cluster-admin --user=$(gcloud config get-value account)

echo "confirm the pod is running"
kubectl get pods

echo "list production services"
kubectl get svc

echo "enable services"
gcloud services enable cloudbuild.googleapis.com
