# Nauta System Software Components Requisites
Nauta requires certian components, as shown in Table 1 before beginning your installation. 

## List of External Software Components

Table 1 shows the software package that includes the external software components for Nauta. 

Name | Version | Project link
--- | --- | --- 
addon-resizer | 1.7 | http://k8s.gcr.io/addon-resizer
dashboard | 1.8.3 | https://k8s.gcr.io/kubernetes-dashboard-amd64 
defaultbackend | 1.4 | https://github.com/kubernetes/ingress-nginx
dnsmasq-nanny | 1.14.8 | https://github.com/kubernetes/dns
dns-sidecar | 1.14.8 | https://github.com/kubernetes/dns
etcd | 3.3.9 | https://github.com/coreos/etcd
elasticsearch | 6.2.3 | https://github.com/elastic/elasticsearch
flannel | 0.9.1 | https://github.com/coreos/flannel
fluentd | 0.12 | https://www.fluentd.org/
heapster | 1.4.2 | https://github.com/kubernetes/heapster
ingress | 0.14.0 | http://quay.io/kubernetes-ingress-controller/nginx-ingress-controller
kubectl | 1.10.6 | https://github.com/kubernetes/kubernetes/tree/master/pkg/kubectl
kube-dns | 1.14.8 | https://github.com/kubernetes/dns 
kube-proxy | 1.10.6 | http://gcr.io/google-containers/kube-proxy-amd64
mkl-dnn | 0.14 | https://github.com/intel/mkl-dnn
nginx | 1.14.0 | https://www.nginx.com/ 
pause | 3.1 | http://gcr.io/google-containers/pause-amd64
redsocks | 0.5 | https://github.com/darkk/redsocks
registry | 2.6.2 | https://github.com/docker/distribution
tensorflow | 1.9.0 | https://github.com/tensorflow/tensorflow
tiller | 2.9.1 | https://github.com/helm/helm

## Key Components
Key Compponents include: 
* Nauta complete bundle (including installation scripts and reference configuration).
  * Vanilla Kubernetes cluster on top of provisioned Hardware and Operating System-level Software.
  * Nauta components (containerized components, their configuration, integration method, and so on.)
  * Used software components are optimized for AI containers with Nauta-optimized libraries

## Inlcluded Documentation
* Installation and Configuration Guide 
  * Format = PDF
* User Guide
  * Format = HTML
* Release Notes
  * Format = HTML & PDF