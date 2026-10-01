# 1. Azure subscription
```
az account show -o table
az account list -o table
```
# 2. Resource Group
```
az group show \
  --name university-erp-rg \
  -o table
```
# 3. AKS cluster — overall health
```
az aks list -o table
```
```
az aks show \
  --resource-group university-erp-rg \
  --name university-erp-aks \
  --query "{name:name,location:location,provisioningState:provisioningState,powerState:powerState,kubernetesVersion:kubernetesVersion,sku:sku,nodeResourceGroup:nodeResourceGroup,fqdn:fqdn}" \
  -o yaml
```
# 4. AKS credentials / Kubernetes connectivity
```
az aks get-credentials \
  --resource-group university-erp-rg \
  --name university-erp-aks \
  --overwrite-existing
```
```
kubectl config current-context
kubectl cluster-info
kubectl get nodes -o wide
```

# 5. Node pools — System/User and VM details
```
az aks nodepool list \
  --resource-group university-erp-rg \
  --cluster-name university-erp-aks \
  -o table
```
```
az aks nodepool show \
  --resource-group university-erp-rg \
  --cluster-name university-erp-aks \
  --name nodepool1 \
  -o yaml
```
# 6. Node health
```
kubectl get nodes
kubectl describe nodes
kubectl top nodes
```
# 7. Namespaces
```
kubectl get namespaces
```
# 8. ERP namespace
```
kubectl get all -n erp
```
# 9. Pods
```
kubectl get pods -n erp -o wide
kubectl get pods -n erp -o wide --show-labels
```
# 10. Unhealthy pods
```
kubectl get pods -n erp \
  --field-selector=status.phase!=Running
```
```
kubectl describe pod <POD_NAME> -n erp
```
# 11. Pod logs
```
kubectl logs <POD_NAME> -n erp
```
```
kubectl logs <POD_NAME> -n erp --previous
```
# 12. Deployments
```
kubectl get deployments -n erp
```
```
kubectl describe deployment <DEPLOYMENT_NAME> -n erp
```
# 13. ReplicaSets
```
kubectl get replicasets -n erp
```
```
kubectl describe replicaset <REPLICASET_NAME> -n erp
```
# 14. Services
```
kubectl get services -n erp
```
```
kubectl describe service <SERVICE_NAME> -n erp
```
# 15. Endpoints
```
kubectl get endpoints -n erp
```
```
kubectl get endpointslices -n erp
```
# 16. Ingress
```
kubectl get ingress -A
```
```
kubectl describe ingress <INGRESS_NAME> -n erp
```
# 17. Ingress controller
```
kubectl get pods -n ingress-nginx -o wide
```
```
kubectl get svc -n ingress-nginx
```
```
kubectl logs -n ingress-nginx <INGRESS_CONTROLLER_POD>
```
# 18. Certificates
```
kubectl get pods -n cert-manager
kubectl get certificates -A
kubectl get certificaterequests -A
kubectl get challenges -A
kubectl get orders -A
```
# 19. Redis
```
kubectl get pods -n erp -l app=redis
kubectl logs -n erp <REDIS_POD>
```
# 20. Events — very useful for troubleshooting
```
kubectl get events -n erp --sort-by=.lastTimestamp
```
# 21. Storage
```
kubectl get pvc -n erp
kubectl get pv
kubectl describe pvc <PVC_NAME> -n erp
```
# 22. Resource consumption
```
kubectl top pods -n erp
kubectl top nodes
```
# 23. Network / DNS
```
kubectl get svc -A
kubectl get networkpolicy -A
```
```
kubectl run dns-test \
  --image=busybox:1.36 \
  --rm -it --restart=Never \
  -- nslookup kubernetes.default
```
# 24. AKS control-plane/nodepool health
```
az aks show \
  --resource-group university-erp-rg \
  --name university-erp-aks \
  --query "{provisioningState:provisioningState,powerState:powerState,version:kubernetesVersion,sku:sku,nodeRG:nodeResourceGroup}" \
  -o yaml
```
# 25. Azure Activity Log — if Azure-side problem
```
az monitor activity-log list \
  --resource-group university-erp-rg \
  --max-events 50 \
  -o table
```
# AKS SETUP:
```
$sudo dnf install -y https://packages.microsoft.com/config/rhel/9/packages-microsoft-prod.rpm
$sudo dnf install -y azure-cli
$az version
{
  "azure-cli": "2.90.0",
  "azure-cli-core": "2.90.0",
  "azure-cli-telemetry": "1.1.0",
  "extensions": {}
}
$az login --use-device-code
To sign in, use a web browser to open the page https://login.microsoft.com/device and enter the code XYZ123ABC to authenticate.

Retrieving tenants and subscriptions for the selection...
No subscriptions found for myazureaccess@gmail.com.

$az account list -o table
```
