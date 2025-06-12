###################################################
# Stage: proxy
# 
# if i do need my own custom proxy
# i think need to upload to Docker Hub
# so that it can be used in the FROM cmd
###################################################
FROM nginxproxy/nginx-proxy:20 AS proxy
WORKDIR /usr/local/app


# TODO: figure out things about nginx
COPY ~/repos/video-stream/server ./server


# start up nginx server
CMD ["nginx"]