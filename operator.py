import kopf
import logging
import kubernetes
import kubernetes.client
from kubernetes.client.rest import ApiException
import urllib3

# Suppress SSL warnings for development (not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@kopf.on.create('annotations')
def create_fn(spec, meta, **kwargs):
    annotations = spec.get('annotations', [])
    namespace = meta.get('namespace')

    if not namespace:
        kopf.warn(f"Missing namespace for creation")
        return

    api = kubernetes.client.CoreV1Api()
    try:
        pods = api.list_namespaced_pod(namespace=namespace)

        for pod in pods.items:
            for annotation in annotations:
                try:
                    annotation_key = annotation['key']
                    annotation_value = annotation['value']
                    patch = {
                        "metadata": {
                        "annotations": {
                                    annotation_key: annotation_value
                            }
                        }
                    }
                    api.patch_namespaced_pod(name=pod.metadata.name, namespace=namespace, body=patch)
                except ApiException as e:
                    kopf.exception(f"Exception when updating pod {pod.metadata.name}: {e}")
    except ApiException as e:
        kopf.exception(f"Exception when listing pods in namespace {namespace}: {e}")

@kopf.on.delete('annotations')
def on_delete(spec, meta, **kwargs):
    annotations = spec.get('annotations', [])
    namespace = meta.get('namespace')

    if not namespace:
        kopf.warn(f"Missing namespace for deletion")
        return

    api = kubernetes.client.CoreV1Api()
    try:
        pods = api.list_namespaced_pod(namespace=namespace)

        for pod in pods.items:
            for annotation in annotations:
                try:
                    annotation_key = annotation['key']

                    patch = {
                        "metadata": {
                            "annotations": {
                                    annotation_key: None
                            }
                        }
                    }
                    api.patch_namespaced_pod(name=pod.metadata.name, namespace=namespace, body=patch)
                except ApiException as e:
                        kopf.exception(f"Exception when removing annotation from pod {pod.metadata.name}: {e}")
    except ApiException as e:
        kopf.exception(f"Exception when listing pods in namespace {namespace}: {e}")
