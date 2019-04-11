# commands are assumed to be run from inside the gke/ directory

# 1. create a gcloud project:
gcloud projects create project-id --set-as-default

# 2: build & push docker images
gcloud auth configure-docker

docker build -f docker/flask/Dockerfile.prod -t gcr.io/project-id/backend .
docker push gcr.io/project-id/backend

docker build -f docker/marketstore/Dockerfile -t gcr.io/project-id/marketstore .
docker push gcr.io/project-id/marketstore

docker build -f docker/postgres/Dockerfile -t gcr.io/project-id/postgres .
docker push gcr.io/project-id/postgres

docker build -f docker/react/Dockerfile.prod -t gcr.io/project-id/react .
docker push gcr.io/project-id/react

# 3. deploy cluster
```bash
# edit environment variables at top, then run init cluster:
bash 1-init-cluster.sh

# edit SUBJECT to specify correct country & domain, then install helm/tiller:
bash 2-install-secure-helm.sh

# install nginx-ingress
helm install --tls stable/nginx-ingress --name project-id

# configure DNS 
#
# get ClusterIP of `project-id-nginx-ingress-controller        LoadBalancer`
kubectl get svc
# create a cloud dns zone: https://console.cloud.google.com/net-services/dns/zones
# create A record for ClusterIP -> domain.com
# create CNAME record for www.domain.com -> domain.com

# deploy frontend
kubectl apply -f react/deployment.yaml
kubectl apply -f react/service.yaml

# install cert-manager CRDs
kubectl apply -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.7/deploy/manifests/00-crds.yaml

# this step is only necessary if namespace "cert-manager" already exists
# ref: https://docs.cert-manager.io/en/latest/getting-started/webhook.html#disabling-validation-on-the-cert-manager-namespace
kubectl label namespace cert-manager certmanager.k8s.io/disable-validation="true"

# add the cert-manager helm repo and sync
helm repo add jetstack https://charts.jetstack.io
helm repo update

# install cert-manager
helm install --tls --name cert-manager --namespace cert-manager jetstack/cert-manager

# create let's encrypt issuer
kubectl apply -f tls/prod-issuer.yaml

# ingress.yaml (edit domain to use the one configured with DNS above)
kubectl apply -f nginx/ingress.yaml

# to regenerate certificates, delete existing (new certs generated automatically)
kubectl delete secret project-id-tls

# deploy remaining services
kubectl apply -f redis
kubectl apply -f postgres
kubectl apply -f marketstore
kubectl apply -f flask

# run jobs (sequentially)
kubectl apply -f jobs/job-migrations.yaml
kubectl apply -f jobs/job-init-db.yaml
kubectl apply -f jobs/job-init-finance.yaml
```
