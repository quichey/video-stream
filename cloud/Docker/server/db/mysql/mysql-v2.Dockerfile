FROM mysql:oraclelinux9

ENV MYSQL_ROOT_PASSWORD="blah"
EXPOSE 8080
# Set the command to start the MySQL server in the foreground
#CMD ["mysqld"]

##
## Make mysql listen on Port 8080 for G-Cloud Run/Build
##
# Copy the custom MySQL configuration file
COPY ./mysql/my.cnf /etc/mysql/conf.d/my.cnf
RUN chmod 644 /etc/mysql/conf.d/my.cnf
# Start the MySQL server in the foreground, using the custom configuration
CMD ["mysqld", "--defaults-file=/etc/mysql/conf.d/my.cnf"]


## this one fails on microdnf not existing
# maybe just install yum