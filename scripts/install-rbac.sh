#!/bin/bash
kubectl apply -f /home/jordan/Desktop/Rules-based-auth/platform/kube/deployment.yaml
kubectl apply -f /home/jordan/Desktop/Rules-based-auth/networking/rbac-gateway.yaml
kubectl apply -f /home/jordan/Desktop/Rules-based-auth/security/rbac-policy.yaml
kubectl apply -f /home/jordan/Desktop/Rules-based-auth/networking/auth0-egress.yaml
kubectl apply -f /home/jordan/Desktop/Rules-based-auth/security/rbac/enable-rbac.yaml
kubectl apply -f /home/jordan/Desktop/Rules-based-auth/security/rbac/admin-role.yaml
kubectl apply -f /home/jordan/Desktop/Rules-based-auth/security/rbac/user-role.yaml



kubectl delete -f /home/jordan/Desktop/Rules-based-auth/networking/auth0-egress.yaml
kubectl delete -f /home/jordan/Desktop/Rules-based-auth/security/rbac-policy.yaml
kubectl delete -f /home/jordan/Desktop/Rules-based-auth/security/rbac/enable-rbac.yaml
kubectl delete -f /home/jordan/Desktop/Rules-based-auth/security/rbac/admin-role.yaml
kubectl delete -f /home/jordan/Desktop/Rules-based-auth/security/rbac/user-role.yaml



kubectl apply -f /home/jordan/Desktop/Rules-based-auth/istio-custom-auth-adapter/cluster-service.yaml
kubectl apply -f /home/jordan/Desktop/Rules-based-auth/istio-custom-auth-adapter/mygrpcadapter/testdata/template.yaml
kubectl apply -f /home/jordan/Desktop/Rules-based-auth/istio-custom-auth-adapter/mygrpcadapter/testdata/attributes.yaml
kubectl apply -f /home/jordan/Desktop/Rules-based-auth/istio-custom-auth-adapter/mygrpcadapter/testdata/mygrpcadapter.yaml
kubectl apply -f /home/jordan/Desktop/Rules-based-auth/istio-custom-auth-adapter/mygrpcadapter/testdata/sample-operator-cfg.yaml



kubectl delete -f /home/jordan/Desktop/Rules-based-auth/istio-custom-auth-adapter/cluster-service.yaml
kubectl delete -f /home/jordan/Desktop/Rules-based-auth/istio-custom-auth-adapter/mygrpcadapter/testdata/template.yaml
kubectl delete -f /home/jordan/Desktop/Rules-based-auth/istio-custom-auth-adapter/mygrpcadapter/testdata/attributes.yaml
kubectl delete -f /home/jordan/Desktop/Rules-based-auth/istio-custom-auth-adapter/mygrpcadapter/testdata/mygrpcadapter.yaml
kubectl delete -f /home/jordan/Desktop/Rules-based-auth/istio-custom-auth-adapter/mygrpcadapter/testdata/sample-operator-cfg.yaml



kubectl get pods -n istio-system
kubectl logs po/mygrpcadapter-57fcc9bd9b-6xbkc -n istio-system