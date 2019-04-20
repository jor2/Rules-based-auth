#!/bin/bash
minikube start --memory=8192 --cpus=4
kubectl apply -f /home/jordan/istio-1.0.5/install/kubernetes/helm/istio/templates/crds.yaml
kubectl apply -f /home/jordan/istio-1.0.5/install/kubernetes/istio-demo.yaml
sudo kubectl patch svc -n istio-system grafana --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"}]'
sudo kubectl patch svc -n istio-system prometheus --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"}]'
sudo kubectl patch svc -n istio-system servicegraph --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"}]'
sudo kubectl patch svc -n istio-system zipkin --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"}]'
sudo kubectl patch svc -n istio-system jaeger-collector --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"}]'
sudo kubectl patch svc -n istio-system jaeger-query --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"}]'
sudo kubectl patch svc -n istio-system tracing --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"}]'
echo "kubectl get svc -n istio-system"
kubectl get svc -n istio-system
echo "kubectl get pods -n istio-system"
kubectl get pods -n istio-system
#echo "kubectl describe svc -n istio-system istio-ingressgateway"
#kubectl describe svc -n istio-system istio-ingressgateway
#istioctl authn tls-check