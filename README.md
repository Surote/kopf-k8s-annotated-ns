## Overview

This script uses the `kopf` framework to manage Kubernetes pod annotations across a specified namespace.

### Features

- **Add Annotations**: Automatically add specified annotations to all pods in a namespace when a creation event is detected.
- **Remove Annotations**: Automatically remove specified annotations from all pods in a namespace when a deletion event is detected.

### Installation

Ensure you have `kopf`, `kubernetes`, and all necessary dependencies installed. You can typically install these using pip:

```bash
pip install kopf kubernetes
```

### Usage
```usage
kopf run -A annotated_operator.py
```

```
oc apply -f test.yaml
oc delete -f test.yaml
```