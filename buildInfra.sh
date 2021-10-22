docker build endPoint/. -t endpoint_cdk8demo
docker build service/. -t service_cdk8demo

docker tag endpoint_cdk8demo:latest kubernetes-Standard-PC-Q35-ICH9-2009.local:5000/kubernetes/endpoint_cdk8demo:latest
docker tag service_cdk8demo:latest kubernetes-Standard-PC-Q35-ICH9-2009.local:5000/kubernetes/service_cdk8demo:latest

docker image push kubernetes-Standard-PC-Q35-ICH9-2009.local:5000/kubernetes/endpoint_cdk8demo:latest
docker image push kubernetes-Standard-PC-Q35-ICH9-2009.local:5000/kubernetes/service_cdk8demo:latest

cd cdk
npm run compile && npm run synth

scp dist/cdk.k8s.yaml kubernetes@kubernetes-Standard-PC-Q35-ICH9-2009.local:deployment