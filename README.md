# Face recognition system

## celebrity-face-learn-app

A python app for training machine learning model for detecting faces of celebrities and sending calculated model to google drive.

Needed dataset:  
https://www.kaggle.com/datasets/hereisburak/pins-face-recognition

Run app by adding symlink and running docker-compose:  
`ln -sf docker-compose.train.yml docker-compose.yml`  
`docker-compose up`

## face-recogn-app

A python web app for detecting faces which uses cv2 for face detection and model developed in celebrity-face-learn-app.

How to run:

1. Generate model files using celebrity-face-learn-app(or placing them there manually):  
   Model/FaceRecogn.h5 (file with model)  
   Model/classes.txt (file with labels(celebrities names) for indexes extracted from model)

2. Similarly as above run app by adding symlink and running docker-compose:  
   `ln -sf docker-compose.deploy.yml docker-compose.yml`  
   `docker-compose up`

## How to run the system in Kubernetes?

1. Place the model and classes generated in *celebrity-face-learn-app* to catalog *Model/* in main project directory. You should also edit paths in k8s configuration to match these on your control-plane. Edit them in *k8s/volumes/model-volume.yaml*, *k8s/webapp-deployment.yaml*.

2. Set up your cluster with at least one node with camera connected to it (you can use k3s as did I in developing on 'production') and install helm on control-plane:  
   `sudo apt install -y curl`  
   `curl -L https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash`  

3. Execute script `k8s/create-cameras.sh` to create akri cameras' server using helm in namespace 'face-recogn' and pick this namespace (edit camera format, width, height and frames in this script to match your camera).

4. After a couple of minutes you should have akri set up (a bunch of k8s resources: deamons, pods). You can validate your akri cameras' server with checking the resources with:  
   `kubectl get all`  
   If everything is fine Akri should detect your camera and create service for it which should look like this: '*service/akri-udev-video-XXXXXX-svc*'. Copy the IP from CLUSTER-IP column and place it in k8s/configuration.yaml in commented place.

5. You may now create deployment with frontend and backend. To do so just execute script `k8s/create-deployment.sh`.  
   After executing in couple of minutes - after downloading images and setting up the pods - you should have properly running containers. If some of them are crashing you should check logs and validate your configuration.

6. If your pods are running properly the last step is forwarding port from you control plane to your PC. To do so, on your PC use ssh:  
   `ssh controlplane-IP -L 50000:localhost:31000`  
   Now you should be able to find frontend on your PC at *http://localhost:50000/* (or *http://localhost:31000/* on your control-plane). Just click the button 'Show Live Camera' to redirect to your camera in the web (which should recognize faces based on the model).

*Instruction and implementation based on _https://web.archive.org/web/20220819023030/https://docs.akri.sh/demos/usb-camera-demo-rpi4_*