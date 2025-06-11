# serverless-demo

This is the code used in the presentation "Effortlessly Scale Your Applications with OpenShift Serverless" made at DevConf.CZ 2025.

## Running the demo

To run this demo, you need a Kubernetes instance. This should work on Minikube, Kind, CodeReady Containers, Minishift, and other platforms. Also, you need to install Serverless with Serving and Eventing features. The demo was developed on CodeReady Containers. Below, you will find documentation on CodeReady Containers and Serverless.

### References

* [Red Hat OpenShift Local (CodeReady Containers)](https://developers.redhat.com/products/openshift-local/overview)
* [CRC Documentation](https://crc.dev/docs/getting-started/)
* [Serverless installation](https://docs.redhat.com/en/documentation/red_hat_openshift_serverless/1.35/html/installing_openshift_serverless/index)
* [Knative Serving installation](https://docs.redhat.com/en/documentation/red_hat_openshift_serverless/1.35/html/installing_openshift_serverless/installing-knative-serving)
* [Knative Eventing installation](https://docs.redhat.com/en/documentation/red_hat_openshift_serverless/1.35/html/installing_openshift_serverless/installing-knative-eventing)

## Enabling the local registry

You can use the local registry to push the container images. Log in to your Kubernetes instance and follow the steps below to enable access to it.

1. Give read and right access to the developer user:

    ```
    oc policy add-role-to-user registry-viewer developer
    ```
    
    ```
    oc policy add-role-to-user registry-editor developer
    ```

2. Log in to the OpenShift Registry:

    ```
    podman login -u developer -p $(oc whoami -t) --tls-verify=false https://default-route-openshift-image-registry.apps-crc.testing
    ```

## Build and deploy the application

To build and deploy the application, follow the steps below.

1. Create the application project

    ```
    oc new-project serverless-demo
    ```

2. Build the application

    ```
    podman build -t serverless:latest .
    ```

    ```
    podman tag localhost/serverless:latest default-route-openshift-image-registry.apps-crc.testing/serverless-demo/serverless:latest
    ```

    ```
    podman push --tls-verify=false default-route-openshift-image-registry.apps-crc.testing/serverless-demo/serverless:latest
    ```

3. Deploy the application

    ```
    oc apply -f deployment/config.yml
    ```

    ```
    oc apply -f deployment/worker.yml
    ```

    ```
    oc apply -f deployment/api.yml
    ```

    ```
    oc apply -f deployment/broker.yml
    ```

    ```
    oc apply -f deployment/trigger.yml
    ```

## Test the application

To test the application, send a request to the endpoint.

### Watch the API and Worker logs

Monitor the logs of the pods to view the request results.

```
oc get pods
```

**Note:** change the pods' names with the output of the previous command.

```
oc logs -f api-00001-deployment-6fbc5f7f84-lnhbn
```

```
oc logs -f worker-00001-deployment-b575ddc64-lf54p
```

### Find the API route

The following command shows the route to the API and the Worker. Use the API route to send requests to the application.

```
oc get serving
```

### Send requests to the application

```
curl -k -X POST https://api-serverless-demo.apps-crc.testing -H "accept: application/json" -H "Content-Type: application/json" -d "{\"work\": \"clean my bedroom\", \"duration\": 5}"
```

## Flood the worker

To see Serverless spawning new Worker pods, flood the Worker pod with requests.

```
seq 1 300 | xargs -P0 -I{} curl -k -X POST https://worker-serverless-demo.apps-crc.testing -H "accept: application/json" -H "Content-Type: application/json" -d "{\"work\": \"clean my bedroom\", \"duration\": 5}"
```
