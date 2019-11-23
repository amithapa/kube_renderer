## Kube Reder

This is a simple python program that will render the kuberntes deployment files by substituting dynamic constants based on the parameters and render it. 

## Motivation

To simplify the process of generating dynamic kubernetes file for deploying it in multiple environments. 



### Command to run and generate the kube deploy files

```bash
python kube_render/kube_renderer.py --instance_status production --docker_image_version 1 --base_dir $(pwd)/kube_render/example
```