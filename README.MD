# DAT455-Lab2
This is the solution of the sceond lab in the course DAT455 that is given at Chalmers Univeristy of technology

1) Build the docker image by running the following command:
   1) Navigate to directory containing the dockerfile
   2) docker build -t NAMEOFYOURCHOICE . (Do not forget the dot)
    
2) Run the docker image :
   1) If using linux enable x11 by running: 

      xhost + 
   2) Run the docke image by using the following command:

      docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix game/image:latest

3) You can run this command instead of steps 1 and 2 which will look for the image build it and then run it :

      docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ghcr.io/sharineh/game/image:latest
